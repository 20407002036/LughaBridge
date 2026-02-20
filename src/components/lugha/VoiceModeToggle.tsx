import { motion } from 'framer-motion';
import { Mic, Keyboard } from 'lucide-react';

interface VoiceModeToggleProps {
  voiceMode: boolean;
  onToggle: (next: boolean) => void;
}

const VoiceModeToggle = ({ voiceMode, onToggle }: VoiceModeToggleProps) => {
  return (
    <button
      onClick={() => onToggle(!voiceMode)}
      className="relative inline-flex items-center gap-2 rounded-full bg-white/60 backdrop-blur-sm border border-white/70 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground transition-all shadow-sm"
    >
      <div className="relative w-10 h-6 bg-white/70 border border-white/80 rounded-full shadow-inner overflow-hidden">
        <motion.div
          layout
          transition={{ type: 'spring', stiffness: 260, damping: 24 }}
          className="absolute top-[2px] left-[2px] w-[20px] h-[20px] rounded-full bg-[hsl(var(--primary))] shadow-sm"
          animate={{ x: voiceMode ? 18 : 0, scale: 1 }}
        />
      </div>
      <motion.div
        key={voiceMode ? 'voice' : 'type'}
        initial={{ opacity: 0.6, scale: 0.98, y: 2 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
        className="flex items-center gap-1"
      >
        {voiceMode ? (
          <Mic size={14} className="text-[hsl(var(--primary))]" />
        ) : (
          <Keyboard size={14} className="text-[hsl(var(--secondary))]" />
        )}
        <span>{voiceMode ? 'Voice' : 'Typing'}</span>
      </motion.div>
    </button>
  );
};

export default VoiceModeToggle;
