"""
Groq API translation service implementation.
Uses Groq's LLM API for fast, free translation (best for Swahili).
"""

import requests
import logging
from typing import Dict, Any
from django.conf import settings

from .base import TranslationService

logger = logging.getLogger(__name__)


class GroqTranslator(TranslationService):
    """
    Translation service using Groq's LLM API.
    Best for Swahili translation - fast and free (30 req/min).
    For Kikuyu, prefer NLLB model (better quality).
    """
    
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        """Initialize Groq translator."""
        self.api_key = settings.GROQ_API_KEY
        self.model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
        
        if not self.api_key or not self.api_key.strip():
            logger.warning(
                "GROQ_API_KEY not set. Groq disabled for Swahili translation. "
                "Get a free API key from https://console.groq.com/keys (30 req/min free tier). "
                "System will fall back to HuggingFace for all translations."
            )
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using Groq's LLM API.
        
        Args:
            text: Text to translate
            source_lang: Source language (kikuyu, swahili, english)
            target_lang: Target language (kikuyu, swahili, english)
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not configured")
        
        logger.info(f"Translating via Groq API: {source_lang} -> {target_lang}")
        
        # Create translation prompt
        system_prompt = self._create_system_prompt(source_lang, target_lang)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 0.1,  # Low temperature for consistent translation
                "max_tokens": 1024
            }
            
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['choices'][0]['message']['content'].strip()
                
                # Remove any markdown or explanations
                translated_text = self._clean_translation(translated_text)
                
                logger.info(f"Groq translation successful: {translated_text[:50]}...")
                
                return {
                    "text": translated_text,
                    "confidence": 0.90  # Groq doesn't provide confidence scores
                }
            
            elif response.status_code == 429:
                logger.error("Groq API rate limit exceeded")
                raise Exception(
                    "Groq rate limit exceeded (30 req/min on free tier). "
                    "Wait a moment or upgrade your plan."
                )
            
            elif response.status_code == 401:
                logger.error("Groq API authentication failed")
                raise Exception(
                    "Invalid GROQ_API_KEY. Get one from https://console.groq.com/keys"
                )
            
            else:
                logger.error(f"Groq API error {response.status_code}: {response.text}")
                raise Exception(f"Groq API error: {response.text}")
            
        except requests.exceptions.Timeout:
            logger.error("Groq API request timed out")
            raise Exception("Groq API request timed out after 30 seconds")
        
        except Exception as e:
            logger.error(f"Groq translation error: {str(e)}")
            raise
    
    def _create_system_prompt(self, source_lang: str, target_lang: str) -> str:
        """
        Create system prompt for translation.
        
        Args:
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            str: System prompt
        """
        # Language name mapping
        lang_names = {
            'kikuyu': 'Kikuyu (Gikuyu)',
            'swahili': 'Swahili (Kiswahili)',
            'english': 'English'
        }
        
        src_name = lang_names.get(source_lang, source_lang.title())
        tgt_name = lang_names.get(target_lang, target_lang.title())
        
        return (
            f"You are a professional translator specializing in {src_name} to {tgt_name} translation. "
            f"Translate the following text from {src_name} to {tgt_name}. "
            f"Provide ONLY the translation without any explanations, notes, or additional text. "
            f"Preserve the tone and meaning of the original text. "
            f"Do not add quotation marks around the translation."
        )
    
    def _clean_translation(self, text: str) -> str:
        """
        Clean translation output from LLM.
        
        Args:
            text: Raw translation from LLM
            
        Returns:
            str: Cleaned translation
        """
        # Remove common prefixes/suffixes added by LLMs
        prefixes_to_remove = [
            "Translation: ",
            "Here is the translation: ",
            "The translation is: ",
        ]
        
        for prefix in prefixes_to_remove:
            if text.startswith(prefix):
                text = text[len(prefix):]
        
        # Remove surrounding quotes if present
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith("'") and text.endswith("'")):
            text = text[1:-1]
        
        return text.strip()
