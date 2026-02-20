interface ConfidenceRingProps {
  confidence: number; // 0 to 1
  size?: number;
}

const ConfidenceRing = ({ confidence, size = 28 }: ConfidenceRingProps) => {
  const strokeWidth = 2.5;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - confidence * circumference;

  return (
    <div className="flex items-center gap-1.5">
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="hsl(var(--muted))"
          strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="hsl(var(--secondary))"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-700 ease-out"
        />
      </svg>
      <span className="text-[10px] font-medium text-muted-foreground">
        {Math.round(confidence * 100)}%
      </span>
    </div>
  );
};

export default ConfidenceRing;
