import { AnimatePresence, motion } from 'framer-motion';
import MicButton from './MicButton';
import WaveformVisualizer from './WaveformVisualizer';
import VoiceModeToggle from './VoiceModeToggle';
import type { SystemState } from '@/data/mockMessages';

interface VoiceInputBarProps {
  state: SystemState;
  onMicPress: () => void;
  voiceMode: boolean;
  onToggleVoice: (val: boolean) => void;
}

const VoiceInputBar = ({ state, onMicPress, voiceMode, onToggleVoice }: VoiceInputBarProps) => {
  const isRecording = state === 'listening';
  const isProcessing = state === 'transcribing' || state === 'translating';

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
              className="bg-white/45 backdrop-blur-xl border border-white/60 rounded-2xl shadow-sm px-4 py-3"
            >
              <div className="flex items-center justify-between gap-3">
                <div className="space-y-1">
                  <p className="text-sm font-semibold text-foreground">Typing mode</p>
                  <p className="text-xs text-muted-foreground">Switch to voice to speak and see the live waveform.</p>
                </div>
                <button
                  onClick={() => onToggleVoice(true)}
                  className="text-xs font-semibold text-[hsl(var(--primary))] hover:underline"
                >
                  Enable voice
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default VoiceInputBar;
