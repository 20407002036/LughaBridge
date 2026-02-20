# LughaBridge Frontend

Simple single-page application for testing the LughaBridge real-time translation chat backend.

## Features

- 🎤 **Voice Recording** - Record audio from your microphone and send for translation
- 💬 **Text Input** - Type messages as a fallback to voice recording
- 🌍 **Room-based Chat** - Create or join translation rooms with unique codes
- 📜 **Message History** - View past translations in the room
- 🔊 **Audio Playback** - Play translated audio responses
- 🎨 **Clean UI** - Modern, responsive design with real-time status updates

## Prerequisites

1. **Backend Running** - LughaBridge backend must be running on `http://localhost:8000`
   ```bash
   cd Backend
   
   # Start Redis
   redis-server
   
   # Start Django-Q worker (in separate terminal)
   source venv/bin/activate
   python manage.py qcluster
   
   # Start Daphne server (in separate terminal)
   source venv/bin/activate
   daphne -p 8000 lughabridge.asgi:application
   ```

2. **Demo Mode (Optional)** - For quick testing without ML models:
   ```bash
   # In Backend/.env
   DEMO_MODE=True
   ```

3. **CORS Configuration** - Backend must allow frontend origin:
   ```bash
   # In Backend/.env
   FRONTEND_URL=http://localhost:3000
   ```

## Quick Start

### Option 1: Open Directly (Simple Files)

For basic testing without WebSocket restrictions:

1. Simply double-click `index.html` or open it in your browser
2. Note: Some browsers may restrict WebSocket connections from `file://` URLs

### Option 2: Local HTTP Server (Recommended)

For full functionality with proper CORS:

```bash
cd Frontend

# Python 3
python3 -m http.server 3000

# Python 2
python -m SimpleHTTPServer 3000
```

Then open: **http://localhost:3000**

### Option 3: Other HTTP Servers

```bash
# Node.js (npx)
npx serve -p 3000

# Node.js (http-server)
npm install -g http-server
http-server -p 3000

# PHP
php -S localhost:3000
```

## Usage

### 1. Create a Room

1. Click **"Create Room"** on the landing page
2. Select source and target languages (e.g., Kikuyu → English)
3. Click **"Create Room"**
4. Note the **room code** displayed (e.g., ABC123)
5. Share this code with others to join

### 2. Join a Room

1. Click **"Join Room"** on the landing page
2. Enter the room code (e.g., ABC123)
3. Click **"Join Room"**
4. You'll see the chat interface and message history

### 3. Send Voice Messages

1. In the room, ensure **"Voice"** tab is selected
2. Click the **microphone button** to start recording
3. Speak your message (in the source language)
4. Click again to stop recording
5. Message is automatically sent and processed
6. Watch for translation progress (transcribing → translating → synthesizing)
7. Translated message appears with audio playback button

### 4. Send Text Messages

1. Switch to the **"Text"** tab
2. Select the message language
3. Type your message
4. Click **"Send"** or press Enter
5. Translation appears in the chat

### 5. Multi-User Testing

1. Open the frontend in **two browser tabs** (or different browsers)
2. Create a room in Tab 1, copy the room code
3. Join the room in Tab 2 using the room code
4. Send messages from either tab
5. Both tabs receive real-time translations

## Configuration

To change backend URL (if not running on localhost:8000):

1. Open `index.html` in a text editor
2. Find the `CONFIG` object near line 480:
   ```javascript
   const CONFIG = {
       API_BASE_URL: 'http://localhost:8000',   // Change this
       WS_BASE_URL: 'ws://localhost:8000',      // Change this
       AUDIO_SAMPLE_RATE: 16000,
   };
   ```
3. Update URLs to match your backend location
4. For HTTPS/production, use:
   ```javascript
   API_BASE_URL: 'https://yourdomain.com',
   WS_BASE_URL: 'wss://yourdomain.com',
   ```

## Testing Workflow

### Basic Functionality Test

1. **Health Check**
   - Open frontend, should auto-check backend health
   - Look for "Demo mode is active" message if `DEMO_MODE=True`

2. **Create Room**
   - Create room with Kikuyu → English
   - Verify room code appears
   - Check connection status shows "Connected"

3. **Text Message**
   - Send text message: "Hello" (English)
   - Verify processing indicator appears
   - Confirm translated message displays

4. **Voice Message** (if microphone available)
   - Click microphone button
   - Speak a phrase
   - Click to stop
   - Verify audio is sent and translation appears

5. **Audio Playback**
   - Click "Play Audio" button on translated message
   - Confirm audio plays

6. **Multi-User**
   - Join room from second tab
   - Verify message history loads
   - Send message from Tab 1, confirm appears in Tab 2

### Expected Behavior in Demo Mode

With `DEMO_MODE=True`, backend returns predefined phrases:

- **Kikuyu** "Wĩ mwega?" → **English** "How are you?"
- **English** "Hello" → **Kikuyu** "Nĩ wega"

Translations are instant (no ML processing).

## Troubleshooting

### Cannot Connect to Backend

**Error:** "Cannot connect to backend. Make sure it is running on http://localhost:8000"

**Solution:**
- Verify backend is running: `curl http://localhost:8000/api/health/`
- Check backend console for errors
- Ensure Redis is running: `redis-cli ping` (should return PONG)

### CORS Error

**Error:** "Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy"

**Solution:**
- Add `FRONTEND_URL=http://localhost:3000` to `Backend/.env`
- Restart backend server
- Or serve frontend from `file://` (less reliable for WebSockets)

### WebSocket Connection Failed

**Error:** Connection status shows "Disconnected" in room

**Solution:**
- Ensure using **Daphne** not Django runserver:
  ```bash
  daphne -p 8000 lughabridge.asgi:application
  ```
- Check room code is correct
- Verify Redis is running
- Check browser console for WebSocket errors

### Microphone Access Denied

**Error:** "Microphone access denied or not available"

**Solution:**
- Grant microphone permissions in browser
- Use HTTPS in production (Chrome requires HTTPS for getUserMedia)
- Use text input as fallback

### Audio Not Playing

**Error:** "Error playing audio"

**Solution:**
- Check browser console for details
- Ensure browser supports Web Audio API
- Try different browser (Chrome, Firefox recommended)
- Verify translated message has `audio_data` field

### Room Not Found

**Error:** "Room not found" when joining

**Solution:**
- Verify room code is correct (case-sensitive)
- Check if room expired (4-hour TTL by default)
- Create a new room

### No Translation Appears

**Possible Causes:**
1. **Django-Q not running** - Start worker: `python manage.py qcluster`
2. **Models downloading** - First run downloads ~2GB (check backend logs)
3. **Demo mode disabled** - Set `DEMO_MODE=True` for instant testing
4. **Task failed** - Check Django-Q logs for errors

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

**Required APIs:**
- WebSocket
- MediaRecorder (for voice input)
- Web Audio API (for playback)
- Fetch API
- ES6+ JavaScript

## File Structure

```
Frontend/
├── index.html          # Single-page application (HTML + CSS + JS)
└── README.md          # This file
```

## Architecture

**Frontend → Backend Flow:**

1. **REST API** - Create/join room, get message history
   ```
   POST /api/rooms/create/ → {room_code, ws_url}
   GET /api/rooms/{code}/join/ → {room_data}
   GET /api/rooms/{code}/messages/ → {messages[]}
   ```

2. **WebSocket** - Real-time messaging
   ```
   Connect: ws://localhost:8000/ws/room/{code}/
   Send: {type: 'voice_message', audio_data: '...', language: 'kikuyu'}
   Receive: {type: 'chat_message', original_text: '...', translated_text: '...'}
   ```

3. **Translation Pipeline**
   ```
   Voice → Base64 → WebSocket → Backend ASR → Translation → TTS → WebSocket → Audio Playback
   ```

## Next Steps

For production use, consider:

1. **Authentication** - Add user login/signup
2. **Persistence** - Use PostgreSQL instead of Redis-only storage
3. **HTTPS/WSS** - Secure connections for production
4. **Error Handling** - Better retry logic and offline support
5. **UI Enhancements** - Typing indicators, read receipts, emoji support
6. **Mobile Support** - Progressive Web App (PWA) features
7. **Accessibility** - ARIA labels, keyboard navigation

## Support

For issues or questions:
- Check backend logs: `docker-compose logs -f` or console output
- Review browser console for frontend errors
- Verify all prerequisites are running (Redis, Django-Q, Daphne)

## License

MIT (same as backend)
