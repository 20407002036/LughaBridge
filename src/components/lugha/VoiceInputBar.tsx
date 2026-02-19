import MicButton from './MicButton';
import type { SystemState } from '@/data/mockMessages';

interface VoiceInputBarProps {
  state: SystemState;
  onMicPress: () => void;
}

const VoiceInputBar = ({ state, onMicPress }: VoiceInputBarProps) => {
  return (
    <div className="sticky bottom-0 z-30 w-full pb-6 pt-4 bg-gradient-to-t from-background via-background/95 to-transparent">
      <div className="flex justify-center">
        <MicButton state={state} onPress={onMicPress} />
      </div>
    </div>
  );
};

export default VoiceInputBar;
