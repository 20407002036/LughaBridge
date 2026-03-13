"""
Hybrid translation service that intelligently routes translations.
Uses Groq as primary (fast, free) with HF NLLB as fallback.
Routing is configurable via .env settings.
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
    Hybrid translator that routes translation requests:
    - When USE_GROQ_TRANSLATION=True: Groq primary for ALL languages, HF fallback
    - When USE_GROQ_TRANSLATION=False: HF primary, Groq fallback for Swahili only
    """
    
    def __init__(self):
        """Initialize hybrid translator with both Groq and HF."""
        self.groq_available = bool(getattr(settings, 'GROQ_API_KEY', '').strip())
        self.hf_available = bool(getattr(settings, 'HF_TOKEN', '').strip())
        self.groq_primary = getattr(settings, 'USE_GROQ_TRANSLATION', False)

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
                "Set either GROQ_API_KEY or HF_TOKEN in .env."
            )

        if self.groq_primary and self.groq_available:
            logger.info("Hybrid translator: Groq is PRIMARY for all languages")
        else:
            logger.info("Hybrid translator: HF is primary, Groq fallback for Swahili")

    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using the best available service.
        
        Routing when USE_GROQ_TRANSLATION=True:
            All languages → Groq first, HF fallback
        Routing when USE_GROQ_TRANSLATION=False:
            Swahili → Groq first, HF fallback
            Kikuyu  → HF first, Groq fallback
            Other   → HF first, Groq fallback
        """
        primary, fallback = self._pick_services(source_lang, target_lang)

        # Try primary service
        primary_error = None
        try:
            name, service = primary
            logger.info(f"Using {name} for {source_lang} -> {target_lang}")
            result = service.translate(text, source_lang, target_lang)
            result['service_used'] = name.lower()
            return result
        except Exception as e:
            primary_error = e
            logger.warning(f"{primary[0]} translation failed: {e}. Trying fallback...")

        # Try fallback
        if fallback:
            try:
                name, service = fallback
                logger.info(f"Using fallback {name} for {source_lang} -> {target_lang}")
                result = service.translate(text, source_lang, target_lang)
                result['service_used'] = name.lower()
                result['fallback'] = True
                return result
            except Exception as fallback_err:
                logger.error(f"Fallback {fallback[0]} also failed: {fallback_err}")
                raise RuntimeError(
                    f"Both translation services failed. "
                    f"Primary ({primary[0]}): {primary_error}. "
                    f"Fallback ({fallback[0]}): {fallback_err}"
                )

        # No fallback available
        raise primary_error

    def _pick_services(self, source_lang: str, target_lang: str):
        """Return (primary, fallback) tuples of (name, service)."""
        is_swahili = source_lang == 'swahili' or target_lang == 'swahili'

        if self.groq_primary and self.groq_available:
            # Groq primary for everything
            primary = ('Groq', self.groq_translator)
            fallback = ('HF', self.hf_translator) if self.hf_available else None
        elif is_swahili and self.groq_available:
            # Legacy mode: Groq for Swahili only
            primary = ('Groq', self.groq_translator)
            fallback = ('HF', self.hf_translator) if self.hf_available else None
        elif self.hf_available:
            primary = ('HF', self.hf_translator)
            fallback = ('Groq', self.groq_translator) if self.groq_available else None
        elif self.groq_available:
            primary = ('Groq', self.groq_translator)
            fallback = None
        else:
            raise RuntimeError("No translation service available")

        return primary, fallback

