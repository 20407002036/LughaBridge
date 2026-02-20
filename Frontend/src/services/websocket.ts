import type { ChatMessage } from '@/data/mockMessages';

const WS_BASE = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

export type WSMessageType =
  | 'connection_established'
  | 'message_history'
  | 'chat_message'
  | 'translation_complete'
  | 'processing'
  | 'translation_progress'
  | 'participant_joined'
  | 'participant_left'
  | 'typing'
  | 'error'
  | 'pong';

export interface WSMessage {
  type: WSMessageType;
  [key: string]: any;
}

export interface VoiceMessagePayload {
  type: 'voice_message';
  message_id: string;
  audio_data: string; // base64
  language: string;
}

export interface TextMessagePayload {
  type: 'text_message';
  message_id: string;
  text: string;
  language: string;
}

export type WSEventCallback = (data: any) => void;

export class RoomWebSocket {
  private ws: WebSocket | null = null;
  private listeners: Map<WSMessageType | 'open' | 'close' | 'error', Set<WSEventCallback>> = new Map();
  private roomCode: string;
  private wsUrl: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  private isIntentionallyClosed = false;

  constructor(roomCode: string, wsBaseUrl?: string) {
    this.roomCode = roomCode;
    const baseUrl = wsBaseUrl || WS_BASE;
    this.wsUrl = `${baseUrl}/ws/room/${roomCode}/`;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.isIntentionallyClosed = false;
        this.ws = new WebSocket(this.wsUrl);

        this.ws.onopen = () => {
          console.log(`WebSocket connected to room: ${this.roomCode}`);
          this.reconnectAttempts = 0;
          this.emit('open', { roomCode: this.roomCode });
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data) as WSMessage;
            console.log('WS message received:', data.type, data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.emit('error', { error });
          reject(error);
        };

        this.ws.onclose = (event) => {
          console.log(`WebSocket disconnected (code: ${event.code})`);
          this.emit('close', { code: event.code, reason: event.reason });
          
          // Attempt reconnection if not intentionally closed
          if (!this.isIntentionallyClosed && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connect(), this.reconnectDelay);
          }
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  disconnect(): void {
    this.isIntentionallyClosed = true;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(data: VoiceMessagePayload | TextMessagePayload | { type: string; [key: string]: any }): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected');
      return;
    }

    try {
      this.ws.send(JSON.stringify(data));
      console.log('WS message sent:', data.type);
    } catch (error) {
      console.error('Error sending WebSocket message:', error);
    }
  }

  sendVoiceMessage(audioData: string, language: string): string {
    const messageId = this.generateMessageId();
    this.send({
      type: 'voice_message',
      message_id: messageId,
      audio_data: audioData,
      language: language,
    });
    return messageId;
  }

  sendTextMessage(text: string, language: string): string {
    const messageId = this.generateMessageId();
    this.send({
      type: 'text_message',
      message_id: messageId,
      text: text,
      language: language,
    });
    return messageId;
  }

  sendPing(): void {
    this.send({ type: 'ping' });
  }

  sendTyping(isTyping: boolean): void {
    this.send({ type: 'typing', is_typing: isTyping });
  }

  on(event: WSMessageType | 'open' | 'close' | 'error', callback: WSEventCallback): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: WSMessageType | 'open' | 'close' | 'error', callback: WSEventCallback): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback);
    }
  }

  private emit(event: string, data: any): void {
    const callbacks = this.listeners.get(event as any);
    if (callbacks) {
      callbacks.forEach((callback) => callback(data));
    }
  }

  private handleMessage(data: WSMessage): void {
    this.emit(data.type, data);
  }

  private generateMessageId(): string {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  getReadyState(): number | null {
    return this.ws?.readyState ?? null;
  }
}

// Helper function to convert Blob to base64
export async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = (reader.result as string).split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// Helper to normalize message from backend format to frontend format
export function normalizeMessage(msg: any): ChatMessage {
  return {
    id: msg.id || msg.message_id || `msg-${Date.now()}`,
    sender: (msg.sender as ChatMessage['sender']) ?? 'A',
    originalText: msg.original_text || msg.originalText || '',
    translatedText: msg.translated_text || msg.translatedText || '',
    originalLanguage: (msg.original_language || msg.originalLanguage || 'Kikuyu') as ChatMessage['originalLanguage'],
    timestamp: msg.timestamp ? new Date(msg.timestamp) : new Date(),
    confidence: typeof msg.confidence === 'number' ? msg.confidence : 0.9,
    audioData: msg.audio_data || msg.audioData,
  };
}
