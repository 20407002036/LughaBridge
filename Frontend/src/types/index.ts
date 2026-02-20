export type Language = 'Kikuyu' | 'English';
export type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error';
export type SystemState = 'idle' | 'listening' | 'transcribing' | 'translating' | 'completed' | 'error';
export type MessageSender = 'A' | 'B';

export interface Room {
  code: string;
  sourceLanguage: Language;
  targetLanguage: Language;
  createdAt: Date;
  participantCount: number;
}

export interface ChatMessage {
  id: string;
  sender: MessageSender;
  originalText: string;
  translatedText: string;
  originalLanguage: Language;
  timestamp: Date;
  confidence: number;
}

export interface CreateRoomPayload {
  source_lang: string;
  target_lang: string;
}

export interface CreateRoomResponse {
  room_code: string;
  ws_url: string;
}

export interface JoinRoomResponse {
  room_code: string;
  source_language: string;
  target_language: string;
  messages: ChatMessage[];
}

export interface HealthCheckResponse {
  status: string;
  demo_mode: boolean;
}
