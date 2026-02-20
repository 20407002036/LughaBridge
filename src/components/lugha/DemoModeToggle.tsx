import { Switch } from '@/components/ui/switch';
import { Sparkles } from 'lucide-react';

interface DemoModeToggleProps {
  enabled: boolean;
  onToggle: (val: boolean) => void;
}

const DemoModeToggle = ({ enabled, onToggle }: DemoModeToggleProps) => {
  return (
    <button
      onClick={() => onToggle(!enabled)}
      className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/60 backdrop-blur-sm border border-white/80 shadow-sm text-xs font-medium text-muted-foreground hover:text-foreground transition-colors"
    >
      <Sparkles size={14} className={enabled ? 'text-[hsl(var(--primary))]' : ''} />
      <span>Demo</span>
      <Switch checked={enabled} onCheckedChange={onToggle} className="scale-75" />
    </button>
  );
};

export default DemoModeToggle;
