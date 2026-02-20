"""
Redis-based room manager for ephemeral translation chat rooms.
No database persistence - all data stored in Redis with automatic expiry.
"""

import redis
import json
import random
import string
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class RoomManager:
    """
    Manages chat rooms using Redis for ephemeral storage.
    Rooms automatically expire after configured time period.
    """
    
    def __init__(self):
        """Initialize Redis client."""
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.room_expiry = settings.ROOM_EXPIRY_HOURS * 3600  # Convert to seconds
        self.code_length = settings.ROOM_CODE_LENGTH
        self.max_messages = settings.MAX_MESSAGES_PER_ROOM
    
    def generate_room_code(self) -> str:
        """
        Generate unique room code.
        
        Returns:
            str: Unique room code (e.g., 'ABC123')
        """
        while True:
            code = ''.join(random.choices(
                string.ascii_uppercase + string.digits,
                k=self.code_length
            ))
            if not self.redis_client.exists(f"room:{code}"):
                return code
    
    def create_room(
        self,
        source_lang: str,
        target_lang: str,
        creator_id: Optional[str] = None
    ) -> str:
        """
        Create a new chat room.
        
        Args:
            source_lang: Source language code (e.g., 'kikuyu')
            target_lang: Target language code (e.g., 'english')
            creator_id: Optional creator identifier
            
        Returns:
            str: Room code
        """
        code = self.generate_room_code()
        
        room_data = {
            'code': code,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'creator_id': creator_id,
            'participants': 0,
            'messages': [],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'last_activity': datetime.now(timezone.utc).isoformat(),
        }
        
        # Store in Redis with expiry
        self.redis_client.setex(
            f"room:{code}",
            self.room_expiry,
            json.dumps(room_data)
        )
        
        logger.info(f"Room created: {code} ({source_lang} ↔ {target_lang})")
        
        return code
    
    def join_room(self, code: str) -> Dict[str, Any]:
        """
        Join an existing room.
        
        Args:
            code: Room code
            
        Returns:
            dict: Room data
            
        Raises:
            ValueError: If room not found
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            raise ValueError(f"Room not found: {code}")
        
        room_data = json.loads(self.redis_client.get(room_key))
        room_data['participants'] += 1
        room_data['last_activity'] = datetime.now(timezone.utc).isoformat()
        
        # Update room and reset expiry
        self.redis_client.setex(
            room_key,
            self.room_expiry,
            json.dumps(room_data)
        )
        
        logger.info(f"User joined room: {code} (participants: {room_data['participants']})")
        
        return room_data
    
    def leave_room(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Leave a room (decrement participant count).
        
        Args:
            code: Room code
            
        Returns:
            dict: Updated room data, or None if room doesn't exist
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            return None
        
        room_data = json.loads(self.redis_client.get(room_key))
        room_data['participants'] = max(0, room_data['participants'] - 1)
        room_data['last_activity'] = datetime.now(timezone.utc).isoformat()
        
        # If no participants, delete room immediately
        if room_data['participants'] == 0:
            self.delete_room(code)
            logger.info(f"Room deleted (no participants): {code}")
            return None
        
        # Otherwise update room
        self.redis_client.setex(
            room_key,
            self.room_expiry,
            json.dumps(room_data)
        )
        
        logger.info(f"User left room: {code} (participants: {room_data['participants']})")
        
        return room_data
    
    def add_message(self, code: str, message: Dict[str, Any]) -> bool:
        """
        Add a message to a room.
        
        Args:
            code: Room code
            message: Message data dict
            
        Returns:
            bool: True if successful, False if room doesn't exist
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            logger.warning(f"Cannot add message - room not found: {code}")
            return False
        
        room_data = json.loads(self.redis_client.get(room_key))
        
        # Add timestamp if not present
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        # Add message to list
        room_data['messages'].append(message)
        
        # Keep only last N messages
        room_data['messages'] = room_data['messages'][-self.max_messages:]
        
        # Update last activity
        room_data['last_activity'] = datetime.now(timezone.utc).isoformat()
        
        # Save back to Redis
        self.redis_client.setex(
            room_key,
            self.room_expiry,
            json.dumps(room_data)
        )
        
        logger.info(f"Message added to room: {code} (total: {len(room_data['messages'])})")
        
        return True
    
    def get_messages(self, code: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get messages from a room.
        
        Args:
            code: Room code
            limit: Optional limit on number of messages (most recent)
            
        Returns:
            list: List of message dicts
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            logger.warning(f"Cannot get messages - room not found: {code}")
            return []
        
        room_data = json.loads(self.redis_client.get(room_key))
        messages = room_data.get('messages', [])
        
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_room(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Get room data.
        
        Args:
            code: Room code
            
        Returns:
            dict: Room data or None if not found
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            return None
        
        return json.loads(self.redis_client.get(room_key))
    
    def delete_room(self, code: str) -> bool:
        """
        Delete a room immediately.
        
        Args:
            code: Room code
            
        Returns:
            bool: True if deleted, False if room didn't exist
        """
        room_key = f"room:{code}"
        result = self.redis_client.delete(room_key)
        
        if result:
            logger.info(f"Room deleted: {code}")
        
        return bool(result)
    
    def room_exists(self, code: str) -> bool:
        """
        Check if room exists.
        
        Args:
            code: Room code
            
        Returns:
            bool: True if room exists
        """
        return self.redis_client.exists(f"room:{code}") > 0
    
    def extend_room_expiry(self, code: str) -> bool:
        """
        Extend room expiry time.
        
        Args:
            code: Room code
            
        Returns:
            bool: True if successful
        """
        room_key = f"room:{code}"
        
        if not self.redis_client.exists(room_key):
            return False
        
        # Refresh expiry time
        self.redis_client.expire(room_key, self.room_expiry)
        
        logger.debug(f"Room expiry extended: {code}")
        
        return True
