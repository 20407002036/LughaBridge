import { AnimatePresence, motion } from 'framer-motion';
import { Send } from 'lucide-react';
import { useState } from 'react';
import MicButton from './MicButton';
import WaveformVisualizer from './WaveformVisualizer';
import VoiceModeToggle from './VoiceModeToggle';
import type { SystemState } from '@/data/mockMessages';

interface VoiceInputBarProps {
  state: SystemState;
  onMicPress: () => void;
  voiceMode: boolean;
  onToggleVoice: (val: boolean) => void;
  onSendText?: (text: string, language: string) => void;
  sourceLanguage?: string;
  targetLanguage?: string;
}

const VoiceInputBar = ({ 
  state, 
  onMicPress, 
  voiceMode, 
  onToggleVoice,
  onSendText,
  sourceLanguage = 'kikuyu',
  targetLanguage = 'english',
}: VoiceInputBarProps) => {
  const isRecording = state === 'listening';
  const isProcessing = state === 'transcribing' || state === 'translating';
  
  const [textInput, setTextInput] = useState('');
  const [textLanguage, setTextLanguage] = useState(sourceLanguage);

  const handleSendText = () => {
    if (textInput.trim() && onSendText) {
      onSendText(textInput.trim(), textLanguage);
      setTextInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendText();
    }
  };

  return (
    <div className="sticky bottom-0 z-30 w-full pb-6 pt-4 bg-gradient-to-t from-white/30 via-white/20 to-transparent backdrop-blur-sm">
      <div className="max-w-lg mx-auto px-4 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <VoiceModeToggle voiceMode={voiceMode} onToggle={onToggleVoice} />
          <span className="text-[11px] text-muted-foreground font-medium tracking-wide">
            {voiceMode ? 'Voice mode' : 'Typing mode'}
          </span>
        </div>

        <AnimatePresence mode="wait">
          {voiceMode ? (
            <motion.div
              key="voice"
              initial={{ opacity: 0, scale: 0.98, y: 6 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: 6 }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
              className="bg-white/45 backdrop-blur-xl border border-white/60 rounded-2xl shadow-sm px-4 py-3"
            >
              <div className="flex flex-col items-center gap-3">
                <div className="relative">
                  {isRecording && (
                    <span className="absolute inset-[-6px] block rounded-full animate-wave-ring" aria-hidden />
                  )}
                  <MicButton state={state} onPress={onMicPress} />
                </div>
                <div className="w-full">
                  <WaveformVisualizer active={isRecording && !isProcessing} />
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="typing"
              initial={{ opacity: 0, scale: 0.98, y: 6 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: 6 }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
              className="bg-white/45 backdrop-blur-xl border border-white/60 rounded-2xl shadow-sm overflow-hidden"
            >
              <div className="px-4 py-3 space-y-3">
                {/* Language selector */}
                <div className="flex items-center gap-2">
                  <label htmlFor="text-language" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Language:
                  </label>
                  <select
                    id="text-language"
                    value={textLanguage}
                    onChange={(e) => setTextLanguage(e.target.value)}
                    className="flex-1 text-sm px-3 py-1.5 bg-white/60 border border-white/70 rounded-lg focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] transition-all"
                  >
                    <option value={sourceLanguage}>{sourceLanguage.charAt(0).toUpperCase() + sourceLanguage.slice(1)}</option>
                    <option value={targetLanguage}>{targetLanguage.charAt(0).toUpperCase() + targetLanguage.slice(1)}</option>
                  </select>
                </div>

                {/* Text input */}
                <div className="flex items-end gap-2">
                  <input
                    type="text"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    className="flex-1 text-sm px-4 py-2.5 bg-white/60 border border-white/70 rounded-xl focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] transition-all"
                  />
                  <button
                    onClick={handleSendText}
                    disabled={!textInput.trim() || isProcessing}
                    className="flex items-center justify-center w-10 h-10 bg-[hsl(var(--primary))] text-white rounded-xl hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    <Send size={18} />
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default VoiceInputBar;
