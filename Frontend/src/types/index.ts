export type Language = 'Kikuyu' | 'Swahili' | 'English';
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
   senderChannelName?: string;
  originalText: string;
  translatedText: string;
  originalLanguage: Language;
  timestamp: Date;
  confidence: number;
   audioData?: string;
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
  source_language?: string;
  target_language?: string;
  source_lang?: string;
  target_lang?: string;
  messages?: ChatMessage[];
}

export interface HealthCheckResponse {
  status: string;
  demo_mode: boolean;
}

export type MessagesResponse = ChatMessage[];
