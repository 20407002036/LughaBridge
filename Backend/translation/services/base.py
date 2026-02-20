"""
Base service interfaces for LughaBridge translation pipeline.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ASRService(ABC):
    """Abstract base class for Automatic Speech Recognition services."""
    
    @abstractmethod
    def transcribe(self, audio_path: str, language: str) -> Dict[str, Any]:
        """
        Transcribe audio to text.
        
        Args:
            audio_path: Path to audio file
            language: Source language code (e.g., 'kikuyu', 'english')
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        pass


class TranslationService(ABC):
    """Abstract base class for translation services."""
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            dict: {"text": str, "confidence": float}
        """
        pass


class TTSService(ABC):
    """Abstract base class for Text-to-Speech services."""
    
    @abstractmethod
    def synthesize(self, text: str, language: str, gender: str = "neutral") -> str:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            language: Target language code
            gender: Voice gender preference (male/female/neutral)
            
        Returns:
            str: Path to generated audio file
        """
        pass
