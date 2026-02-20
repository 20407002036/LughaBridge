import { useRef, useEffect } from 'react';
import { ArrowLeft, Copy } from 'lucide-react';
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
  roomCode?: string;
  onBack?: () => void;
  voiceMode: boolean;
  onToggleVoice: (val: boolean) => void;
}

const ChatLayout = ({ messages, systemState, demoMode, onDemoToggle, onMicPress, roomCode, onBack, voiceMode, onToggleVoice }: ChatLayoutProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-[100dvh] max-w-lg mx-auto relative">
      {/* Glass background with colored blurs */}
      <div className="fixed inset-0 bg-gradient-to-br from-indigo-100/60 via-slate-100/40 to-teal-100/50 -z-20" />
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-indigo-300/30 blur-3xl" />
        <div className="absolute top-1/2 -right-24 w-72 h-72 rounded-full bg-teal-300/20 blur-3xl" />
        <div className="absolute bottom-0 left-1/4 w-64 h-64 rounded-full bg-purple-200/15 blur-3xl" />
      </div>
      {systemState === 'idle' && (
        <div className="ambient-layer animate-ambient-float" />
      )}

      {/* Header */}
      <header className="sticky top-0 z-30 flex items-center justify-between px-5 py-3 bg-white/40 backdrop-blur-2xl border-b border-white/50 shadow-sm">
        <div className="flex items-center gap-3">
          {onBack && (
            <button onClick={onBack} className="p-1.5 -ml-1 rounded-xl hover:bg-black/5 transition-colors">
              <ArrowLeft size={18} className="text-foreground" />
            </button>
          )}
          <div>
            <h1 className="text-lg font-bold tracking-tight text-foreground">
              Lugha<span className="text-[hsl(var(--primary))]">Bridge</span>
            </h1>
            {roomCode && (
              <button
                onClick={() => navigator.clipboard.writeText(roomCode)}
                className="flex items-center gap-1 text-[10px] text-muted-foreground tracking-wide mt-0.5 hover:text-foreground transition-colors"
              >
                Room: <span className="font-mono font-semibold">{roomCode}</span>
                <Copy size={10} />
              </button>
            )}
          </div>
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
            <div className="w-16 h-16 rounded-full bg-white/40 backdrop-blur-xl border border-white/50 shadow-sm flex items-center justify-center">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="hsl(var(--primary))" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
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
      <VoiceInputBar state={systemState} onMicPress={onMicPress} voiceMode={voiceMode} onToggleVoice={onToggleVoice} />
    </div>
  );
};

export default ChatLayout;
