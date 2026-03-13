"""
Hugging Face ASR (Automatic Speech Recognition) service implementation.
Supports both CTC models (Wav2Vec2, W2V-BERT, etc.) and Seq2Seq models
(Whisper) — the correct architecture is detected automatically at load time.
"""

try:
    import torch
    import torchaudio
    from transformers import (
        AutoProcessor,
        AutoModelForCTC,
        AutoModelForSpeechSeq2Seq,
        AutoConfig,
    )
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from django.conf import settings
from typing import Dict, Any
import logging

from .base import ASRService

logger = logging.getLogger(__name__)

# Model families that require the Seq2Seq (encoder-decoder) pipeline
_SEQ2SEQ_MODEL_TYPES = {"whisper", "seamless_m4t", "speech_to_text"}


def _check_torch_available():
    """Check if torch is available, raise error only if actually trying to use it."""
    if not TORCH_AVAILABLE:
        raise ImportError(
            "torch and torchaudio are required for local ASR models. "
            "Use HF Inference API instead: SET USE_HF_INFERENCE=True in .env"
        )


def _is_seq2seq_model(model_name: str) -> bool:
    """Return True if *model_name* is a seq2seq (encoder-decoder) ASR model."""
    try:
        config = AutoConfig.from_pretrained(
            model_name, cache_dir=settings.HF_CACHE_DIR
        )
        return config.model_type in _SEQ2SEQ_MODEL_TYPES
    except Exception:
        # Fallback heuristic when config cannot be fetched
        lower = model_name.lower()
        return any(tag in lower for tag in ("whisper", "seamless"))


class HuggingFaceASR(ASRService):
    """
    ASR service using Hugging Face models.
    Automatically detects whether the configured model is CTC-based
    (Wav2Vec2, W2V-BERT …) or Seq2Seq-based (Whisper …) and loads the
    appropriate classes.
    """

    def __init__(self):
        """Initialize ASR service with lazy loading."""
        self.processors = {}
        self.models = {}
        self.model_configs = settings.MODELS['asr']
        # Track which architecture each loaded model uses
        self._is_seq2seq: Dict[str, bool] = {}

    def _load_model(self, language: str):
        """
        Lazy load model for specified language.

        Args:
            language: Language code (kikuyu, swahili, english)
        """
        if language not in self.models:
            model_name = self.model_configs.get(language)
            if not model_name:
                raise ValueError(f"No ASR model configured for language: {language}")

            logger.info(f"Loading ASR model for {language}: {model_name}")

            try:
                seq2seq = _is_seq2seq_model(model_name)
                self._is_seq2seq[language] = seq2seq

                self.processors[language] = AutoProcessor.from_pretrained(
                    model_name,
                    cache_dir=settings.HF_CACHE_DIR,
                )

                if seq2seq:
                    logger.info(f"Detected Seq2Seq model for {language} — using AutoModelForSpeechSeq2Seq")
                    self.models[language] = AutoModelForSpeechSeq2Seq.from_pretrained(
                        model_name,
                        cache_dir=settings.HF_CACHE_DIR,
                    )
                else:
                    logger.info(f"Detected CTC model for {language} — using AutoModelForCTC")
                    self.models[language] = AutoModelForCTC.from_pretrained(
                        model_name,
                        cache_dir=settings.HF_CACHE_DIR,
                    )

                # Move to GPU if available
                if torch.cuda.is_available():
                    self.models[language] = self.models[language].cuda()

                logger.info(f"Successfully loaded ASR model for {language}")

            except Exception as e:
                logger.error(f"Error loading ASR model for {language}: {str(e)}")
                raise

    # ------------------------------------------------------------------
    # Language code helpers for Whisper forced-decoder-prompt
    # ------------------------------------------------------------------
    _WHISPER_LANG_CODES = {
        "english": "en",
        "swahili": "sw",
        "kikuyu": "ki",       # best-effort; Whisper may fall back to auto-detect
    }

    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """
        Transcribe audio file to text.

        Supports both CTC models (Wav2Vec2 / W2V-BERT) and Seq2Seq models
        (Whisper).  The correct inference path is chosen automatically based
        on the model that was loaded for *language*.

        Args:
            audio_path: Path to audio file (wav, mp3, etc.)
            language: Source language code

        Returns:
            dict: {"text": str, "confidence": float}
        """
        try:
            # Load model if not already loaded
            self._load_model(language)

            # Load and preprocess audio
            waveform, sample_rate = torchaudio.load(audio_path)

            # Resample if needed (most models expect 16 kHz)
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(
                    orig_freq=sample_rate,
                    new_freq=16000,
                )
                waveform = resampler(waveform)

            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)

            if self._is_seq2seq.get(language):
                return self._transcribe_seq2seq(waveform, language)
            else:
                return self._transcribe_ctc(waveform, language)

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise RuntimeError(f"Transcription failed: {str(e)}")

    # ------------------------------------------------------------------
    # CTC inference (Wav2Vec2, W2V-BERT, etc.)
    # ------------------------------------------------------------------
    def _transcribe_ctc(self, waveform, language: str) -> Dict[str, Any]:
        inputs = self.processors[language](
            waveform.squeeze().numpy(),
            sampling_rate=16000,
            return_tensors="pt",
        )

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        with torch.no_grad():
            logits = self.models[language](**inputs).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processors[language].batch_decode(predicted_ids)[0]

        # Confidence from token-level softmax
        probs = torch.softmax(logits, dim=-1)
        max_probs = torch.max(probs, dim=-1).values
        confidence = float(torch.mean(max_probs).cpu())

        logger.info(f"CTC transcription ({language}): {transcription[:50]}… (conf: {confidence:.2f})")

        return {
            "text": transcription.strip(),
            "confidence": round(confidence, 3),
        }

    # ------------------------------------------------------------------
    # Seq2Seq inference (Whisper, etc.)
    # ------------------------------------------------------------------
    def _transcribe_seq2seq(self, waveform, language: str) -> Dict[str, Any]:
        processor = self.processors[language]
        model = self.models[language]

        inputs = processor(
            waveform.squeeze().numpy(),
            sampling_rate=16000,
            return_tensors="pt",
        )

        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        # Build generate kwargs — set language for Whisper when possible
        generate_kwargs: Dict[str, Any] = {}
        whisper_lang = self._WHISPER_LANG_CODES.get(language)
        if whisper_lang is not None:
            generate_kwargs["language"] = whisper_lang
            generate_kwargs["task"] = "transcribe"

        with torch.no_grad():
            predicted_ids = model.generate(
                inputs["input_features"],
                **generate_kwargs,
            )

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # Whisper doesn't expose per-token probabilities easily;
        # use a fixed high confidence since the model is generally reliable.
        confidence = 0.92

        logger.info(f"Seq2Seq transcription ({language}): {transcription[:50]}… (conf: {confidence})")

        return {
            "text": transcription.strip(),
            "confidence": confidence,
        }

