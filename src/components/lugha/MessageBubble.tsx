import { useState, useRef, useEffect } from 'react';
import { MoreVertical, Volume2, Copy, Share2, Mic } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { ChatMessage } from '@/data/mockMessages';
import ConfidenceRing from './ConfidenceRing';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble = ({ message }: MessageBubbleProps) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const isLeft = message.sender === 'A';

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    if (menuOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [menuOpen]);

  const time = message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const menuItems = [
    { icon: Volume2, label: 'Read Original Aloud' },
    { icon: Volume2, label: 'Read Translation Aloud' },
    { icon: Mic, label: 'Change Voice' },
    { icon: Copy, label: 'Copy Text' },
    { icon: Share2, label: 'Share' },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={`flex ${isLeft ? 'justify-start' : 'justify-end'} px-4`}
    >
      <div className={`relative max-w-[85%] sm:max-w-[70%] ${isLeft ? 'glass-bubble-left' : 'glass-bubble-right'} p-4 space-y-2`}>
        {/* Language badge */}
        <div className="flex items-center justify-between">
          <span className={`text-xs font-semibold uppercase tracking-widest ${
            message.originalLanguage === 'Kikuyu' ? 'text-gold' : 'text-emerald-accent'
          }`}>
            {message.originalLanguage}
          </span>
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="p-1 rounded-full hover:bg-black/5 transition-colors text-muted-foreground"
            >
              <MoreVertical size={14} />
            </button>
            <AnimatePresence>
              {menuOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 8, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 8, scale: 0.98 }}
                  transition={{ duration: 0.15 }}
                  className={`absolute ${isLeft ? 'left-0' : 'right-0'} top-8 z-50 w-52 rounded-xl bg-white/80 backdrop-blur-xl border border-white/90 p-1.5 shadow-lg`}
                >
                  {menuItems.map((item) => (
                    <button
                      key={item.label}
                      onClick={() => setMenuOpen(false)}
                      className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-xs text-foreground/80 hover:bg-black/5 transition-colors"
                    >
                      <item.icon size={14} strokeWidth={1.5} className="text-muted-foreground" />
                      {item.label}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Original text */}
        <p className="text-sm font-medium leading-relaxed text-foreground">
          {message.originalText}
        </p>

        {/* Translated text */}
        <p className="text-xs leading-relaxed text-muted-foreground">
          {message.translatedText}
        </p>

        {/* Footer: confidence + timestamp */}
        <div className="flex items-center justify-between pt-1">
          <ConfidenceRing confidence={message.confidence} />
          <span className="text-[10px] text-muted-foreground/60">{time}</span>
        </div>
      </div>
    </motion.div>
  );
};

export default MessageBubble;
