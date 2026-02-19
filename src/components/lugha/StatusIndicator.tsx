import { motion } from 'framer-motion';

type Status = 'idle' | 'listening' | 'transcribing' | 'translating' | 'completed' | 'error';

const statusConfig: Record<Status, { label: string; color: string; pulse: boolean }> = {
  idle: { label: 'Connected', color: 'bg-emerald-light', pulse: false },
  listening: { label: 'Listening to your voice…', color: 'bg-emerald-light', pulse: true },
  transcribing: { label: 'Transcribing with care…', color: 'bg-gold', pulse: true },
  translating: { label: 'Translating…', color: 'bg-gold', pulse: true },
  completed: { label: 'Connected', color: 'bg-emerald-light', pulse: false },
  error: { label: 'Connection lost', color: 'bg-destructive', pulse: false },
};

interface StatusIndicatorProps {
  status: Status;
}

const StatusIndicator = ({ status }: StatusIndicatorProps) => {
  const config = statusConfig[status];

  return (
    <motion.div
      className="flex items-center gap-2"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      key={status}
    >
      <span className={`inline-block h-2 w-2 rounded-full ${config.color} ${config.pulse ? 'animate-status-pulse' : ''}`} />
      <span className="text-xs font-medium text-muted-foreground tracking-wide">
        {config.label}
      </span>
    </motion.div>
  );
};

export default StatusIndicator;
