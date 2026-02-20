"""
Hugging Face ASR (Automatic Speech Recognition) service implementation.
"""

import torch
import torchaudio
from transformers import AutoProcessor, AutoModelForCTC
from django.conf import settings
from typing import Dict, Any
import logging

from .base import ASRService

logger = logging.getLogger(__name__)


class HuggingFaceASR(ASRService):
    """
    ASR service using Hugging Face Wav2Vec2/W2V-BERT models.
    Supports Kikuyu, Swahili, and English.
    """
    
    def __init__(self):
        """Initialize ASR service with lazy loading."""
        self.processors = {}
        self.models = {}
        self.model_configs = settings.MODELS['asr']
        
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
                self.processors[language] = AutoProcessor.from_pretrained(
                    model_name,
                    cache_dir=settings.HF_CACHE_DIR
                )
                self.models[language] = AutoModelForCTC.from_pretrained(
                    model_name,
                    cache_dir=settings.HF_CACHE_DIR
                )
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.models[language] = self.models[language].cuda()
                    
                logger.info(f"Successfully loaded ASR model for {language}")
                
            except Exception as e:
                logger.error(f"Error loading ASR model for {language}: {str(e)}")
                raise
    
    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """
        Transcribe audio file to text using Wav2Vec2/W2V-BERT.
        
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
            
            # Resample if needed (most models expect 16kHz)
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(
                    orig_freq=sample_rate,
                    new_freq=16000
                )
                waveform = resampler(waveform)
            
            # Convert to mono if stereo
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            # Process audio
            inputs = self.processors[language](
                waveform.squeeze().numpy(),
                sampling_rate=16000,
                return_tensors="pt"
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Perform inference
            with torch.no_grad():
                logits = self.models[language](**inputs).logits
            
            # Decode predictions
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processors[language].batch_decode(predicted_ids)[0]
            
            # Calculate confidence score (using logits probability)
            probs = torch.softmax(logits, dim=-1)
            max_probs = torch.max(probs, dim=-1).values
            confidence = float(torch.mean(max_probs).cpu())
            
            logger.info(f"Transcription ({language}): {transcription[:50]}... (conf: {confidence:.2f})")
            
            return {
                "text": transcription.strip(),
                "confidence": round(confidence, 3)
            }
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise RuntimeError(f"Transcription failed: {str(e)}")
