"""
NLLB (No Language Left Behind) translation service implementation.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from django.conf import settings
from typing import Dict, Any
import logging

from .base import TranslationService

logger = logging.getLogger(__name__)


class NLLBTranslator(TranslationService):
    """
    Translation service using Meta's NLLB model.
    Supports 200+ languages including Kikuyu, Swahili, and English.
    """
    
    def __init__(self):
        """Initialize NLLB translator."""
        self.model = None
        self.tokenizer = None
        self.model_name = settings.MODELS['translation']['model']
        self.lang_codes = settings.MODELS['translation']['lang_codes']
        
    def _load_model(self):
        """Lazy load NLLB model."""
        if self.model is None:
            logger.info(f"Loading NLLB translation model: {self.model_name}")
            
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    cache_dir=settings.HF_CACHE_DIR,
                    src_lang=self.lang_codes['english'],  # Default source
                    use_fast=False  # Force slow tokenizer which has lang_code_to_id
                )
                
                self.model = AutoModelForSeq2SeqLM.from_pretrained(
                    self.model_name,
                    cache_dir=settings.HF_CACHE_DIR
                )
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.model = self.model.cuda()
                    logger.info("NLLB model loaded on GPU")
                else:
                    logger.info("NLLB model loaded on CPU")
                    
            except Exception as e:
                logger.error(f"Error loading NLLB model: {str(e)}")
                raise
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using NLLB model.
        
        Args:
            text: Text to translate
            source_lang: Source language (kikuyu, swahili, english)
            target_lang: Target language (kikuyu, swahili, english)
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Get NLLB language codes
            src_code = self.lang_codes.get(source_lang)
            tgt_code = self.lang_codes.get(target_lang)
            
            if not src_code or not tgt_code:
                raise ValueError(f"Unsupported language pair: {source_lang} -> {target_lang}")
            
            logger.info(f"Translating from {source_lang} to {target_lang}")
            
            # Set source language
            self.tokenizer.src_lang = src_code
            
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Get forced_bos_token_id (handles both old and new tokenizer APIs)
            if hasattr(self.tokenizer, 'lang_code_to_id'):
                forced_bos_token_id = self.tokenizer.lang_code_to_id[tgt_code]
            elif hasattr(self.tokenizer, 'convert_tokens_to_ids'):
                forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_code)
            else:
                forced_bos_token_id = self.tokenizer.get_lang_id(tgt_code)
            
            # Generate translation
            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=forced_bos_token_id,
                    max_length=512,
                    num_beams=5,
                    early_stopping=True,
                    return_dict_in_generate=True,
                    output_scores=True
                )
            
            # Decode translation
            translation = self.tokenizer.batch_decode(
                generated_tokens.sequences,
                skip_special_tokens=True
            )[0]
            
            # Calculate confidence score from generation scores
            # This is a simplified confidence based on sequence scores
            if hasattr(generated_tokens, 'sequences_scores'):
                confidence = float(torch.exp(generated_tokens.sequences_scores[0]).cpu())
            else:
                confidence = 0.95  # Default confidence if scores not available
            
            # Clamp confidence to reasonable range
            confidence = min(max(confidence, 0.5), 0.99)
            
            logger.info(f"Translation result: {translation[:50]}... (conf: {confidence:.2f})")
            
            return {
                "text": translation.strip(),
                "confidence": round(confidence, 3)
            }
            
        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            raise RuntimeError(f"Translation failed: {str(e)}")
