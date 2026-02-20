"""
WebSocket consumer for real-time translation chat rooms.
"""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django_q.tasks import async_task

from .room_manager import RoomManager

logger = logging.getLogger(__name__)


class RoomConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat in translation rooms.
    """
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'room_{self.room_code}'
        self.room_manager = RoomManager()
        
        # Verify room exists
        room_exists = await sync_to_async(self.room_manager.room_exists)(self.room_code)
        
        if not room_exists:
            logger.warning(f"Connection rejected - room not found: {self.room_code}")
            await self.close(code=4004)
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept connection
        await self.accept()
        
        # Join room (increment participant count)
        room_data = await sync_to_async(self.room_manager.join_room)(self.room_code)
        
        # Send connection confirmation with room info
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'room_code': self.room_code,
            'source_lang': room_data['source_lang'],
            'target_lang': room_data['target_lang'],
            'participant_count': room_data['participants']
        }))
        
        # Send message history
        messages = await sync_to_async(self.room_manager.get_messages)(self.room_code)
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))
        
        # Notify others about new participant
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_joined',
                'participant_count': room_data['participants']
            }
        )
        
        logger.info(f"WebSocket connected to room: {self.room_code}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Decrement participant count
        room_data = await sync_to_async(self.room_manager.leave_room)(self.room_code)
        
        if room_data:
            # Notify others about participant leaving
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'participant_left',
                    'participant_count': room_data['participants']
                }
            )
        
        logger.info(f"WebSocket disconnected from room: {self.room_code} (code: {close_code})")
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'voice_message':
                await self.handle_voice_message(data)
            
            elif message_type == 'text_message':
                await self.handle_text_message(data)
            
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            
            elif message_type == 'typing':
                # Broadcast typing indicator
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_typing',
                        'is_typing': data.get('is_typing', False)
                    }
                )
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_voice_message(self, data):
        """
        Handle voice message - trigger translation pipeline.
        
        Args:
            data: Message data containing audio_data and language
        """
        message_id = data.get('message_id')
        audio_data = data.get('audio_data')  # Base64 encoded
        language = data.get('language')
        
        if not audio_data or not language:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Missing audio_data or language',
                'message_id': message_id
            }))
            return
        
        # Send processing status immediately
        await self.send(text_data=json.dumps({
            'type': 'processing',
            'message_id': message_id,
            'status': 'received'
        }))
        
        # Trigger async translation pipeline task
        await sync_to_async(async_task)(
            'translation.tasks.process_voice_message',
            self.room_code,
            audio_data,
            language,
            message_id
        )
        
        logger.info(f"Voice message queued for processing: {message_id}")
    
    async def handle_text_message(self, data):
        """
        Handle text-only message (for testing or fallback).
        
        Args:
            data: Message data containing text and language
        """
        message_id = data.get('message_id')
        text = data.get('text')
        language = data.get('language')
        
        if not text or not language:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Missing text or language'
            }))
            return
        
        # Trigger translation task without ASR
        await sync_to_async(async_task)(
            'translation.tasks.process_text_message',
            self.room_code,
            text,
            language,
            message_id
        )
    
    # Channel layer event handlers
    
    async def chat_message(self, event):
        """Broadcast chat message to WebSocket."""
        await self.send(text_data=json.dumps(event['message']))
    
    async def participant_joined(self, event):
        """Broadcast participant joined event."""
        await self.send(text_data=json.dumps({
            'type': 'participant_joined',
            'participant_count': event['participant_count']
        }))
    
    async def participant_left(self, event):
        """Broadcast participant left event."""
        await self.send(text_data=json.dumps({
            'type': 'participant_left',
            'participant_count': event['participant_count']
        }))
    
    async def user_typing(self, event):
        """Broadcast typing indicator."""
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'is_typing': event['is_typing']
        }))
    
    async def translation_progress(self, event):
        """Broadcast translation progress updates."""
        await self.send(text_data=json.dumps({
            'type': 'translation_progress',
            'message_id': event['message_id'],
            'status': event['status'],
            'progress': event.get('progress')
        }))
