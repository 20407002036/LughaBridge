"""
Service factory for creating ASR, Translation, and TTS services.
Supports three modes:
- Demo mode: Mock services with simulated responses
- HF Inference API mode: Cloud-hosted models via Hugging Face API
- Local mode: Self-hosted models loaded locally
"""

from django.conf import settings
import logging

from .base import ASRService, TranslationService, TTSService
from .huggingface_asr import HuggingFaceASR
from .nllb_translator import NLLBTranslator
from .mms_tts import MMSTTS
from .mock_services import MockASR, MockTranslator, MockTTS
from .hf_inference_services import HFInferenceASR, HFInferenceTranslator, HFInferenceTTS
from .hybrid_translator import HybridTranslator

logger = logging.getLogger(__name__)


class ModelFactory:
    """
    Factory for creating translation pipeline services.
    Singleton pattern ensures models are loaded only once.
    """
    
    # Local model instances
    _asr_service = None
    _translation_service = None
    _tts_service = None
    
    # HF Inference API instances
    _hf_asr_service = None
    _hf_translation_service = None
    _hf_tts_service = None
    
    # Hybrid translator (HF + Groq)
    _hybrid_translator = None
    
    # Mock instances
    _mock_asr = None
    _mock_translator = None
    _mock_tts = None
    
    @classmethod
    def get_asr_service(cls, use_demo: bool = None, use_hf_inference: bool = None) -> ASRService:
        """
        Get ASR service instance.
        
        Args:
            use_demo: Override demo mode setting. If None, uses settings.DEMO_MODE
            use_hf_inference: Override HF Inference mode. If None, uses settings.USE_HF_INFERENCE
            
        Returns:
            ASRService instance (MockASR, HFInferenceASR, or HuggingFaceASR)
        """
        demo_mode = use_demo if use_demo is not None else settings.DEMO_MODE
        hf_mode = use_hf_inference if use_hf_inference is not None else settings.USE_HF_INFERENCE
        
        if demo_mode:
            if cls._mock_asr is None:
                logger.info("Creating MockASR service (demo mode)")
                cls._mock_asr = MockASR()
            return cls._mock_asr
        elif hf_mode:
            if cls._hf_asr_service is None:
                logger.info("Creating HFInferenceASR service (HF Inference API mode)")
                cls._hf_asr_service = HFInferenceASR()
            return cls._hf_asr_service
        else:
            if cls._asr_service is None:
                logger.info("Creating HuggingFaceASR service (local model mode)")
                cls._asr_service = HuggingFaceASR()
            return cls._asr_service
    
    @classmethod
    def get_translation_service(cls, use_demo: bool = None, use_hf_inference: bool = None) -> TranslationService:
        """
        Get translation service instance.
        
        Args:
            use_demo: Override demo mode setting. If None, uses settings.DEMO_MODE
            use_hf_inference: Override HF Inference mode. If None, uses settings.USE_HF_INFERENCE
            
        Returns:
            TranslationService instance (MockTranslator, HybridTranslator, HFInferenceTranslator, or NLLBTranslator)
        """
        demo_mode = use_demo if use_demo is not None else settings.DEMO_MODE
        hf_mode = use_hf_inference if use_hf_inference is not None else settings.USE_HF_INFERENCE
        
        if demo_mode:
            if cls._mock_translator is None:
                logger.info("Creating MockTranslator service (demo mode)")
                cls._mock_translator = MockTranslator()
            return cls._mock_translator
        elif hf_mode:
            # Use HybridTranslator when in HF mode (it handles Groq + HF routing)
            if cls._hybrid_translator is None:
                logger.info("Creating HybridTranslator service (intelligent routing: Groq for Swahili, HF for Kikuyu)")
                cls._hybrid_translator = HybridTranslator()
            return cls._hybrid_translator
        else:
            if cls._translation_service is None:
                logger.info("Creating NLLBTranslator service (local model mode)")
                cls._translation_service = NLLBTranslator()
            return cls._translation_service
    
    @classmethod
    def get_tts_service(cls, use_demo: bool = None, use_hf_inference: bool = None) -> TTSService:
        """
        Get TTS service instance.
        
        Args:
            use_demo: Override demo mode setting. If None, uses settings.DEMO_MODE
            use_hf_inference: Override HF Inference mode. If None, uses settings.USE_HF_INFERENCE
            
        Returns:
            TTSService instance (MockTTS, HFInferenceTTS, or MMSTTS)
        """
        demo_mode = use_demo if use_demo is not None else settings.DEMO_MODE
        hf_mode = use_hf_inference if use_hf_inference is not None else settings.USE_HF_INFERENCE
        
        if demo_mode:
            if cls._mock_tts is None:
                logger.info("Creating MockTTS service (demo mode)")
                cls._mock_tts = MockTTS()
            return cls._mock_tts
        elif hf_mode:
            if cls._hf_tts_service is None:
                logger.info("Creating HFInferenceTTS service (HF Inference API mode)")
                cls._hf_tts_service = HFInferenceTTS()
            return cls._hf_tts_service
        else:
            if cls._tts_service is None:
                logger.info("Creating MMSTTS service (local model mode)")
                cls._tts_service = MMSTTS()
            return cls._tts_service
    
    @classmethod
    def reset_services(cls):
        """Reset all service instances (useful for testing)."""
        cls._asr_service = None
        cls._translation_service = None
        cls._tts_service = None
        cls._hf_asr_service = None
        cls._hf_translation_service = None
        cls._hf_tts_service = None
        cls._hybrid_translator = None
        cls._mock_asr = None
        cls._mock_translator = None
        cls._mock_tts = None
        logger.info("All service instances reset")
