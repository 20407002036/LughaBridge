import { useEffect, useRef } from 'react';

interface WaveformVisualizerProps {
  active: boolean;
  height?: number;
  barCount?: number;
}

const WaveformVisualizer = ({ active, height = 72, barCount = 40 }: WaveformVisualizerProps) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number>();
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array<ArrayBuffer> | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const stop = () => {
    if (animationRef.current) cancelAnimationFrame(animationRef.current);
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (sourceRef.current) {
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.suspend().catch(() => undefined);
    }
  };

  const drawIdle = (ctx: CanvasRenderingContext2D, w: number, h: number) => {
    ctx.clearRect(0, 0, w, h);
    const lineY = h / 2;
    ctx.strokeStyle = 'rgba(0,0,0,0.06)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, lineY);
    ctx.lineTo(w, lineY);
    ctx.stroke();
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = height * dpr;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.scale(dpr, dpr);

    if (!active) {
      drawIdle(ctx, rect.width, height);
      stop();
      return () => stop();
    }

    let cancelled = false;

    const start = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        streamRef.current = stream;
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        audioContextRef.current = audioContext;
        const source = audioContext.createMediaStreamSource(stream);
        sourceRef.current = source;
        const analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        analyser.smoothingTimeConstant = 0.7;
        analyserRef.current = analyser;
        const bufferLength = analyser.frequencyBinCount;
        dataArrayRef.current = new Uint8Array(bufferLength) as Uint8Array<ArrayBuffer>;
        source.connect(analyser);

        const styles = getComputedStyle(document.documentElement);
        const from = styles.getPropertyValue('--wave-from') || '250 70% 70%';
        const to = styles.getPropertyValue('--wave-to') || '230 75% 60%';
        const gradient = ctx.createLinearGradient(0, 0, rect.width, 0);
        gradient.addColorStop(0, `hsl(${from.trim()})`);
        gradient.addColorStop(1, `hsl(${to.trim()})`);

        const render = () => {
          if (cancelled) return;
          animationRef.current = requestAnimationFrame(render);
          if (!analyserRef.current || !dataArrayRef.current) return;
          const dataArray = dataArrayRef.current as Uint8Array;
          analyserRef.current.getByteTimeDomainData(dataArray as unknown as Uint8Array<ArrayBuffer>);
          ctx.clearRect(0, 0, rect.width, height);

          const bars = barCount;
          const slice = Math.floor(dataArray.length / bars);
          const barWidth = rect.width / bars;

          for (let i = 0; i < bars; i++) {
            const v = dataArray[i * slice] / 128.0 - 1.0; // -1..1
            const magnitude = Math.max(Math.min(Math.abs(v), 1), 0.05);
            const barHeight = magnitude * (height * 0.9);
            const x = i * barWidth;
            const y = (height - barHeight) / 2;
            ctx.fillStyle = gradient;
            ctx.fillRect(x, y, barWidth * 0.7, barHeight);
            ctx.globalAlpha = 0.9;
          }
        };

        render();
      } catch (e) {
        drawIdle(ctx, rect.width, height);
      }
    };

    start();

    return () => {
      cancelled = true;
      stop();
    };
  }, [active, barCount, height]);

  return (
    <div className="w-full">
      <canvas
        ref={canvasRef}
        className="w-full" 
        style={{ height }}
        aria-hidden
      />
    </div>
  );
};

export default WaveformVisualizer;
