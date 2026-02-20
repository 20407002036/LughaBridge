"""
Django-Q background tasks for translation pipeline.
"""

import base64
import os
import uuid
import logging
from datetime import datetime, timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

from .services.factory import ModelFactory
from rooms.room_manager import RoomManager

logger = logging.getLogger(__name__)


def process_voice_message(room_code: str, audio_data_base64: str, language: str, message_id: str = None):
    """
    Process voice message through full translation pipeline:
    1. Decode audio from base64
    2. ASR: audio → text
    3. Translate: source text → target text
    4. TTS: target text → audio (optional)
    5. Broadcast result to room
    
    Args:
        room_code: Room code
        audio_data_base64: Base64 encoded audio data
        language: Source language code
        message_id: Optional message ID for tracking
    """
    if not message_id:
        message_id = str(uuid.uuid4())
    
    logger.info(f"Processing voice message {message_id} in room {room_code}")
    
    channel_layer = get_channel_layer()
    room_manager = RoomManager()
    
    try:
        # Get room to determine target language
        room_data = room_manager.get_room(room_code)
        if not room_data:
            logger.error(f"Room not found: {room_code}")
            return
        
        source_lang = language
        # Determine target language (swap source/target)
        if source_lang == room_data['source_lang']:
            target_lang = room_data['target_lang']
        elif source_lang == room_data['target_lang']:
            target_lang = room_data['source_lang']
        else:
            # Default to opposite of room's source language
            target_lang = room_data['target_lang'] if source_lang != room_data['target_lang'] else room_data['source_lang']
        
        # Update progress: Starting ASR
        _broadcast_progress(channel_layer, room_code, message_id, 'transcribing', 0.1)
        
        # Step 1: Decode audio
        audio_bytes = base64.b64decode(audio_data_base64)
        temp_audio_path = os.path.join(settings.MEDIA_ROOT, f"temp_audio_{uuid.uuid4()}.wav")
        os.makedirs(os.path.dirname(temp_audio_path), exist_ok=True)
        
        with open(temp_audio_path, 'wb') as f:
            f.write(audio_bytes)
        
        # Step 2: ASR - Transcribe audio
        asr_service = ModelFactory.get_asr_service()
        transcription = asr_service.transcribe(temp_audio_path, source_lang)
        
        logger.info(f"Transcription: '{transcription['text']}' (conf: {transcription['confidence']})")
        
        # Update progress: Starting translation
        _broadcast_progress(channel_layer, room_code, message_id, 'translating', 0.5)
        
        # Step 3: Translate text
        translator = ModelFactory.get_translation_service()
        translation = translator.translate(
            transcription['text'],
            source_lang,
            target_lang
        )
        
        logger.info(f"Translation: '{translation['text']}' (conf: {translation['confidence']})")
        
        # Update progress: Starting TTS
        _broadcast_progress(channel_layer, room_code, message_id, 'synthesizing', 0.8)
        
        # Step 4: TTS - Generate audio (optional, can skip for efficiency)
        tts_service = ModelFactory.get_tts_service()
        audio_path = tts_service.synthesize(translation['text'], target_lang)
        
        # Convert audio to base64
        with open(audio_path, 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode()
        
        # Create message object
        message = {
            'id': message_id,
            'type': 'translation_complete',
            'original_text': transcription['text'],
            'original_language': source_lang,
            'translated_text': translation['text'],
            'translated_language': target_lang,
            'stt_confidence': transcription['confidence'],
            'translation_confidence': translation['confidence'],
            'audio_data': audio_base64,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        
        # Store message in Redis
        room_manager.add_message(room_code, message)
        
        # Broadcast to all participants in room
        async_to_sync(channel_layer.group_send)(
            f'room_{room_code}',
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
        # Cleanup temp files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        logger.info(f"Voice message processed successfully: {message_id}")
    
    except Exception as e:
        logger.error(f"Error processing voice message {message_id}: {str(e)}", exc_info=True)
        
        # Broadcast error to room
        async_to_sync(channel_layer.group_send)(
            f'room_{room_code}',
            {
                'type': 'chat_message',
                'message': {
                    'type': 'translation_error',
                    'message_id': message_id,
                    'error': str(e),
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                }
            }
        )


def process_text_message(room_code: str, text: str, language: str, message_id: str = None):
    """
    Process text-only message (no ASR, no TTS).
    Useful for testing or fallback mode.
    
    Args:
        room_code: Room code
        text: Text to translate
        language: Source language
        message_id: Optional message ID
    """
    if not message_id:
        message_id = str(uuid.uuid4())
    
    logger.info(f"Processing text message {message_id} in room {room_code}")
    
    channel_layer = get_channel_layer()
    room_manager = RoomManager()
    
    try:
        # Get room to determine target language
        room_data = room_manager.get_room(room_code)
        if not room_data:
            logger.error(f"Room not found: {room_code}")
            return
        
        source_lang = language
        if source_lang == room_data['source_lang']:
            target_lang = room_data['target_lang']
        else:
            target_lang = room_data['source_lang']
        
        # Translate
        translator = ModelFactory.get_translation_service()
        translation = translator.translate(text, source_lang, target_lang)
        
        # Create message
        message = {
            'id': message_id,
            'type': 'translation_complete',
            'original_text': text,
            'original_language': source_lang,
            'translated_text': translation['text'],
            'translated_language': target_lang,
            'stt_confidence': 1.0,  # Perfect confidence for text input
            'translation_confidence': translation['confidence'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        
        # Store and broadcast
        room_manager.add_message(room_code, message)
        
        async_to_sync(channel_layer.group_send)(
            f'room_{room_code}',
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
        logger.info(f"Text message processed successfully: {message_id}")
    
    except Exception as e:
        logger.error(f"Error processing text message {message_id}: {str(e)}", exc_info=True)


def _broadcast_progress(channel_layer, room_code: str, message_id: str, status: str, progress: float):
    """
    Broadcast translation progress update.
    
    Args:
        channel_layer: Channels layer instance
        room_code: Room code
        message_id: Message ID
        status: Status string (transcribing, translating, synthesizing)
        progress: Progress value 0.0-1.0
    """
    async_to_sync(channel_layer.group_send)(
        f'room_{room_code}',
        {
            'type': 'translation_progress',
            'message_id': message_id,
            'status': status,
            'progress': progress
        }
    )
