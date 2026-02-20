# LughaBridge Frontend - Development Log

## Project Overview

Single-page application for real-time translation chat using WebSocket and REST APIs.

## Current Status

- **Last Updated**: February 20, 2026
- **Framework**: React 18 + TypeScript 5.8
- **Build Tool**: Vite 5.4.19
- **Status**: Core UI implemented, backend integration pending

---

## ✅ COMPLETED: Phase 1 - Core Project Structure

### 1.1 Project Setup ✅ (Updated with Universal Design System)

- ✅ Vite + React 18 + TypeScript initialized
- ✅ Tailwind CSS v3.4.17 configured with **Universal Design System**
- ✅ React Router v6.30.1 set up
- ✅ Dependencies installed (see package.json)
- ✅ ESLint + TypeScript configured
- ✅ Vitest configured for testing

**Installed Key Dependencies:**

- `react-router-dom` - Navigation ✅
- `react-hook-form` + `zod` - Form validation ✅
- `@tanstack/react-query` - Data fetching ✅
- `framer-motion` - Animations ✅
- `lucide-react` - Icons ✅
- `shadcn/ui` - UI component library ✅
- `sonner` - Toast notifications ✅

**Universal Design System Applied (from universal-rule-styles.md):**

- ✅ Universal spacing scale (xs: 4px → 3xl: 64px)
- ✅ Universal radius scale (xs: 4px → 2xl: 24px)
- ✅ Universal shadow depth scale (xs → xl)
- ✅ Universal transition durations (fast: 150ms, base: 250ms, slow: 350ms)
- ✅ CHAT_DARK color template applied
- ✅ Glass morphism (Medium strength for chat pattern)
- ✅ Typography scale with proper hierarchy
- ✅ Accessibility compliance (WCAG AA contrast, 44px touch targets, focus states)
- ✅ Universal CSS reset and scrollbar styling
- ✅ Monospace font stack for data/numbers

**Still Needed:**

- [ ] `axios` - HTTP client (for REST API)
- [ ] `zustand` - State management

#### Project Structure

```
src/
├── components/
│   ├── NavLink.tsx          ✅ Router link wrapper
│   ├── lugha/              ✅ Custom chat components
│   │   ├── ChatLayout.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── VoiceInputBar.tsx
│   │   ├── MicButton.tsx
│   │   ├── StatusIndicator.tsx
│   │   ├── ConfidenceRing.tsx
│   │   └── DemoModeToggle.tsx
│   └── ui/                 ✅ shadcn components (50+ components)
├── pages/
│   ├── Index.tsx           ✅ Landing page (with demo)
│   └── NotFound.tsx        ✅ 404 page
├── hooks/
│   ├── use-mobile.tsx      ✅ Mobile detection
│   └── use-toast.ts        ✅ Toast notifications
├── data/
│   └── mockMessages.ts     ✅ Mock chat data & demo sequences
├── lib/
│   └── utils.ts            ✅ classname utility (cn)
├── services/               ❌ NOT IMPLEMENTED
├── stores/                 ❌ NOT IMPLEMENTED
└── types/                  ❌ NOT IMPLEMENTED
```

### 1.2 Build Configuration ✅ (Updated with Universal Rules)

- ✅ `vite.config.ts` - Configured with React plugin, path aliases (@)
- ✅ `tsconfig.json` - TypeScript paths configured
- ✅ `tailwind.config.ts` - Updated with universal spacing, radius, shadows, transitions
- ✅ `postcss.config.js` - PostCSS with Tailwind
- ✅ `index.html` - Entry point with dark mode class
- ✅ `main.tsx` - React root render
- ✅ `src/index.css` - Updated with CHAT_DARK theme and universal reset
- ✅ `src/App.css` - Updated with universal typography utilities

**Tailwind Config Updates (Phase 1 - Universal Rules):**

- Universal spacing scale replaces arbitrary values
- Universal radius scale (xs/sm/base/lg/xl/2xl)
- Universal shadow scale (xs/sm/md/lg/xl)
- Universal transition durations (fast/base/slow)
- Brand color variables aligned with CHAT context
- Monospace font family for data display

**CSS Variables Applied (CHAT_DARK Template):**

- Background: #111827 (dark base)
- Foreground: #F9FAFB (primary text)
- Card/Surface: #1F2937
- Accent Primary: #D4A574 (Gold - brand color)
- Accent Secondary: #10B981 (Emerald - active states)
- Muted: #9CA3AF (secondary text)
- Border: #2D3748 (default borders)
- Glass opacity: 0.03 (subtle), 0.05 (medium)

---

## 📋 Universal Design System Application (Phase 1)

## ✅ COMPLETED: Phase 2 - Core Components

### 2.1 Layout Components ✅

- ✅ `App.tsx` - Main app wrapper with providers (QueryClient, Tooltip, Toaster, Router)

### 2.2 Page Components ✅

- ✅ `pages/Index.tsx` - Landing page with demo mode
  - Displays mock messages with demo sequences
  - Mic button interaction with state management
  - Demo mode toggle functionality
  - Shows system states (listening → transcribing → translating → completed)
- ✅ `pages/NotFound.tsx` - 404 error page

**Missing Landing Page Features:**

- [ ] "Create Room" button/modal with language selection
- [ ] "Join Room" button/modal with room code input
- [ ] Room connection logic
- [ ] Backend health check display

### 2.3 Chat Components ✅

- ✅ `ChatLayout.tsx` - Main chat container
  - Sticky header with app title and status
  - Message list with auto-scroll
  - Voice input bar
  - Empty state display
- ✅ `MessageBubble.tsx` - Individual message display
  - Language badge (Kikuyu/English)
  - Original and translated text
  - Confidence ring visualization
  - Menu with options (copy, share, play audio, etc.)
  - Framer motion animations
  - Sender-based styling (left/right alignment)
- ✅ `StatusIndicator.tsx` - Connection/system status badge
- ✅ `ConfidenceRing.tsx` - Visual confidence ring for translation accuracy
- ✅ `DemoModeToggle.tsx` - Demo mode on/off toggle

### 2.4 Input Components ⚠️ Partially Implemented

- ✅ `VoiceInputBar.tsx` - Mic button container
- ✅ `MicButton.tsx` - Microphone button with state visualization

**Missing Input Components:**

- [ ] `TextInput.tsx` - Text message form with language selector
- [ ] Text input tab switching
- [ ] Character counter
- [ ] Send button with loading state

### 2.5 Modal Components ❌ NOT IMPLEMENTED

- [ ] `CreateRoomModal.tsx` - Room creation form
  - Source language selector
  - Target language selector
  - Submit button
  - Copy room code functionality
- [ ] `JoinRoomModal.tsx` - Room join form
  - Room code input with validation
  - Submit button
- [ ] `LanguageSelector.tsx` - Language dropdown component

### 2.6 Status/Info Components ✅ Partially Implemented

- ✅ `StatusIndicator.tsx` - System state visualization
- ✅ `ConfidenceRing.tsx` - Confidence visualization
- ✅ `DemoModeToggle.tsx` - Demo mode switch

**Missing Info Components:**

- [ ] `ConnectionStatus.tsx` - WebSocket connection indicator
- [ ] `LoadingSpinner.tsx` - Loading animation
- [ ] `ErrorAlert.tsx` - Error message display
- [ ] `SuccessAlert.tsx` - Success notification
- [ ] `AudioPlayer.tsx` - Audio playback button with player

---

## ❌ NOT IMPLEMENTED: Phase 3 - Services & API Integration

### 3.1 API Service ❌

**Location**: `src/services/api.ts`

**What's Needed:**

- [ ] Axios HTTP client setup with configuration
- [ ] API base URL from environment variables
- [ ] Request/response interceptors
- [ ] Error handling wrapper
- [ ] REST endpoints:
  - `POST /api/rooms/create/` - Create room
    - Input: { source_language, target_language }
    - Output: { room_code, ws_url }
  - `GET /api/rooms/{code}/join/` - Join room
    - Output: { room_data, messages[] }
  - `GET /api/rooms/{code}/messages/` - Fetch message history
    - Output: { messages[] }
  - `GET /api/health/` - Backend health check
    - Output: { status, demo_mode }

### 3.2 WebSocket Service ❌

**Location**: `src/services/websocket.ts`

**What's Needed:**

- [ ] WebSocket connection manager class
- [ ] Auto-connect to `ws://localhost:8000/ws/room/{code}/`
- [ ] Message types handling:
  - Send voice: `{type: 'voice_message', audio_data: '...', language: '...'}`
  - Send text: `{type: 'text_message', text: '...', language: '...'}`
  - Receive: `{type: 'chat_message', original_text: '...', translated_text: '...'}`
- [ ] Connection state management (connecting, connected, disconnected, error)
- [ ] Reconnection logic with exponential backoff
- [ ] Message queue for offline mode
- [ ] Event emitter pattern for subscribers

### 3.3 Audio Service ❌

**Location**: `src/services/audio.ts`

**What's Needed:**

- [ ] MediaRecorder API wrapper
  - Start/stop recording
  - Get audio blob
  - Audio constraints (sample rate: 16000)
- [ ] Audio to Base64 encoding
- [ ] Audio playback using Web Audio API
- [ ] Microphone permissions handling
  - Request permission
  - Handle denials
  - Show permission errors
- [ ] Audio visualization data extraction (for waveform)
- [ ] Audio format validation

---

## ❌ NOT IMPLEMENTED: Phase 4 - State Management

### 4.1 Zustand Stores ❌

**Location**: `src/stores/`

**What's Needed:**

#### 4.1.1 `roomStore.ts`

- [ ] Current room code
- [ ] Room data (source_language, target_language)
- [ ] Messages list
- [ ] Connection status (connecting, connected, disconnected)
- [ ] Actions:
  - `createRoom(sourceLanguage, targetLanguage)`
  - `joinRoom(roomCode)`
  - `leaveRoom()`
  - `addMessage(message)`
  - `setConnectionStatus(status)`
  - `fetchMessageHistory()`

#### 4.1.2 `authStore.ts` (Future)

- [ ] User ID/session
- [ ] User preferences (language pair history)
- [ ] Authentication token

#### 4.1.3 `uiStore.ts`

- [ ] Modal visibility states (createRoomOpen, joinRoomOpen)
- [ ] Loading states (isCreatingRoom, isJoiningRoom)
- [ ] Error messages
- [ ] Toast notifications queue
- [ ] System state (idle, listening, transcribing, translating, completed)

---

## ❌ NOT IMPLEMENTED: Phase 5 - Hooks & Utilities

### 5.1 Custom Hooks ❌

**Location**: `src/hooks/`

**What's Needed:**

#### 5.1.1 `useWebSocket.ts`

- [ ] Connect on component mount
- [ ] Disconnect on unmount
- [ ] Auto-reconnect on disconnect
- [ ] Message subscription pattern
- [ ] Return: { isConnected, send, subscribe, disconnect }

#### 5.1.2 `useAudio.ts`

- [ ] Request microphone permission
- [ ] Start recording with MediaRecorder
- [ ] Stop recording and get audio blob
- [ ] Convert audio to Base64
- [ ] Handle permission denied errors
- [ ] Return: { isRecording, startRecording, stopRecording, error }

#### 5.1.3 `useRoom.ts`

- [ ] Create room API call
- [ ] Join room API call
- [ ] Fetch room messages
- [ ] Handle loading/error states
- [ ] Return: { roomCode, messages, loading, error, createRoom, joinRoom }

#### 5.1.4 `useApi.ts`

- [ ] Wrapper for API calls with try-catch
- [ ] Loading state management
- [ ] Error state management
- [ ] Return: { data, loading, error, execute }

#### 5.1.5 `useMessage.ts` (Optional)

- [ ] Send voice message
- [ ] Send text message
- [ ] Message encoding/decoding
- [ ] Return: { sendVoiceMessage, sendTextMessage, isSending }

### 5.2 Utilities ❌

**Location**: `src/lib/`

#### 5.2.1 `config.ts` - Configuration Constants

```typescript
export const CONFIG = {
  API_BASE_URL: process.env.VITE_API_URL || "http://localhost:8000",
  WS_BASE_URL: process.env.VITE_WS_URL || "ws://localhost:8000",
  AUDIO_SAMPLE_RATE: 16000,
  MAX_ROOM_CODE_LENGTH: 10,
  MIN_MESSAGE_LENGTH: 1,
  MAX_MESSAGE_LENGTH: 1000,
  RECONNECT_INTERVAL: 5000,
  RECONNECT_MAX_ATTEMPTS: 5,
};
```

#### 5.2.2 `types.ts` - TypeScript Interfaces

- [ ] `interface Message { id, sender, originalText, translatedText, ... }`
- [ ] `interface Room { code, sourceLanguage, targetLanguage, createdAt }`
- [ ] `interface User { id, sessionId }`
- [ ] `interface WebSocketMessage { type, payload }`
- [ ] `type SystemState = 'idle' | 'listening' | 'transcribing' | 'translating' | 'completed' | 'error'`
- [ ] `type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'reconnecting'`

#### 5.2.3 `validators.ts` - Input Validation

- [ ] Room code validation (alphanumeric, 3-10 chars)
- [ ] Language code validation
- [ ] Message length validation
- [ ] Email validation (future)

#### 5.2.4 `helpers.ts` - Utility Functions

- [ ] Format timestamp for display
- [ ] Language name to code mapping
- [ ] Base64 encoding/decoding
- [ ] Audio blob to WAV conversion
- [ ] Error message formatting

---

## ❌ NOT IMPLEMENTED: Phase 6 - Styling & UI Polish

### 6.1 CSS Customization ✅ Partially Done

- ✅ CSS variables for theming (colors, spacing)
- ✅ Tailwind dark mode configured
- ✅ Global styles in `index.css`
- ✅ App-specific styles in `App.css`

**Still Needed:**

- [ ] Animation keyframes customization
- [ ] Custom scrollbar styling
- [ ] Glass-morphism effects refinement
- [ ] Dark mode complete coverage

### 6.2 Responsive Design ⚠️ Partially Implemented

- ✅ Mobile-first Tailwind approach
- ✅ ChatLayout responsive (max-w-lg, flex)
- ✅ Message bubbles responsive (85% width on mobile, 70% on desktop)

**Still Needed:**

- [ ] Tablet optimization
- [ ] Desktop layout optimization (potentially two-column layout)
- [ ] Modal responsive design
- [ ] Input fields responsive
- [ ] Test on various screen sizes

---

## ❌ NOT IMPLEMENTED: Phase 7 - Routing & Navigation

### 7.1 React Router Setup ✅ Basic

- ✅ BrowserRouter configured
- ✅ Routes structure:
  - `/` → Index (landing/demo page)
  - `/404` → Not Found page (on `*`)
  - `/room/:code` → Missing (needs implementation)

**Still Needed:**

- [ ] `/room/:code` route for actual chat room
  - [ ] Load room data from URL code
  - [ ] Auto-join room on mount
  - [ ] WebSocket connection
- [ ] Protected routes (future authentication)
- [ ] Route transitions/animations
- [ ] Breadcrumb navigation
- [ ] Error boundary for error handling

---

## ❌ NOT IMPLEMENTED: Phase 8 - Error Handling & Validation

### 8.1 Error Handling ❌

- [ ] API error interceptor with retry logic
- [ ] WebSocket disconnection handling
- [ ] Microphone permission denial handling
- [ ] Network timeout handling
- [ ] User-friendly error messages
- [ ] Error logging/telemetry
- [ ] Graceful degradation

### 8.2 Form Validation ❌

- [ ] Room code validation (length, format)
- [ ] Language selection requirement
- [ ] Text message min/max length
- [ ] Real-time validation feedback
- [ ] Error messages for invalid input

### 8.3 Input Sanitization ❌

- [ ] Text input sanitization
- [ ] Room code sanitization
- [ ] XSS prevention
- [ ] SQL injection prevention (N/A for frontend)

---

## ❌ NOT IMPLEMENTED: Phase 9 - Testing

### 9.1 Unit Tests ❌

**Location**: `src/__tests__/`

**What's Needed:**

- [ ] Component tests:
  - [ ] `MessageBubble.test.tsx`
  - [ ] `ChatLayout.test.tsx`
  - [ ] `MicButton.test.tsx`
  - [ ] `StatusIndicator.test.tsx`
- [ ] Hook tests:
  - [ ] `useWebSocket.test.ts`
  - [ ] `useAudio.test.ts`
  - [ ] `useRoom.test.ts`
- [ ] Utility tests:
  - [ ] `validators.test.ts`
  - [ ] `helpers.test.ts`
  - [ ] `config.test.ts`
- [ ] Store tests:
  - [ ] `roomStore.test.ts`
  - [ ] `uiStore.test.ts`

### 9.2 Integration Tests ❌

- [ ] API service tests (mock axios)
- [ ] WebSocket mock tests
- [ ] Room creation + join flow
- [ ] Message sending + receiving flow
- [ ] Audio recording + playback flow

### 9.3 E2E Tests ❌ (Optional)

- [ ] Create room and chat flow
- [ ] Join room flow
- [ ] Send voice message flow
- [ ] Send text message flow
- [ ] Multi-user real-time sync

---

## ❌ NOT IMPLEMENTED: Phase 10 - Performance & Optimization

### 10.1 Code Splitting ❌

- [ ] Lazy load room page component
- [ ] Dynamic import of modals
- [ ] Chunk analysis with Vite plugin

### 10.2 Memoization ❌

- [ ] Memoize expensive components
- [ ] useMemo for message list filtering
- [ ] useCallback for event handlers
- [ ] Prevent unnecessary re-renders

### 10.3 Bundle Optimization ❌

- [ ] Tree-shake unused code
- [ ] Minify and compress assets
- [ ] Analyze bundle with Vite analyzer
- [ ] Reduce shadcn/ui imports

### 10.4 Performance Monitoring ❌

- [ ] Web Vitals tracking
- [ ] Lighthouse audits
- [ ] Performance profiling
- [ ] Load time measurement

---

## ❌ NOT IMPLEMENTED: Phase 11 - Backend Integration Testing

### 11.1 Backend API Testing ❌

- [ ] Test `/api/health/` endpoint
- [ ] Test room creation endpoint
- [ ] Test room join endpoint
- [ ] Test message history endpoint
- [ ] Test error responses

### 11.2 WebSocket Testing ❌

- [ ] Connect to WebSocket
- [ ] Send/receive messages
- [ ] Handle disconnection
- [ ] Test message format
- [ ] Test auto-reconnection

### 11.3 End-to-End Flow Testing ❌

- [ ] Create room → Get room code
- [ ] Another user joins with code
- [ ] Send voice message → Receive translation
- [ ] Send text message → Receive translation
- [ ] Multiple messages → History display
- [ ] Real-time sync between users

---

## ❌ NOT IMPLEMENTED: Phase 12 - Deployment Preparation

### 12.1 Environment Configuration ❌

- [ ] `.env.example` template
- [ ] `.env.development`
- [ ] `.env.production`
- [ ] Environment variable validation

### 12.2 Build Optimization ❌

- [ ] Production build configuration
- [ ] Source maps configuration
- [ ] Asset hashing
- [ ] Cache busting strategy

### 12.3 CI/CD Pipeline ❌

- [ ] GitHub Actions workflow
- [ ] Auto-test on push
- [ ] Auto-build on release
- [ ] Deployment automation

### 12.4 Docker Configuration ❌ (Optional)

- [ ] Dockerfile for frontend
- [ ] Multi-stage build
- [ ] Docker Compose integration

### 12.5 Deployment Documentation ❌

- [ ] Deployment guide
- [ ] Environment setup
- [ ] Troubleshooting guide

---

## 📋 Implementation Priority

### 🔴 CRITICAL (Must have for MVP)

1. **Phase 3.1** - API Service (REST client setup)
2. **Phase 3.2** - WebSocket Service (real-time messaging)
3. **Phase 3.3** - Audio Service (recording + playback)
4. **Phase 4.1** - Zustand State Management
5. **Phase 5.1.1** - useWebSocket hook
6. **Phase 5.1.2** - useAudio hook
7. **Phase 5.2.1** - Configuration setup
8. **Phase 5.2.2** - Type definitions
9. **Phase 2.5** - Modals (Create Room, Join Room)
10. **Phase 2.4** - Text input component
11. **Phase 7.1** - Room route (/room/:code)

### 🟡 HIGH (Important for functionality)

12. **Phase 5.1.3** - useRoom hook
13. **Phase 8.1** - Basic error handling
14. **Phase 8.2** - Input validation
15. **Phase 2.6** - Additional status components
16. **Phase 5.2.3** - Validators utility
17. **Phase 5.2.4** - Helper functions

### 🟢 MEDIUM (Nice to have)

18. **Phase 9** - Testing suite
19. **Phase 10** - Performance optimization
20. **Phase 6.2** - Responsive design polish

### 🔵 LOW (Future/Polish)

21. **Phase 11** - Comprehensive backend testing
22. **Phase 12** - Deployment preparation
23. **Phase 4.1.2** - Auth store

---

## 🔧 Tech Stack Summary

| Layer            | Technology      | Version | Status            |
| ---------------- | --------------- | ------- | ----------------- |
| Framework        | React           | 18.3.1  | ✅                |
| Language         | TypeScript      | 5.8.3   | ✅                |
| Build Tool       | Vite            | 5.4.19  | ✅                |
| Routing          | React Router    | 6.30.1  | ✅                |
| Styling          | Tailwind CSS    | 3.4.17  | ✅                |
| UI Components    | shadcn/ui       | Latest  | ✅                |
| Forms            | react-hook-form | 7.61.1  | ✅                |
| Validation       | Zod             | 3.25.76 | ✅                |
| Data Fetching    | React Query     | 5.83.0  | ✅                |
| Animations       | Framer Motion   | 12.34.2 | ✅                |
| HTTP Client      | Axios           | -       | ❌                |
| State Management | Zustand         | -       | ❌                |
| WebSocket        | Native WS API   | -       | ❌                |
| Testing          | Vitest          | 3.2.4   | ✅ (not used yet) |
| Linting          | ESLint          | 9.32.0  | ✅                |

---

## 🎯 Key Features Status

### Core Features

- ✅ Mock chat interface (demo mode)
- ✅ Message display with confidence rings
- ✅ Status indicators
- ✅ Voice input interface (UI only)
- ✅ Message history display
- ⚠️ Multi-user support (backend only)
- ❌ Real room creation
- ❌ Real room joining
- ❌ WebSocket messaging
- ❌ Audio recording
- ❌ Audio playback
- ❌ Real translations

### UI/UX Features

- ✅ Responsive design (mobile-first)
- ✅ Dark mode support
- ✅ Smooth animations
- ✅ Glass morphism effects
- ✅ Toast notifications
- ✅ Loading states (UI ready)
- ✅ Error display ready
- ⚠️ Form inputs (minimal)
- ❌ Input validation messages
- ❌ Accessibility (WCAG)

---

## 📱 Browser Compatibility

Targeted Support (from shadcn/ui):

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+

Required APIs:

- ✅ ES2020+ JavaScript
- ❌ WebSocket (ready to implement)
- ❌ MediaRecorder API (ready to implement)
- ❌ Web Audio API (ready to implement)
- ❌ Fetch API (ready to implement)

---

## 🚀 Next Immediate Steps

### Week 1 Priority

1. **Install missing package**: `npm install axios zustand`
2. **Create configuration** - `src/lib/config.ts`
3. **Create type definitions** - `src/types/index.ts`
4. **Implement API service** - `src/services/api.ts`
5. **Implement WebSocket service** - `src/services/websocket.ts`
6. **Implement audio service** - `src/services/audio.ts`

### Week 1-2 Priority

7. **Create Zustand stores** - `src/stores/roomStore.ts`, `uiStore.ts`
8. **Create custom hooks** - `useWebSocket.ts`, `useAudio.ts`, `useRoom.ts`
9. **Create modals** - `CreateRoomModal.tsx`, `JoinRoomModal.tsx`
10. **Refactor Index.tsx** - Add create/join room flow instead of just demo
11. **Create room page** - `pages/RoomPage.tsx`
12. **Implement text input component** - `VoiceInputBar.tsx` → Tab switching

### Testing & Polish

13. **Add error handling** - Error boundaries, error states
14. **Add form validation** - Room code, language selection
15. **Add tests** - Basic component tests
16. **Optimize** - Code splitting, performance

---

## 📝 Development Notes

### Current Architecture Observations

- ✅ Good: Component-based architecture with shadcn/ui
- ✅ Good: Framer motion for smooth animations
- ✅ Good: TypeScript strict mode enabled
- ✅ Good: Tailwind CSS for consistency
- ⚠️ Concern: No state management yet (mock data in component state)
- ⚠️ Concern: No API integration ready
- ⚠️ Concern: No WebSocket setup
- ⚠️ Concern: No audio handling
- 🔴 Missing: Landing page with room creation/joining

### Best Practices to Follow

- Use TypeScript interfaces for all props and states
- Keep components pure and focused
- Use custom hooks for logic reusability
- Implement proper error boundaries
- Add loading and error states to all async operations
- Use Zustand for global state (not Context API)
- Keep shadcn/ui components unstyled, use Tailwind classes
- Use Vitest for unit tests
- Add proper TypeScript types to all functions

---

## 📊 Project Statistics

- **Total Components**: 50+ (mostly from shadcn/ui)
- **Custom Components**: 8 (ChatLayout, MessageBubble, VoiceInputBar, MicButton, StatusIndicator, ConfidenceRing, DemoModeToggle, NavLink)
- **Pages**: 2 (Index, NotFound)
- **Hooks**: 2 (use-mobile, use-toast)
- **Dependencies**: 50+ packages
- **TypeScript**: 100% (goal)
- **Test Coverage**: 0% (not started)

---

## 🎨 UI/UX Flow Documentation

### Component Hierarchy & Architecture

```
App (Root)
├── Provider Wrapper (QueryClientProvider, TooltipProvider, Toaster, Router)
│
└── Routes
    ├── "/" → Index (Landing Page)
    │   │
    │   └── ChatLayout (Main UI Container)
    │       ├── Header (Title + Status + Demo Toggle)
    │       │   ├── Branding (LughaBridge title)
    │       │   ├── StatusIndicator (System state badge)
    │       │   └── DemoModeToggle (On/Off switch)
    │       │
    │       ├── Messages Container (Scrollable)
    │       │   ├── Empty State (when no messages)
    │       │   │   └── Icon + "Tap to Speak" text
    │       │   │
    │       │   └── Message List
    │       │       └── MessageBubble[] (repeated)
    │       │           ├── Language Badge (Kikuyu/English)
    │       │           ├── Original Text (sender's language)
    │       │           ├── Translated Text (translated language)
    │       │           ├── Menu Button (More options)
    │       │           │   └── Menu Items:
    │       │           │       ├── Read Original Aloud
    │       │           │       ├── Read Translation Aloud
    │       │           │       ├── Change Voice
    │       │           │       ├── Copy Text
    │       │           │       └── Share
    │       │           │
    │       │           ├── Confidence Ring (accuracy visualization)
    │       │           └── Timestamp (12:34 PM)
    │       │
    │       └── Voice Input Bar (Bottom sticky)
    │           ├── Status Label (Tap to Speak / Listening / etc.)
    │           ├── Microphone Button
    │           │   ├── Idle State: Golden glow
    │           │   ├── Recording State: Emerald glow + pulse
    │           │   ├── Processing State: Muted color
    │           │   └── Error State: Red tint
    │           │
    │           └── Sub-text feedback
    │
    └── "*" → NotFound (404 Page)
```

### Current UI Flows

#### **FLOW 1: Initial Application Load**

```
1. User visits http://localhost:3000
   ↓
2. App renders with default state:
   - Messages: Pre-populated mock messages
   - System State: 'idle'
   - Demo Mode: OFF
   ↓
3. ChatLayout displays:
   - Header with "LughaBridge" title
   - Status badge showing "Ready"
   - Demo toggle in OFF position
   - Message history with 4+ mock messages
   - Empty state hidden (messages exist)
   - Mic button ready to interact
```

#### **FLOW 2: User Clicks Microphone (Manual Message)**

```
Click Cycle:
1. User clicks Mic Button
   ↓
2. If systemState !== 'idle' AND !== 'completed' → Ignore click (disabled)
   If systemState = 'idle' OR 'completed' → Process
   ↓
3. simulateMessage() function triggers:
   - Set systemState → 'listening' (Mic visual changes: Gold → Emerald)
   - Label changes: "Tap to Speak" → "Listening…"
   ↓ (Wait 1200ms - simulated recording)
   ↓
4. Set systemState → 'transcribing'
   - Label changes: "Listening…" → "Transcribing…"
   ↓ (Wait 700ms - simulated ASR processing)
   ↓
5. Set systemState → 'translating'
   - Label changes: "Transcribing…" → "Translating…"
   ↓ (Wait 900ms - simulated translation)
   ↓
6. Set systemState → 'completed'
   - Create & add new ChatMessage to messages[]
   - New message animates in (fade + slide up)
   - Reset label: "Translating…" → "Tap to Speak"
   - Scroll auto-scrolls to bottom
   ↓ (Wait 800ms)
   ↓
7. Set systemState → 'idle'
   - Button re-enabled for next interaction
   - Mic ready for next message
```

#### **FLOW 3: Demo Mode Auto-Play**

```
Demo Toggle OFF (default):
- Manual mic clicks work
- No auto-playback
- demoTimeout cleared on toggle

Demo Toggle ON:
1. User clicks DemoModeToggle switch
   ↓
2. handleDemoToggle(true) triggers runDemo(0)
   ↓
3. runDemo() runs automated sequence:
   - Loop through demoSequence array
   - Each iteration:
     a) Trigger systemState transitions (listening → transcribing → translating)
     b) Add next message from demoSequence to messages[]
     c) Show all animation + state changes
     d) Wait 500ms, then run runDemo(i + 1)
   ↓
4. When demoSequence ends (i >= length):
   - Stop looping
   - Wait for user interaction
```

#### **FLOW 4: User Interacts with Message Menu**

```
1. User clicks 3-dot menu on message bubble
   ↓
2. Menu state toggles open/closed
   ↓
3. Menu items appear with animation (fade + scale):
   - Read Original Aloud
   - Read Translation Aloud
   - Change Voice
   - Copy Text
   - Share
   ↓
4. User clicks any menu item:
   - Menu closes
   - (Currently no-op - ready for backend integration)
   ↓
5. Click outside menu:
   - Closes automatically (useEffect with mousedown listener)
```

#### **FLOW 5: Chat History & Auto-Scroll**

```
1. Messages array updates:
   - New message added to state
   ↓
2. useEffect triggers on [messages] dependency:
   - Gets scrollRef element
   - Sets scrollTop = scrollHeight
   ↓
3. User sees auto-scroll to latest message
   - Smooth scroll behavior (natural JS scroll)
   - Works even with many messages
```

### System States & Visual Changes

| State          | Duration | Label           | Mic Color            | Button State      | Auto-Reset |
| -------------- | -------- | --------------- | -------------------- | ----------------- | ---------- |
| `idle`         | ∞        | "Tap to Speak"  | Gold glow            | Enabled           | N/A        |
| `listening`    | 1200ms   | "Listening…"    | Emerald glow + pulse | Disabled          | No         |
| `transcribing` | 700ms    | "Transcribing…" | Muted (gray)         | Disabled          | No         |
| `translating`  | 900ms    | "Translating…"  | Muted (gray)         | Disabled          | No         |
| `completed`    | 0-800ms  | "Tap to Speak"  | Gold glow            | Enabled (briefly) | Yes → idle |
| `error`        | ∞        | "Try Again"     | Red tint             | Enabled           | Manual     |

### Message Bubble Anatomy

```
┌─────────────────────────────────────────┐
│ Kikuyu     ⋮ (Three-dot menu)          │  ← Language badge + menu button
├─────────────────────────────────────────┤
│ Wĩ mwega? Nĩ ngũkena gũkuona.         │  ← Original text (bold, larger)
├─────────────────────────────────────────┤
│ How are you? I am happy to see you.    │  ← Translated text (smaller, muted)
├─────────────────────────────────────────┤
│ ◯ (confidence ring)     12:34 PM        │  ← Confidence + timestamp
└─────────────────────────────────────────┘
```

**Styling by Sender:**

- Sender A (Left): Light glass background, left-aligned
- Sender B (Right): Slightly darker glass background, right-aligned

**Animations:**

- Initial: Fade in (0 → 1 opacity) + slide up (y: 12 → 0)
- Duration: 250ms easing

### Header Component

```
┌────────────────────────────┐
│ LughaBridge    Status  Toggle
│ Real-Time Kikuyu ↔ English
└────────────────────────────┘
```

**Elements:**

1. **Title** - "Lugha" (normal) + "Bridge" (gold colored)
2. **Subtitle** - "Real-Time Kikuyu ↔ English Translation" (small, muted)
3. **Status Indicator** - Visual badge showing current systemState
4. **Demo Toggle** - Switch to turn demo mode on/off

**Sticky Behavior:**

- Header stays at top while user scrolls messages
- Backdrop blur effect (glass-morphism)
- Border-bottom subtle separator

### Input Area Component

```
Label: "Tap to Speak" / "Listening…" / etc.
        ↓
    ┌─────────┐
    │    🎤   │  16x16 button
    │ (glowing)
    └─────────┘
        ↓
    Sub-feedback (optional)
```

**Button States:**

- **Idle**: Golden background, subtle glow
- **Recording**: Emerald background, animated pulse
- **Processing**: Muted, disabled (cursor: wait)
- **Error**: Red-tinted, enabled for retry

### Responsive Breakpoints (Tailwind)

```
Mobile (max-w-lg):
- ChatLayout: max-w-lg (32rem) = full viewport width
- Message bubbles: max-w-[85%]
- Padding: px-4, py-3.5

Tablet (sm: and up):
- Message bubbles: max-w-[70%]
- Slightly more spacious padding

Desktop (md: and up):
- Max-width enforced, centered
- Could expand for future multi-column layout
```

### Component Data & Props Flow

In this app, all state lives in **Index.tsx** and flows downward:

1. **State Definition** (Index.tsx):
   - `messages[]` - Array of ChatMessage objects
   - `systemState` - Current processing state
   - `demoMode` - Boolean for demo auto-play
   - `demoIndex` - Ref to current demo sequence index
   - `demoTimeout` - Ref to scheduled timeouts

2. **Callbacks** (Index.tsx):
   - `simulateMessage()` - Triggered by mic click, runs state transitions
   - `handleMicPress()` - Click handler for mic button
   - `handleDemoToggle()` - Click handler for demo switch

3. **Props Passing**:
   - Index.tsx → ChatLayout (5 props: messages, systemState, demoMode, onDemoToggle, onMicPress)
   - ChatLayout → Children (distributed props)
   - MessageBubble manages own local state (menuOpen)

### Key State Transitions

```typescript
// In Index.tsx state management:

// Manual click flow:
idle → listening (1200ms) → transcribing (700ms) → translating (900ms) → completed (800ms) → idle

// Demo mode flow (looping):
For each item in demoSequence:
  idle → listening → transcribing → translating → completed → [wait 500ms] → next iteration

// Toggle handlers:
- demoToggle OFF: Clear timeout, reset state to idle
- demoToggle ON: Start runDemo loop from index 0
```

### Visual Screen States

#### **Screen 1: Initial Load (Empty or with Mock Data)**

```
┌─────────────────────────────────────────┐
│ LughaBridge (gold)      Ready/Processing │ ← Header sticky
├─────────────────────────────────────────┤
│                                         │
│         🎤 (gold icon)                  │ ← Empty state or
│    "Tap the microphone to begin"        │   Message list starts
│    "Speak in Kikuyu or English"         │
│                                         │
│  [Message bubbles if messages exist]    │
│                                         │
├─────────────────────────────────────────┤
│             [Label: "Tap to Speak"]     │ ← Voice input sticky
│          ◯  []  )))  )))    ◯          │
│             Μic Button (Gold Glow)      │
└─────────────────────────────────────────┘
```

#### **Screen 2: During Recording (Listening)**

```
┌─────────────────────────────────────────┐
│ LughaBridge                Pulse ⚪      │ ← Status shows listening
├─────────────────────────────────────────┤
│                                         │
│  Previous messages...                   │
│                                         │
├─────────────────────────────────────────┤
│            [Label: "Listening…"]        │
│          ◯   ~    ~    ~   ◯            │ ← Emerald glow + pulse
│         Mic Button Animating            │
│          (Disabled, red circle)         │
└─────────────────────────────────────────┘
```

#### **Screen 3: Processing (Transcribing)**

```
┌─────────────────────────────────────────┐
│ LughaBridge                Processing    │ ← Status shows transcribing
├─────────────────────────────────────────┤
│  Previous messages...                   │
├─────────────────────────────────────────┤
│          [Label: "Transcribing…"]       │
│          ◯         ◯                    │ ← Muted/gray, disabled
│      Mic Button (Gray - Disabled)       │
└─────────────────────────────────────────┘
```

#### **Screen 4: Processing (Translating)**

```
┌─────────────────────────────────────────┐
│ LughaBridge                Processing    │ ← Status shows translating
├─────────────────────────────────────────┤
│  Previous messages...                   │
├─────────────────────────────────────────┤
│          [Label: "Translating…"]        │
│          ◯         ◯                    │ ← Still disabled
│      Mic Button (Gray - Disabled)       │
└─────────────────────────────────────────┘
```

#### **Screen 5: Message Added (Completed)**

```
┌─────────────────────────────────────────┐
│ LughaBridge                   Ready      │ ← Status shows ready
├─────────────────────────────────────────┤
│  [Previous messages...]                 │
│                                         │
│         ┌────────────────────┐          │
│         │ Kikuyu    ⋮        │          │ ← NEW MESSAGE (animated in)
│         │ Original text...   │          │   Fade + slide up
│         │ Translated text... │          │
│         │ ◯ Ring  12:34 PM  │          │
│         └────────────────────┘          │
│                                         │
├─────────────────────────────────────────┤
│            [Label: "Tap to Speak"]      │
│          ◯         ◯ (Gold Glow)        │ ← Still momentarily disabled
│        Mic Button (Ready)               │
└─────────────────────────────────────────┘
```

#### **Screen 6: Back to Idle (Ready for Next)**

```
┌─────────────────────────────────────────┐
│ LughaBridge                    Ready     │ ← Back to normal
├─────────────────────────────────────────┤
│  [All messages including new one]       │
│                                         │
│  Auto-scrolled to show latest message   │
│                                         │
├─────────────────────────────────────────┤
│             [Label: "Tap to Speak"]     │
│          ◯  [Subtle glow] ◯             │ ← ENABLED & ready
│        Mic Button (Idle)                │
└─────────────────────────────────────────┘
```

#### **Screen 7: Message Menu Interaction**

```
┌─────────────────────────────────────────┐
│                                         │
│  Message with menu open:                │
│  ┌───────────────────────────┐          │
│  │ Kikuyu    ⋮               │          │
│  │ Original text...          │          │
│  │ Translated text...        │          │
│  │ ◯ Ring  12:34 PM         │          │
│  └───────────────────────────┘          │
│      ┌──────────────────────┐           │
│      │ 🔊 Read Original    │ ← Menu appears
│      │ 🔊 Read Translation │   with animation
│      │ 🎤 Change Voice     │
│      │ 📋 Copy Text        │
│      │ 📤 Share            │
│      └──────────────────────┘
│                                         │
└─────────────────────────────────────────┘
```

---

## 📱 UI Interaction Patterns

### Click Interactions

**Mic Button Click:**

- Ignored if state != 'idle' and != 'completed'
- Triggers simulateMessage() if state safe
- Disabled during processing phases

**Demo Toggle Click:**

- ON: Starts auto-play loop
- OFF: Clears timeout, resets state
- Multiple messages auto-sent

**Message Menu Click:**

- Opens dropdown with animation
- Closes on item click
- Closes on outside click (useEffect)

**Menu Item Click:**

- Currently no-op (ready for implementation)
- Planned: TTS, copy, share, etc.

### Keyboard Interactions

Currently: None (voice-first design)

Future additions:

- Enter to send text message
- Spacebar to toggle recording
- Escape to close menus

---

## 🎨 Styling & Animation Details

### Tailwind Classes Used

```
Layout:
- flex, flex-col, h-[100dvh], max-w-lg, mx-auto
- sticky (top-0, bottom-0), z-30
- overflow-y-auto, scrollbar-none

Text:
- text-lg, text-sm, text-xs (sizes)
- font-bold, font-medium (weights)
- tracking-tight, tracking-wide (spacing)
- text-foreground, text-muted-foreground (colors)

Interactive:
- hover:bg-muted/50, transition-colors
- disabled:cursor-wait
- rounded-full, rounded-xl (shapes)

Effects:
- bg-background/80, backdrop-blur-xl (glass)
- border-b, border-border/50 (dividers)
- shadow-xl (elevation)
```

### Framer Motion Animations

1. **Message Bubbles** (on enter):

   ```
   opacity: 0 → 1
   y: 12 → 0
   duration: 250ms
   easing: easeOut
   ```

2. **Menu** (on open):

   ```
   opacity: 0 → 1
   y: 8 → 0
   scale: 0.98 → 1
   duration: 150ms
   ```

3. **Status Label** (on state change):

   ```
   opacity: 0 → 1
   y: 4 → 0
   (key-based animation)
   ```

4. **Mic Button**:
   - Idle: `animate-mic-idle` (subtle pulse - custom CSS)
   - Recording: `animate-pulse-glow` (strong pulse - custom CSS)

---

## 🔄 Future Screen Flows (Planned)

### Landing Page (Not Yet Implemented)

```
┌─────────────────────────────────────────┐
│   Lugha🟰Bridge                         │
│                                         │
│   Real-Time Translation Chat            │
│                                         │
│   [Create Room Button] [Join Room Button]
│                                         │
│   About the app / Features              │
└─────────────────────────────────────────┘
```

### Create Room Modal (Not Yet Implemented)

```
Modal Dialog:
- Title: "Create Translation Room"
- Source Language: [Dropdown: Kikuyu/English]
- Target Language: [Dropdown: English/Kikuyu]
- [Create Button] [Cancel Button]
- Shows room code after creation
```

### Join Room Modal (Not Yet Implemented)

```
Modal Dialog:
- Title: "Join Room"
- Room Code Input: [Text field]
- [Join Button] [Cancel Button]
- Error message if room not found
```

### Room Chat Page (Not Yet Implemented)

```
/room/:code
- Similar to current chat layout
- Actual WebSocket messages
- Real audio recording
- Multiple users
- Room info in header
```

---

## 📝 Summary: How It Works Today (v0.1.2)

1. **Landing**: User sees ChatLayout with mock messages
2. **Empty State**: Icon + "Tap to speak" if no messages
3. **Manual Mode** (Default):
   - Click mic → State transitions (listening → transcribing → translating)
   - New mock message appears
   - Auto-scroll to latest
   - Ready for next click
4. **Demo Mode** (Togglable):
   - Click toggle → Auto-plays demo sequence
   - Messages appear automatically with timing
   - Toggle OFF → Stops and resets
5. **Message Interaction**:
   - Click menu on any message
   - See options (read aloud, copy, share, etc.)
   - Menu closes on selection
6. **Visual Feedback**:
   - Color-coded states (gold idle, emerald recording, gray processing)
   - Animated transitions
   - Auto-scroll keeps latest message visible
   - Status badge shows current state

---

## 🔗 Backend Integration Points

### API Endpoints Needed

```
POST /api/rooms/create/
  Request: { source_language: string, target_language: string }
  Response: { room_code: string, ws_url: string }

GET /api/rooms/{code}/join/
  Response: { room_data: object, messages: [] }

GET /api/rooms/{code}/messages/
  Response: { messages: [] }

GET /api/health/
  Response: { status: string, demo_mode: boolean }
```

### WebSocket Endpoints Needed

```
ws://localhost:8000/ws/room/{code}/

Message Types:
- voice_message: { type, audio_data, language }
- text_message: { type, text, language }
- chat_message: { type, original_text, translated_text, sender }
```

---

## 📞 Contact & Support

For backend integration questions, check Backend/ directory README.

---

## 📄 Version History

| Date         | Version | Status                | Notes                                                                       |
| ------------ | ------- | --------------------- | --------------------------------------------------------------------------- |
| Feb 20, 2026 | v0.1.0  | Core UI Complete      | Initial setup, demo mode working                                            |
| Feb 20, 2026 | v0.1.1  | Documentation Updated | Added comprehensive implementation tracking                                 |
| Feb 20, 2026 | v0.1.2  | UI Flow Documentation | Added detailed UI flows, component hierarchy, and interaction documentation |
