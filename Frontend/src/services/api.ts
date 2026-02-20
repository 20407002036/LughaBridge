import type { CreateRoomPayload, CreateRoomResponse, JoinRoomResponse, HealthCheckResponse } from '@/types';
import { generateRoomCode } from '@/data/mockRooms';
import { mockMessages, type ChatMessage } from '@/data/mockMessages';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const WS_BASE = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/ws';
// Use real API by default; fall back to mock on failure
const USE_MOCK_DEFAULT = false;

async function mockDelay(ms = 600) {
  return new Promise((r) => setTimeout(r, ms));
}

export const api = {
  baseUrl: API_BASE,
  wsBase: WS_BASE,

  async createRoom(payload: CreateRoomPayload): Promise<CreateRoomResponse> {
    try {
      if (!USE_MOCK_DEFAULT) {
        const res = await fetch(`${API_BASE}/rooms/create/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error('Failed to create room');
        return res.json();
      }
      throw new Error('Mock fallback forced');
    } catch {
      await mockDelay();
      const code = generateRoomCode();
      return {
        room_code: code,
        ws_url: `${WS_BASE}/room/${code}/`,
      };
    }
  },

  async joinRoom(code: string): Promise<JoinRoomResponse> {
    try {
      if (!USE_MOCK_DEFAULT) {
        const res = await fetch(`${API_BASE}/rooms/${code}/join/`);
        if (!res.ok) throw new Error('Room not found');
        return res.json();
      }
      throw new Error('Mock fallback forced');
    } catch {
      await mockDelay();
      return {
        room_code: code,
        source_language: 'Kikuyu',
        target_language: 'English',
        messages: mockMessages,
      };
    }
  },

  async healthCheck(): Promise<HealthCheckResponse> {
    try {
      if (!USE_MOCK_DEFAULT) {
        const res = await fetch(`${API_BASE}/health/`);
        if (!res.ok) throw new Error('Backend unreachable');
        return res.json();
      }
      throw new Error('Mock fallback forced');
    } catch {
      await mockDelay(200);
      return { status: 'ok', demo_mode: true };
    }
  },

  getWsUrl(roomCode: string): string {
    return `${WS_BASE}/room/${roomCode}/`;
  },

  normalizeMessages(raw: any[]): ChatMessage[] {
    return (raw || []).map((m, idx) => ({
      id: m.id ?? `msg-${idx}-${Date.now()}`,
      sender: (m.sender as ChatMessage['sender']) ?? 'A',
      originalText: m.originalText ?? m.original_text ?? '',
      translatedText: m.translatedText ?? m.translated_text ?? '',
      originalLanguage: (m.originalLanguage ?? m.original_language ?? 'Kikuyu') as ChatMessage['originalLanguage'],
      timestamp: m.timestamp ? new Date(m.timestamp) : new Date(),
      confidence: typeof m.confidence === 'number' ? m.confidence : 0.9,
    }));
  },
};
