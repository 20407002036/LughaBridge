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
    <div className="flex flex-col h-[100dvh] max-w-lg mx-auto bg-background">
      {/* Header */}
      <header className="sticky top-0 z-30 flex items-center justify-between px-5 py-4 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div>
          <h1 className="text-lg font-bold tracking-tight text-foreground">
            Lugha<span className="text-gold">Bridge</span>
          </h1>
          <p className="text-[10px] text-muted-foreground tracking-wide mt-0.5">
            Real-Time Kikuyu ↔ English Translation
          </p>
        </div>
        <div className="flex items-center gap-3">
          <StatusIndicator status={systemState} />
          <DemoModeToggle enabled={demoMode} onToggle={onDemoToggle} />
        </div>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto py-4 space-y-3 scrollbar-none">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center px-8 gap-3">
            <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--gold))" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
            </div>
            <p className="text-sm text-muted-foreground font-medium">
              Tap the microphone to begin
            </p>
            <p className="text-xs text-muted-foreground/60">
              Speak in Kikuyu or English
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
