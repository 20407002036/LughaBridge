"""
REST API views for room management.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

from .room_manager import RoomManager

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_room(request):
    """
    Create a new translation chat room.
    
    POST /api/rooms/create/
    
    Request body:
    {
        "source_lang": "kikuyu",  # Optional, default: kikuyu
        "target_lang": "english"  # Optional, default: english
    }
    
    Response:
    {
        "room_code": "ABC123",
        "source_lang": "kikuyu",
        "target_lang": "english",
        "ws_url": "ws://localhost:8000/ws/room/ABC123/"
    }
    """
    source_lang = request.data.get('source_lang', 'kikuyu')
    target_lang = request.data.get('target_lang', 'english')
    
    # Validate languages
    supported_langs = settings.SUPPORTED_LANGUAGES
    if source_lang not in supported_langs or target_lang not in supported_langs:
        return Response(
            {
                'error': f'Unsupported language. Supported: {", ".join(supported_langs)}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if source_lang == target_lang:
        return Response(
            {'error': 'Source and target languages must be different'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        manager = RoomManager()
        room_code = manager.create_room(source_lang, target_lang)
        
        # Build WebSocket URL
        ws_url = f"ws://{request.get_host()}/ws/room/{room_code}/"
        
        logger.info(f"Room created via API: {room_code}")
        
        return Response(
            {
                'room_code': room_code,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'ws_url': ws_url,
                'expiry_hours': settings.ROOM_EXPIRY_HOURS
            },
            status=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        logger.error(f"Error creating room: {str(e)}")
        return Response(
            {'error': 'Failed to create room'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def join_room(request, room_code):
    """
    Get room information before joining.
    
    GET /api/rooms/{room_code}/join/
    
    Response:
    {
        "room_code": "ABC123",
        "source_lang": "kikuyu",
        "target_lang": "english",
        "participants": 1,
        "created_at": "2026-02-19T...",
        "ws_url": "ws://localhost:8000/ws/room/ABC123/"
    }
    """
    manager = RoomManager()
    
    try:
        room_data = manager.get_room(room_code)
        
        if not room_data:
            return Response(
                {'error': 'Room not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Build WebSocket URL
        ws_url = f"ws://{request.get_host()}/ws/room/{room_code}/"
        
        return Response(
            {
                'room_code': room_data['code'],
                'source_lang': room_data['source_lang'],
                'target_lang': room_data['target_lang'],
                'participants': room_data['participants'],
                'created_at': room_data['created_at'],
                'last_activity': room_data['last_activity'],
                'ws_url': ws_url
            },
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.error(f"Error getting room {room_code}: {str(e)}")
        return Response(
            {'error': 'Failed to get room information'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_messages(request, room_code):
    """
    Get message history for a room.
    
    GET /api/rooms/{room_code}/messages/?limit=50
    
    Response:
    {
        "room_code": "ABC123",
        "messages": [
            {
                "id": "msg-uuid",
                "original_text": "Wĩ mwega?",
                "original_language": "kikuyu",
                "translated_text": "How are you?",
                "translated_language": "english",
                "timestamp": "2026-02-19T..."
            },
            ...
        ]
    }
    """
    limit = request.query_params.get('limit', 100)
    
    try:
        limit = int(limit)
        if limit < 1 or limit > 500:
            limit = 100
    except ValueError:
        limit = 100
    
    manager = RoomManager()
    
    if not manager.room_exists(room_code):
        return Response(
            {'error': 'Room not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        messages = manager.get_messages(room_code, limit=limit)
        
        return Response(
            {
                'room_code': room_code,
                'message_count': len(messages),
                'messages': messages
            },
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.error(f"Error getting messages for room {room_code}: {str(e)}")
        return Response(
            {'error': 'Failed to get messages'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint.
    
    GET /api/health/
    """
    return Response(
        {
            'status': 'healthy',
            'demo_mode': settings.DEMO_MODE,
            'use_hf_inference': settings.USE_HF_INFERENCE,
            'supported_languages': settings.SUPPORTED_LANGUAGES
        },
        status=status.HTTP_200_OK
    )
