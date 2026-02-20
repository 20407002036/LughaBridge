"""
MMS-TTS (Massively Multilingual Speech - Text-to-Speech) service implementation.
"""

import torch
from transformers import VitsModel, AutoTokenizer
from django.conf import settings
from typing import Dict, Any
import logging
import os
import uuid
import scipy.io.wavfile

from .base import TTSService

logger = logging.getLogger(__name__)


class MMSTTS(TTSService):
    """
    Text-to-Speech service using Facebook's MMS-TTS models.
    Supports 1100+ languages including Kikuyu, Swahili, and English.
    """
    
    def __init__(self):
        """Initialize TTS service with lazy loading."""
        self.models = {}
        self.tokenizers = {}
        self.model_configs = settings.MODELS['tts']
        
        # Create temp directory for audio files
        self.temp_dir = os.path.join(settings.MEDIA_ROOT, 'tts_temp')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def _load_model(self, language: str):
        """
        Lazy load TTS model for specified language.
        
        Args:
            language: Language code (kikuyu, swahili, english)
        """
        if language not in self.models:
            model_name = self.model_configs.get(language)
            if not model_name:
                raise ValueError(f"No TTS model configured for language: {language}")
            
            logger.info(f"Loading TTS model for {language}: {model_name}")
            
            try:
                self.tokenizers[language] = AutoTokenizer.from_pretrained(
                    model_name,
                    cache_dir=settings.HF_CACHE_DIR
                )
                self.models[language] = VitsModel.from_pretrained(
                    model_name,
                    cache_dir=settings.HF_CACHE_DIR
                )
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.models[language] = self.models[language].cuda()
                    
                logger.info(f"Successfully loaded TTS model for {language}")
                
            except Exception as e:
                logger.error(f"Error loading TTS model for {language}: {str(e)}")
                raise
    
    def synthesize(self, text: str, language: str, gender: str = "neutral") -> str:
        """
        Synthesize speech from text using MMS-TTS.
        
        Args:
            text: Text to synthesize
            language: Target language code
            gender: Voice gender preference (currently not used by MMS-TTS)
            
        Returns:
            str: Path to generated audio file
        """
        try:
            # Load model if not already loaded
            self._load_model(language)
            
            logger.info(f"Synthesizing speech for {language}: {text[:50]}...")
            
            # Tokenize text
            inputs = self.tokenizers[language](
                text,
                return_tensors="pt",
                padding=True
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Generate speech
            with torch.no_grad():
                output = self.models[language](**inputs)
                waveform = output.waveform
            
            # Move to CPU and convert to numpy
            waveform_np = waveform.squeeze().cpu().numpy()
            
            # Generate unique filename
            audio_filename = f"tts_{uuid.uuid4().hex}.wav"
            audio_path = os.path.join(self.temp_dir, audio_filename)
            
            # Save as WAV file (MMS-TTS outputs at 16kHz)
            scipy.io.wavfile.write(
                audio_path,
                rate=16000,  # MMS-TTS sample rate
                data=waveform_np
            )
            
            logger.info(f"Speech synthesized successfully: {audio_path}")
            
            return audio_path
            
        except Exception as e:
            logger.error(f"Error during TTS synthesis: {str(e)}")
            raise RuntimeError(f"TTS synthesis failed: {str(e)}")
