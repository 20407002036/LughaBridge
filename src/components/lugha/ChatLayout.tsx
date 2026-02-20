import { useRef, useEffect } from 'react';
import type { ChatMessage, SystemState } from '@/data/mockMessages';
import MessageBubble from './MessageBubble';
import VoiceInputBar from './VoiceInputBar';
import StatusIndicator from './StatusIndicator';
import DemoModeToggle from './DemoModeToggle';

interface ChatLayoutProps {
  messages: ChatMessage[];
  systemState: SystemState;
  demoMode: boolean;
  onDemoToggle: (val: boolean) => void;
  onMicPress: () => void;
}

const ChatLayout = ({ messages, systemState, demoMode, onDemoToggle, onMicPress }: ChatLayoutProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-[100dvh] max-w-lg mx-auto bg-bridge-dark">
      {/* Header */}
      <header className="sticky top-0 z-30 pt-12 pb-4 px-6 text-center">
        <h1 className="text-xl font-semibold mb-4 text-white">
          Gĩkũyũ<span className="text-bridge-teal">Bridge</span>
        </h1>
        <div className="inline-flex items-center bg-bridge-glass backdrop-blur-md border border-white/20 rounded-full px-4 py-2 text-sm">
          <span className="text-bridge-teal">Gĩkũyũ</span>
          <span className="mx-3 opacity-50">⇄</span>
          <span className="text-white">English</span>
        </div>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto py-4 space-y-3 scrollbar-none">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-8 gap-3">
            <div className="w-16 h-16 rounded-full bg-bridge-glass flex items-center justify-center">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2DD4BF" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
            </div>
            <p className="text-sm text-white/60 font-medium">
              Tap the microphone to begin
            </p>
            <p className="text-xs text-white/40">
              Speak in Kikuyu or English, or type a message
            </p>
          </div>
        )}
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>

      {/* Voice Input */}
      <VoiceInputBar state={systemState} onMicPress={onMicPress} />
    </div>
  );
};

export default ChatLayout;
