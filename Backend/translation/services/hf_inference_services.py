"""
Hugging Face Inference API service implementations.
Uses cloud-hosted models via HF Inference API instead of local models.
"""

import logging
from typing import Dict, Any
from django.conf import settings
import os
import uuid

try:
    from huggingface_hub import InferenceClient
    HF_HUB_AVAILABLE = True
except ImportError:
    HF_HUB_AVAILABLE = False
    logging.warning("huggingface_hub not installed. Run: pip install huggingface_hub>=0.20")

from .base import ASRService, TranslationService, TTSService

logger = logging.getLogger(__name__)


class HFInferenceASR(ASRService):
    """
    ASR service using Hugging Face Inference API.
    Calls cloud-hosted Wav2Vec2/W2V-BERT models for speech recognition.
    """
    
    def __init__(self):
        """Initialize HF Inference ASR service."""
        if not HF_HUB_AVAILABLE:
            raise ImportError("huggingface_hub is required. Run: pip install huggingface_hub>=0.20")
        
        self.model_configs = settings.MODELS['asr']
        self.token = settings.HF_TOKEN
        
        if not self.token:
            logger.warning(
                "HF_TOKEN not set. HF Inference API requests may be rate-limited. "
                "Get a token from https://huggingface.co/settings/tokens"
            )
        
        # Initialize Inference Client
        self.client = InferenceClient(token=self.token)
    
    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """
        Transcribe audio file using HF Inference API.
        
        Args:
            audio_path: Path to audio file (wav, mp3, etc.)
            language: Source language code (kikuyu, swahili, english)
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        model_name = self.model_configs.get(language)
        if not model_name:
            raise ValueError(f"No ASR model configured for language: {language}")
        
        logger.info(f"Transcribing audio via HF API for {language}: {model_name}")
        
        try:
            # Read audio file as bytes
            with open(audio_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Call HF Inference API using InferenceClient
            result = self.client.automatic_speech_recognition(
                audio_data,
                model=model_name
            )
            
            # Extract text from response
            if isinstance(result, dict):
                transcribed_text = result.get('text', '')
            elif isinstance(result, str):
                transcribed_text = result
            else:
                logger.error(f"Unexpected API response format: {result}")
                transcribed_text = ""
            
            logger.info(f"ASR successful: {transcribed_text[:50]}...")
            
            return {
                "text": transcribed_text,
                "confidence": 0.95  # HF API doesn't return confidence scores
            }
            
        except Exception as e:
            logger.error(f"HF Inference API ASR error for {language}: {str(e)}")
            raise


class HFInferenceTranslator(TranslationService):
    """
    Translation service using Hugging Face Inference API.
    Calls cloud-hosted NLLB model for translation.
    """
    
    def __init__(self):
        """Initialize HF Inference translation service."""
        if not HF_HUB_AVAILABLE:
            raise ImportError("huggingface_hub is required. Run: pip install huggingface_hub>=0.20")
        
        self.model_name = settings.MODELS['translation']['model']
        self.lang_codes = settings.MODELS['translation']['lang_codes']
        self.token = settings.HF_TOKEN
        
        if not self.token:
            logger.warning(
                "HF_TOKEN not set. HF Inference API requests may be rate-limited."
            )
        
        # Initialize Inference Client
        self.client = InferenceClient(token=self.token)
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using HF Inference API.
        
        Args:
            text: Text to translate
            source_lang: Source language (kikuyu, swahili, english)
            target_lang: Target language (kikuyu, swahili, english)
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        src_code = self.lang_codes.get(source_lang)
        tgt_code = self.lang_codes.get(target_lang)
        
        if not src_code or not tgt_code:
            raise ValueError(f"Unsupported language pair: {source_lang} -> {target_lang}")
        
        logger.info(f"Translating via HF API: {source_lang} -> {target_lang}")
        
        try:
            # Call HF Inference API using InferenceClient
            result = self.client.translation(
                text,
                model=self.model_name,
                src_lang=src_code,
                tgt_lang=tgt_code
            )
            
            # Extract translated text from response
            if isinstance(result, dict):
                translated_text = result.get('translation_text', '')
            elif isinstance(result, str):
                translated_text = result
            else:
                logger.error(f"Unexpected API response format: {result}")
                translated_text = ""
            
            logger.info(f"Translation successful: {translated_text[:50]}...")
            
            return {
                "text": translated_text,
                "confidence": 0.92  # HF API doesn't return confidence scores
            }
            
        except Exception as e:
            logger.error(f"HF Inference API translation error: {str(e)}")
            raise


class HFInferenceTTS(TTSService):
    """
    Text-to-Speech service using Hugging Face Inference API.
    Calls cloud-hosted MMS-TTS models for speech synthesis.
    """
    
    def __init__(self):
        """Initialize HF Inference TTS service."""
        if not HF_HUB_AVAILABLE:
            raise ImportError("huggingface_hub is required. Run: pip install huggingface_hub>=0.20")
        
        self.model_configs = settings.MODELS['tts']
        self.token = settings.HF_TOKEN
        
        if not self.token:
            logger.warning(
                "HF_TOKEN not set. HF Inference API requests may be rate-limited."
            )
        
        # Initialize Inference Client
        self.client = InferenceClient(token=self.token)
        
        # Create temp directory for audio files
        self.temp_dir = os.path.join(settings.MEDIA_ROOT, 'tts_temp')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def synthesize(self, text: str, language: str, gender: str = "neutral") -> str:
        """
        Synthesize speech from text using HF Inference API.
        
        Args:
            text: Text to synthesize
            language: Target language code (kikuyu, swahili, english)
            gender: Voice gender preference (not used by HF API)
            
        Returns:
            str: Path to generated audio file
        """
        model_name = self.model_configs.get(language)
        if not model_name:
            raise ValueError(f"No TTS model configured for language: {language}")
        
        logger.info(f"Synthesizing speech via HF API for {language}: {text[:50]}...")
        
        try:
            # Call HF Inference API using InferenceClient
            audio_bytes = self.client.text_to_speech(
                text,
                model=model_name
            )
            
            # Save audio to file
            audio_filename = f"tts_{language}_{uuid.uuid4().hex[:8]}.flac"
            audio_path = os.path.join(self.temp_dir, audio_filename)
            
            with open(audio_path, 'wb') as audio_file:
                audio_file.write(audio_bytes)
            
            logger.info(f"TTS successful: {audio_path}")
            
            return audio_path
            
        except Exception as e:
            logger.error(f"HF Inference API TTS error for {language}: {str(e)}")
            raise
