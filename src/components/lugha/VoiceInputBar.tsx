import { useState } from 'react';
import { Keyboard, Send } from 'lucide-react';
import MicButton from './MicButton';
import type { SystemState } from '@/data/mockMessages';

interface VoiceInputBarProps {
  state: SystemState;
  onMicPress: () => void;
}

const VoiceInputBar = ({ state, onMicPress }: VoiceInputBarProps) => {
  const [inputText, setInputText] = useState('');

  return (
    <div className="sticky bottom-0 z-30 w-full pb-6 pt-4 bg-gradient-to-t from-bridge-dark via-bridge-dark/80 to-transparent px-6">
      {/* Typing Input Bar */}
      <div className="flex items-center bg-bridge-glass backdrop-blur-xl border border-white/20 rounded-full px-5 py-3 mb-6 group focus-within:border-bridge-teal/50 transition-all">
        <Keyboard size={20} className="text-white/40 mr-3" />
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type a message..."
          className="bg-transparent flex-1 outline-none text-sm placeholder:text-white/30 text-white"
        />
        <button className="p-1 text-bridge-teal opacity-50 group-focus-within:opacity-100 hover:opacity-100 transition-opacity">
          <Send size={20} />
        </button>
      </div>

      {/* Voice Visualization & Mic */}
      <div className="relative flex flex-col items-center">
        {/* Glowing Waves with animation */}
        <div className="absolute w-full h-24 flex items-center justify-center opacity-40">
          <div className="w-full h-[2px] bg-gradient-to-r from-transparent via-bridge-teal to-transparent blur-[1px] animate-wave"></div>
          <div className="absolute w-3/4 h-[1px] bg-gradient-to-r from-transparent via-bridge-gold to-transparent blur-[2px] mt-4 opacity-50 animate-wave" style={{ animationDelay: '0.5s' }}></div>
        </div>

        {/* Mic Button */}
        <div>
          <MicButton state={state} onPress={onMicPress} />
        </div>
      </div>
    </div>
  );
};

export default VoiceInputBar;
