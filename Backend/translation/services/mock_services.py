"""
Mock services for demo mode - no actual ML models required.
"""

import time
import random
import os
import uuid
from typing import Dict, Any
from django.conf import settings
import logging

from .base import ASRService, TranslationService, TTSService

logger = logging.getLogger(__name__)


class MockASR(ASRService):
    """Mock ASR service with predefined transcriptions."""
    
    DEMO_PHRASES = {
        'kikuyu': [
            "Wĩ mwega?",
            "Nĩ wega, nĩ waku?",
            "Nĩ wega mũno",
            "Rĩĩtwa rĩaku nĩ atĩa?",
            "Nĩ wega gũkũona",
        ],
        'english': [
            "How are you?",
            "I'm fine, and you?",
            "I'm very well",
            "What is your name?",
            "Nice to meet you",
        ],
        'swahili': [
            "Habari yako?",
            "Mzuri, wewe je?",
            "Mzuri sana",
            "Jina lako ni nani?",
            "Nimefurahi kukujua",
        ]
    }
    
    def __init__(self):
        self.counter = 0
    
    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """Return predefined transcription with simulated delay."""
        # Simulate processing time
        time.sleep(random.uniform(0.5, 1.5))
        
        phrases = self.DEMO_PHRASES.get(language, self.DEMO_PHRASES['english'])
        phrase = phrases[self.counter % len(phrases)]
        self.counter += 1
        
        confidence = random.uniform(0.85, 0.98)
        
        logger.info(f"[DEMO] Mock transcription ({language}): {phrase}")
        
        return {
            "text": phrase,
            "confidence": round(confidence, 3)
        }


class MockTranslator(TranslationService):
    """Mock translator with predefined translations."""
    
    TRANSLATIONS = {
        ('kikuyu', 'english'): {
            "Wĩ mwega?": "How are you?",
            "Nĩ wega, nĩ waku?": "I'm fine, and you?",
            "Nĩ wega mũno": "I'm very well",
            "Rĩĩtwa rĩaku nĩ atĩa?": "What is your name?",
            "Nĩ wega gũkũona": "Nice to meet you",
        },
        ('english', 'kikuyu'): {
            "How are you?": "Wĩ mwega?",
            "I'm fine, and you?": "Nĩ wega, nĩ waku?",
            "I'm very well": "Nĩ wega mũno",
            "What is your name?": "Rĩĩtwa rĩaku nĩ atĩa?",
            "Nice to meet you": "Nĩ wega gũkũona",
        },
        ('swahili', 'english'): {
            "Habari yako?": "How are you?",
            "Mzuri, wewe je?": "I'm fine, and you?",
            "Mzuri sana": "I'm very well",
            "Jina lako ni nani?": "What is your name?",
            "Nimefurahi kukujua": "Nice to meet you",
        },
        ('english', 'swahili'): {
            "How are you?": "Habari yako?",
            "I'm fine, and you?": "Mzuri, wewe je?",
            "I'm very well": "Mzuri sana",
            "What is your name?": "Jina lako ni nani?",
            "Nice to meet you": "Nimefurahi kukujua",
        }
    }
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """Return predefined translation with simulated delay."""
        # Simulate processing time
        time.sleep(random.uniform(0.3, 0.8))
        
        translation_dict = self.TRANSLATIONS.get((source_lang, target_lang), {})
        translation = translation_dict.get(text, f"[Mock translation of: {text}]")
        
        confidence = random.uniform(0.88, 0.97)
        
        logger.info(f"[DEMO] Mock translation ({source_lang}->{target_lang}): {translation}")
        
        return {
            "text": translation,
            "confidence": round(confidence, 3)
        }


class MockTTS(TTSService):
    """Mock TTS service - returns empty audio file."""
    
    def __init__(self):
        # Create temp directory for mock audio
        self.temp_dir = os.path.join(settings.MEDIA_ROOT, 'mock_tts')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def synthesize(self, text: str, language: str, gender: str = "neutral") -> str:
        """Return path to mock audio file."""
        # Simulate processing time
        time.sleep(random.uniform(0.4, 0.9))
        
        # Create empty mock audio file
        audio_filename = f"mock_tts_{uuid.uuid4().hex}.wav"
        audio_path = os.path.join(self.temp_dir, audio_filename)
        
        # Create minimal valid WAV file (silence)
        # WAV header for 1 second of silence at 16kHz, mono, 16-bit
        with open(audio_path, 'wb') as f:
            # RIFF header
            f.write(b'RIFF')
            f.write((36 + 16000 * 2).to_bytes(4, 'little'))  # File size - 8
            f.write(b'WAVE')
            
            # Format chunk
            f.write(b'fmt ')
            f.write((16).to_bytes(4, 'little'))  # Chunk size
            f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
            f.write((1).to_bytes(2, 'little'))   # Channels (mono)
            f.write((16000).to_bytes(4, 'little'))  # Sample rate
            f.write((32000).to_bytes(4, 'little'))  # Byte rate
            f.write((2).to_bytes(2, 'little'))   # Block align
            f.write((16).to_bytes(2, 'little'))  # Bits per sample
            
            # Data chunk
            f.write(b'data')
            f.write((16000 * 2).to_bytes(4, 'little'))  # Data size
            f.write(bytes(16000 * 2))  # Silence (zeros)
        
        logger.info(f"[DEMO] Mock TTS generated: {audio_path}")
        
        return audio_path
