"""
Hybrid translation service that intelligently routes translations.
Uses Groq for Swahili (fast & free) and HF for Kikuyu (better quality).
"""

import logging
from typing import Dict, Any
from django.conf import settings

from .base import TranslationService
from .groq_translator import GroqTranslator
from .hf_inference_services import HFInferenceTranslator

logger = logging.getLogger(__name__)


class HybridTranslator(TranslationService):
    """
    Hybrid translator that intelligently routes translation requests:
    - Swahili ↔ English: Use Groq (faster, still accurate)
    - Kikuyu ↔ English: Use HF NLLB (trained on Kikuyu data)
    - Fallback: If primary service fails, try the other
    """
    
    def __init__(self):
        """Initialize hybrid translator with both Groq and HF."""
        # Check for non-empty API keys (empty strings should be treated as unavailable)
        self.groq_available = bool(getattr(settings, 'GROQ_API_KEY', '').strip())
        self.hf_available = bool(getattr(settings, 'HF_TOKEN', '').strip())
        
        # Initialize services
        self.groq_translator = None
        self.hf_translator = None
        
        if self.groq_available:
            try:
                self.groq_translator = GroqTranslator()
                logger.info("Groq translator initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq translator: {e}")
                self.groq_available = False
        
        if self.hf_available:
            try:
                self.hf_translator = HFInferenceTranslator()
                logger.info("HF Inference translator initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize HF translator: {e}")
                self.hf_available = False
        
        if not self.groq_available and not self.hf_available:
            raise RuntimeError(
                "No translation services available. "
                "Set either GROQ_API_KEY or HF_TOKEN in environment."
            )
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using the best available service.
        
        Routing strategy:
        1. Swahili translations → Try Groq first, fallback to HF
        2. Kikuyu translations → Try HF first, fallback to Groq
        3. If one service fails, automatically try the other
        
        Args:
            text: Text to translate
            source_lang: Source language (kikuyu, swahili, english)
            target_lang: Target language (kikuyu, swahili, english)
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        # Determine which service to use based on language
        is_swahili = source_lang == 'swahili' or target_lang == 'swahili'
        is_kikuyu = source_lang == 'kikuyu' or target_lang == 'kikuyu'
        
        # Choose primary and fallback services
        if is_swahili and self.groq_available:
            primary_service = ('Groq', self.groq_translator)
            fallback_service = ('HF', self.hf_translator) if self.hf_available else None
        elif is_kikuyu and self.hf_available:
            primary_service = ('HF', self.hf_translator)
            fallback_service = ('Groq', self.groq_translator) if self.groq_available else None
        elif self.hf_available:
            # Default to HF for better quality
            primary_service = ('HF', self.hf_translator)
            fallback_service = ('Groq', self.groq_translator) if self.groq_available else None
        elif self.groq_available:
            # Use Groq if HF not available
            primary_service = ('Groq', self.groq_translator)
            fallback_service = None
        else:
            raise RuntimeError("No translation service available")
        
        # Try primary service
        try:
            service_name, service = primary_service
            logger.info(f"Using {service_name} for {source_lang} -> {target_lang} translation")
            result = service.translate(text, source_lang, target_lang)
            
            # Add metadata about which service was used
            result['service_used'] = service_name.lower()
            return result
            
        except Exception as e:
            logger.warning(
                f"{primary_service[0]} translation failed: {str(e)}. "
                f"Trying fallback service..."
            )
            
            # Try fallback service if available
            if fallback_service:
                try:
                    service_name, service = fallback_service
                    logger.info(f"Using fallback {service_name} for translation")
                    result = service.translate(text, source_lang, target_lang)
                    
                    # Add metadata
                    result['service_used'] = service_name.lower()
                    result['fallback'] = True
                    return result
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback {fallback_service[0]} also failed: {fallback_error}")
                    raise Exception(
                        f"Both translation services failed. "
                        f"Primary ({primary_service[0]}): {e}. "
                        f"Fallback ({fallback_service[0]}): {fallback_error}"
                    )
            else:
                # No fallback available
                logger.error(f"Translation failed and no fallback available: {e}")
                raise
