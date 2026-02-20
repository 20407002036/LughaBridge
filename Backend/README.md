# LughaBridge Backend

Real-time Kikuyu ↔ English translation chat API using Django Channels and Hugging Face models.

## Features

- **Room-based translation chat** - Anonymous sessions with room codes
- **Real-time WebSocket communication** - Instant message delivery
- **Self-hosted AI models** - Hugging Face Transformers (no API costs!)
- **Full translation pipeline** - ASR → Translation → TTS
- **Ephemeral storage** - Redis-only, auto-expiring rooms
- **Demo mode** - Mock services for testing/presentations

## Tech Stack

- Django 6.0 + Channels 4.x (WebSockets)
- Redis (channel layer & ephemeral storage)
- Django-Q (background tasks)
- Hugging Face Transformers (ASR, Translation, TTS)
- PyTorch (ML model inference)

## Models Used

### Speech Recognition (ASR)
- **Kikuyu**: `badrex/w2v-bert-2.0-kikuyu-asr`
- **Swahili**: `thinkKenya/wav2vec2-large-xls-r-300m-sw`
- **English**: `facebook/wav2vec2-large-960h-lv60-self`

### Translation
- **NLLB**: `facebook/nllb-200-distilled-600M` (supports Kikuyu, Swahili, English)

### Text-to-Speech
- **Kikuyu**: `facebook/mms-tts-kik`
- **Swahili**: `facebook/mms-tts-swh`
- **English**: `facebook/mms-tts-eng`

## Setup

### Prerequisites

- Python 3.11+
- Redis server
- ~5GB disk space for models (first run only)

### Local Development

1. **Clone and navigate to Backend**:
```bash
cd Backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements/development.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

5. **Run migrations**:
```bash
python manage.py migrate
```

6. **Start Redis** (in separate terminal):
```bash
redis-server
```

7. **Start Django-Q worker** (in separate terminal):
```bash
source venv/bin/activate
python manage.py qcluster
```

8. **Start development server**:
```bash
# Using Daphne (recommended for WebSockets)
daphne -p 8000 lughabridge.asgi:application

# Or using Django's runserver (development only)
python manage.py runserver
```

9. **Access the API**:
- Health check: http://localhost:8000/api/health/
- Create room: POST http://localhost:8000/api/rooms/create/
- WebSocket: ws://localhost:8000/ws/room/{ROOM_CODE}/

### Docker Setup

1. **Build and start services**:
```bash
docker-compose up --build
```

2. **First run** - Models will download (~2GB, takes 10-15 minutes):
```bash
# Watch logs
docker-compose logs -f web
```

3. **Subsequent runs** - Models are cached:
```bash
docker-compose up
```

4. **Stop services**:
```bash
docker-compose down
```

## API Endpoints

### REST API

#### Create Room
```http
POST /api/rooms/create/
Content-Type: application/json

{
  "source_lang": "kikuyu",
  "target_lang": "english"
}

Response:
{
  "room_code": "ABC123",
  "source_language": "kikuyu",
  "target_language": "english",
  "ws_url": "ws://localhost:8000/ws/room/ABC123/",
  "expiry_hours": 4
}
```

#### Join Room
```http
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
```

#### Get Messages
```http
GET /api/rooms/{room_code}/messages/?limit=50

Response:
{
  "room_code": "ABC123",
  "message_count": 5,
  "messages": [...]
}
```

#### Health Check
```http
GET /api/health/

Response:
{
  "status": "healthy",
  "demo_mode": false,
  "supported_languages": ["kikuyu", "english"]
}
```

### WebSocket API

#### Connect
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/room/ABC123/');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

#### Send Voice Message
```javascript
// Send base64 encoded audio
ws.send(JSON.stringify({
  type: 'voice_message',
  message_id: 'unique-id',
  audio_data: 'base64-encoded-wav-data',
  language: 'kikuyu'
}));
```

#### Receive Translation
```javascript
{
  "type": "translation_complete",
  "id": "message-id",
  "original_text": "Wĩ mwega?",
  "original_language": "kikuyu",
  "translated_text": "How are you?",
  "translated_language": "english",
  "stt_confidence": 0.95,
  "translation_confidence": 0.92,
  "audio_data": "base64-encoded-wav",
  "timestamp": "2026-02-19T..."
}
```

## Demo Mode

Run without downloading models for testing/demos:

```bash
# In .env
DEMO_MODE=True
```

Demo mode uses predefined phrases and instant responses. Perfect for:
- Hackathon presentations
- UI development
- Testing without GPU

## Configuration

Key environment variables in `.env`:

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis
REDIS_URL=redis://localhost:6379/0

# Models
HF_CACHE_DIR=/tmp/huggingface_cache
DEMO_MODE=False

# Languages
SUPPORTED_LANGUAGES=kikuyu,english

# CORS
FRONTEND_URL=http://localhost:3000
```

## Adding New Languages

1. **Find Hugging Face models** for ASR, Translation, TTS
2. **Update settings** in `lughabridge/settings.py`:
```python
MODELS = {
    'asr': {
        'swahili': 'thinkKenya/wav2vec2-large-xls-r-300m-sw',
    },
    'translation': {
        'lang_codes': {
            'swahili': 'swh_Latn',
        }
    },
    'tts': {
        'swahili': 'facebook/mms-tts-swh',
    }
}

SUPPORTED_LANGUAGES = ['kikuyu', 'english', 'swahili']
```

3. **Update demo phrases** in `translation/services/mock_services.py`

## Troubleshooting

### Models not downloading
```bash
# Check HF_CACHE_DIR permissions
ls -la /tmp/huggingface_cache

# Or set custom directory
export HF_CACHE_DIR=~/models
```

### Redis connection error
```bash
# Check if Redis is running
redis-cli ping  # Should return PONG

# Or start Redis
redis-server
```

### WebSocket connection refused
```bash
# Use Daphne, not runserver
daphne -p 8000 lughabridge.asgi:application
```

### Out of memory
```bash
# Use smaller models or demo mode
DEMO_MODE=True

# Or use NLLB 600M instead of 1.3B
```

## Development

### Run tests
```bash
pytest
```

### Check code style
```bash
black . --check
flake8
```

### View logs
```bash
# Django-Q worker
python manage.py qcluster  # Shows task logs

# Django
DEBUG=True  # See detailed logs in console
```

## Production Deployment

1. **Set production settings**:
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=strong-random-key
```

2. **Use PostgreSQL** instead of SQLite:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

3. **Use Gunicorn + Nginx**:
```bash
gunicorn lughabridge.asgi:application -k uvicorn.workers.UvicornWorker
```

4. **Monitor with Sentry**:
```bash
pip install sentry-sdk
# Configure in settings.py
```

## License

MIT

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## Support

For issues or questions, open a GitHub issue.
