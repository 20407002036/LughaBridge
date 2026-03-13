"""
gTTS (Google Text-to-Speech) service implementation.
Lightweight, no-GPU alternative that calls Google Translate's TTS endpoint.
Supports English and Swahili but NOT Kikuyu.
"""

import logging
import os
import uuid

from django.conf import settings
from pydub import AudioSegment

from .base import TTSService

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not installed. Run: pip install gTTS>=2.5.0")

logger = logging.getLogger(__name__)

# Map internal LughaBridge language names to gTTS/IETF language codes
GTTS_LANG_MAP = {
    'english': 'en',
    'swahili': 'sw',
    # Kikuyu is NOT supported by gTTS
}


class GttsTTS(TTSService):
    """
    Text-to-Speech service using Google Translate's TTS endpoint via gTTS.

    Pros:
      - No GPU / local model required
      - Fast, lightweight
      - Good quality for supported languages
    Cons:
      - Requires internet access
      - Kikuyu is not supported (falls back to HF/MMS if configured)
    """

    def __init__(self):
        """Initialize gTTS service."""
        if not GTTS_AVAILABLE:
            raise ImportError("gTTS is required. Run: pip install gTTS>=2.5.0")

        # Directory for generated audio files
        self.temp_dir = os.path.join(settings.MEDIA_ROOT, 'tts_temp')
        os.makedirs(self.temp_dir, exist_ok=True)

        # Optional: a fallback TTS service for unsupported languages (e.g. Kikuyu)
        self._fallback_service = None

        logger.info("GttsTTS service initialised")

    @property
    def fallback_service(self):
        """Lazy-load fallback TTS service for unsupported languages."""
        if self._fallback_service is None:
            use_hf = getattr(settings, 'USE_HF_INFERENCE', False)
            if use_hf:
                try:
                    from .hf_inference_services import HFInferenceTTS
                    self._fallback_service = HFInferenceTTS()
                    logger.info("GttsTTS fallback → HFInferenceTTS")
                except Exception as e:
                    logger.warning(f"Could not create HFInferenceTTS fallback: {e}")
            else:
                try:
                    from .mms_tts import MMSTTS
                    self._fallback_service = MMSTTS()
                    logger.info("GttsTTS fallback → MMSTTS (local)")
                except Exception as e:
                    logger.warning(f"Could not create MMSTTS fallback: {e}")
        return self._fallback_service

    @staticmethod
    def supports_language(language: str) -> bool:
        """Check whether gTTS supports the given language."""
        return language in GTTS_LANG_MAP

    def synthesize(self, text: str, language: str, gender: str = "neutral") -> str:
        """
        Synthesize speech from text using gTTS.

        If the requested language is not supported by gTTS (e.g. Kikuyu),
        the call is delegated to a fallback TTS service when available.

        Args:
            text: Text to synthesize.
            language: Target language code (english, swahili, kikuyu …).
            gender: Voice gender preference (ignored by gTTS).

        Returns:
            str: Path to the generated WAV audio file.

        Raises:
            ValueError: If language is unsupported and no fallback is available.
            RuntimeError: If synthesis fails.
        """
        # ── Fallback for unsupported languages ──────────────────────────
        if not self.supports_language(language):
            fallback = self.fallback_service
            if fallback is not None:
                logger.info(
                    f"gTTS does not support '{language}'; "
                    f"delegating to {type(fallback).__name__}"
                )
                return fallback.synthesize(text, language, gender)

            raise ValueError(
                f"gTTS does not support language '{language}' and no "
                f"fallback TTS service is available."
            )

        gtts_lang = GTTS_LANG_MAP[language]

        logger.info(f"Synthesizing speech via gTTS for {language} ({gtts_lang}): {text[:50]}…")

        try:
            tts = gTTS(text=text, lang=gtts_lang)

            # gTTS outputs MP3; save to a temp file first
            mp3_filename = f"gtts_{uuid.uuid4().hex}.mp3"
            mp3_path = os.path.join(self.temp_dir, mp3_filename)
            tts.save(mp3_path)

            # Convert MP3 → WAV (16 kHz mono) for pipeline consistency
            wav_filename = f"tts_{uuid.uuid4().hex}.wav"
            wav_path = os.path.join(self.temp_dir, wav_filename)

            audio = AudioSegment.from_mp3(mp3_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_path, format="wav")

            # Clean up intermediate MP3
            os.remove(mp3_path)

            logger.info(f"gTTS synthesis successful: {wav_path}")
            return wav_path

        except Exception as e:
            logger.error(f"gTTS synthesis error for {language}: {e}")
            raise RuntimeError(f"gTTS synthesis failed: {e}")
