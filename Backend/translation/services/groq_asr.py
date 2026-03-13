"""
Groq API ASR service implementation.
Uses Groq's hosted Whisper models for fast speech recognition.
"""

import logging
import requests
from typing import Dict, Any
from django.conf import settings

from .base import ASRService

logger = logging.getLogger(__name__)


class GroqASR(ASRService):
    """
    ASR service using Groq's hosted Whisper API.
    Fast and reliable – supports all languages via whisper-large-v3.
    """

    API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

    def __init__(self):
        """Initialize Groq ASR service."""
        self.api_key = settings.GROQ_API_KEY
        self.model = getattr(settings, 'GROQ_ASR_MODEL', 'whisper-large-v3')

        if not self.api_key or not self.api_key.strip():
            raise ValueError(
                "GROQ_API_KEY not set. Get a free key from https://console.groq.com/keys"
            )

    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Groq's Whisper API.

        Args:
            audio_path: Path to audio file (wav, mp3, etc.)
            language: Source language code (kikuyu, swahili, english)

        Returns:
            dict: {"text": str, "confidence": float}
        """
        # Map internal language codes to ISO 639-1 for Whisper
        # Only include languages Groq/Whisper actually supports.
        # Unsupported languages (e.g. Kikuyu) are omitted so Whisper auto-detects.
        lang_map = {
            'english': 'en',
            'swahili': 'sw',
        }
        whisper_lang = lang_map.get(language)

        logger.info(f"Transcribing audio via Groq Whisper ({self.model}) for {language}")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            with open(audio_path, 'rb') as audio_file:
                files = {
                    'file': (audio_path.split('/')[-1], audio_file, 'audio/wav'),
                }
                data = {
                    'model': self.model,
                    'response_format': 'verbose_json',
                }
                # Only send language hint if we have a mapping
                if whisper_lang:
                    data['language'] = whisper_lang

                response = requests.post(
                    self.API_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30,
                )

            if response.status_code == 200:
                result = response.json()
                transcribed_text = result.get('text', '').strip()

                # Groq's verbose_json may include segments with avg_logprob
                segments = result.get('segments', [])
                if segments:
                    avg_logprobs = [s.get('avg_logprob', -1.0) for s in segments]
                    # Convert avg log-prob to a rough confidence (0-1)
                    import math
                    avg_logprob = sum(avg_logprobs) / len(avg_logprobs)
                    confidence = min(1.0, max(0.0, math.exp(avg_logprob)))
                else:
                    confidence = 0.90

                logger.info(f"Groq ASR successful: {transcribed_text[:50]}... (conf: {confidence:.2f})")

                return {
                    "text": transcribed_text,
                    "confidence": round(confidence, 3),
                }

            elif response.status_code == 429:
                logger.error("Groq API rate limit exceeded for ASR")
                raise RuntimeError(
                    "Groq rate limit exceeded. Wait a moment or upgrade your plan."
                )

            elif response.status_code == 401:
                logger.error("Groq API authentication failed for ASR")
                raise RuntimeError(
                    "Invalid GROQ_API_KEY. Get one from https://console.groq.com/keys"
                )

            else:
                body = response.text[:500]
                logger.error(f"Groq ASR API error {response.status_code}: {body}")
                raise RuntimeError(f"Groq ASR API error {response.status_code}: {body}")

        except requests.exceptions.Timeout:
            logger.error("Groq ASR API request timed out")
            raise RuntimeError("Groq ASR request timed out after 30s")

        except RuntimeError:
            raise  # Re-raise our own errors

        except Exception as e:
            logger.error(f"Groq ASR error: {str(e)}")
            raise
