import { useRef, useEffect } from 'react';
import { Mic, Keyboard, Send, MoreVertical } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { ChatMessage, SystemState } from '@/data/mockMessages';
import MessageBubble from './MessageBubble';
import MicButton from './MicButton';

interface ChatLayoutProProps {
  messages: ChatMessage[];
  systemState: SystemState;
  demoMode: boolean;
  onDemoToggle: (val: boolean) => void;
  onMicPress: () => void;
}

const ChatLayoutPro = ({
  messages,
  systemState,
  demoMode,
  onDemoToggle,
  onMicPress,
}: ChatLayoutProProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="h-[100dvh] bg-bridge-dark text-white flex flex-col overflow-hidden relative max-w-lg mx-auto">
      {/* Background Radial Glow */}
      <div className="absolute bottom-[-20%] left-1/2 -translate-x-1/2 w-[400px] h-[400px] mic-glow pointer-events-none" />

      {/* 1. Header with Brand and User Info */}
      <header className="flex items-center justify-between px-4 py-3 z-10 border-b border-white/10">
        {/* Brand and Logo - Far Left */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-bridge-teal to-[#1fb5a0] flex items-center justify-center">
            <span className="text-white text-xs font-bold">L</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-white">LughaBridge</span>
            <span className="text-[10px] text-bridge-teal">Live</span>
          </div>
        </div>

        {/* Language Pair Switcher - Center */}
        <div className="glass-panel rounded-full flex items-center gap-2 px-3 py-1.5">
          <span className="text-bridge-teal text-xs font-medium">Gĩkũyũ</span>
          <div className="w-5 h-5 rounded-full bg-bridge-teal/10 flex items-center justify-center text-[9px] text-bridge-teal">
            ⇄
          </div>
          <span className="text-white/70 text-xs">English</span>
        </div>

        {/* Connected Status + Avatar - Far Right */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 glass-panel rounded-full px-3 py-1.5">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
            <span className="text-[10px] text-white/70">Connected</span>
          </div>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-bridge-gold to-amber-600 flex items-center justify-center border border-white/20 cursor-pointer hover:border-bridge-teal transition-colors">
            <span className="text-white text-xs font-bold">U</span>
          </div>
        </div>
      </header>

      {/* Demo Toggle Button */}
      <div className="px-4 py-2 z-10 flex justify-center">
        <button
          onClick={() => onDemoToggle(!demoMode)}
          className={`px-4 py-1.5 rounded-full text-xs font-medium transition-all ${
            demoMode
              ? 'bg-bridge-teal/20 border border-bridge-teal text-bridge-teal'
              : 'glass-panel text-white/60 hover:text-white/80'
          }`}
        >
          {demoMode ? '● Demo Active' : 'Demo'}
        </button>
      </div>

      {/* 2. Chat Bubbles (The Stream) */}
      <div
        ref={scrollRef}
        className="flex-1 space-y-4 overflow-y-auto scrollbar-none z-10 px-4 py-4"
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <div className="w-14 h-14 rounded-full bg-bridge-glass flex items-center justify-center">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#2DD4BF"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" x2="12" y1="19" y2="22" />
              </svg>
            </div>
            <p className="text-xs text-white/60 font-medium">Tap the microphone to begin</p>
            <p className="text-[10px] text-white/40">Speak in Kikuyu or English</p>
          </div>
        ) : (
          messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)
        )}
      </div>

      {/* 3. Footer: Typing + Voice Waves */}
      <div className="relative pt-4 pb-6 px-4 z-10">
        {/* Animated Voice Waves with SVG */}
        <div className="absolute bottom-24 left-0 w-full h-16 overflow-hidden pointer-events-none">
          <svg viewBox="0 0 400 100" className="w-full h-full opacity-50">
            <path
              d="M0 50 Q100 20 200 50 T400 50"
              fill="none"
              stroke="#2DD4BF"
              strokeWidth="2"
              className="animate-wave"
            />
            <path
              d="M0 50 Q100 80 200 50 T400 50"
              fill="none"
              stroke="#C5A358"
              strokeWidth="1"
              className="animate-wave opacity-40"
              style={{ animationDelay: '-2s' }}
            />
          </svg>
        </div>

        {/* Typing Bar */}
        <div className="glass-panel rounded-full flex items-center px-4 py-3 mb-4">
          <Keyboard className="text-white/30 mr-2 flex-shrink-0" size={18} />
          <input
            type="text"
            placeholder="Type..."
            className="bg-transparent flex-1 outline-none text-sm placeholder:text-white/20 text-white"
          />
          <Send className="text-bridge-teal opacity-60 cursor-pointer flex-shrink-0" size={16} />
        </div>

        {/* The Hero: Microphone */}
        <div className="flex justify-center pb-2">
          <MicButton state={systemState} onPress={onMicPress} />
        </div>
      </div>
    </div>
  );
};

export default ChatLayoutPro;
