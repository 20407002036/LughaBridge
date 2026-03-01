import type { CreateRoomPayload, CreateRoomResponse, JoinRoomResponse, HealthCheckResponse, MessagesResponse } from '@/types';
import type { ChatMessage } from '@/data/mockMessages';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const WS_BASE = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/ws';

export const api = {
  baseUrl: API_BASE,
  wsBase: WS_BASE,

  async createRoom(payload: CreateRoomPayload): Promise<CreateRoomResponse> {
    const res = await fetch(`${API_BASE}/rooms/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to create room');
    return res.json();
  },

  async joinRoom(code: string): Promise<JoinRoomResponse> {
    const res = await fetch(`${API_BASE}/rooms/${code}/join/`);
    if (!res.ok) throw new Error('Room not found');
    return res.json();
  },

  async getRoomMessages(code: string): Promise<MessagesResponse> {
    const res = await fetch(`${API_BASE}/rooms/${code}/messages/`);
    if (!res.ok) throw new Error('Messages not available');
    return res.json();
  },

  async healthCheck(): Promise<HealthCheckResponse> {
    const res = await fetch(`${API_BASE}/health/`);
    if (!res.ok) throw new Error('Backend unreachable');
    return res.json();
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
