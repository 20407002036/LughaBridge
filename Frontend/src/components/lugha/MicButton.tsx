import { motion } from 'framer-motion';
import type { SystemState } from '@/data/mockMessages';

interface MicButtonProps {
  state: SystemState;
  onPress: () => void;
}

const stateLabels: Record<SystemState, string> = {
  idle: 'Tap to Speak',
  listening: 'Listening…',
  transcribing: 'Transcribing…',
  translating: 'Translating…',
  completed: 'Tap to Speak',
  error: 'Try Again',
};

const MicButton = ({ state, onPress }: MicButtonProps) => {
  const isRecording = state === 'listening';
  const isProcessing = state === 'transcribing' || state === 'translating';

  return (
    <div className="flex flex-col items-center gap-3">
      <motion.span
        key={state}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-xs font-medium text-muted-foreground tracking-wide"
      >
        {stateLabels[state]}
      </motion.span>
      <button
        onClick={onPress}
        disabled={isProcessing}
        className={`
          relative flex items-center justify-center w-16 h-16 rounded-full transition-all duration-300
          ${isRecording ? 'bg-secondary text-white glow-emerald animate-pulse-glow' : ''}
          ${!isRecording && !isProcessing ? 'bg-primary text-white glow-gold-subtle animate-mic-idle' : ''}
          ${isProcessing ? 'bg-white/60 backdrop-blur-sm border border-white/80 shadow-sm' : ''}
          disabled:cursor-wait
        `}
      >
        {/* Waveform bars when listening */}
        {isRecording ? (
          <div className="flex items-center gap-[3px]">
            {[0, 1, 2, 3, 4].map((i) => (
              <motion.div
                key={i}
                className="w-[3px] rounded-full bg-foreground"
                animate={{ height: [4, 16, 4] }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: 'easeInOut',
                }}
              />
            ))}
          </div>
        ) : (
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            className={isProcessing ? 'text-muted-foreground' : 'text-primary-foreground'}
          >
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" x2="12" y1="19" y2="22" />
          </svg>
        )}
      </button>
    </div>
  );
};

export default MicButton;
