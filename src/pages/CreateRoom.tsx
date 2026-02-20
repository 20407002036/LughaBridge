import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Globe, ArrowRight, Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import type { Language } from '@/types';
import { api } from '@/services/api';

const languages: Language[] = ['Kikuyu', 'English'];

const CreateRoom = () => {
  const navigate = useNavigate();
  const [source, setSource] = useState<Language>('Kikuyu');
  const [target, setTarget] = useState<Language>('English');
  const [loading, setLoading] = useState(false);
  const [roomCode, setRoomCode] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreate = async () => {
    if (source === target) {
      setError('Source and target languages must be different');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.createRoom({
        source_language: source,
        target_language: target,
      });
      setRoomCode(res.room_code);
    } catch {
      setError('Failed to create room. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!roomCode) return;
    await navigator.clipboard.writeText(roomCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleEnter = () => {
    if (roomCode) navigate(`/room/${roomCode}`);
  };

  return (
    <div className="min-h-[100dvh] flex flex-col bg-gradient-to-br from-indigo-100/60 via-slate-100/40 to-teal-100/50">
      {/* Decorative blurs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-indigo-300/30 blur-3xl" />
        <div className="absolute top-1/3 -right-24 w-80 h-80 rounded-full bg-teal-300/25 blur-3xl" />
      </div>

      {/* Header */}
      <header className="w-full px-6 py-5">
        <div className="max-w-lg mx-auto">
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft size={16} />
            Back
          </button>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 pb-12">
        <div className="max-w-lg w-full space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/40 backdrop-blur-2xl border border-white/60 rounded-3xl p-8 shadow-lg space-y-6"
          >
            <div className="text-center space-y-1">
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Create a Room</h2>
              <p className="text-sm text-muted-foreground">Set your language pair and share the code</p>
            </div>

            {/* Language Selectors */}
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Source Language
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {languages.map((lang) => (
                    <button
                      key={`src-${lang}`}
                      onClick={() => setSource(lang)}
                      className={`flex items-center justify-center gap-2 h-12 rounded-xl text-sm font-medium transition-all ${
                        source === lang
                          ? 'bg-[hsl(var(--primary))] text-white shadow-md'
                          : 'bg-white/50 backdrop-blur-sm border border-white/70 text-foreground hover:bg-white/70'
                      }`}
                    >
                      <Globe size={16} />
                      {lang}
                    </button>
                  ))}
                </div>
              </div>

              {/* Arrow */}
              <div className="flex justify-center">
                <div className="w-10 h-10 rounded-full bg-white/50 backdrop-blur-sm border border-white/60 flex items-center justify-center">
                  <ArrowRight size={18} className="text-muted-foreground rotate-90" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Target Language
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {languages.map((lang) => (
                    <button
                      key={`tgt-${lang}`}
                      onClick={() => setTarget(lang)}
                      className={`flex items-center justify-center gap-2 h-12 rounded-xl text-sm font-medium transition-all ${
                        target === lang
                          ? 'bg-[hsl(var(--secondary))] text-white shadow-md'
                          : 'bg-white/50 backdrop-blur-sm border border-white/70 text-foreground hover:bg-white/70'
                      }`}
                    >
                      <Globe size={16} />
                      {lang}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {error && (
              <p className="text-sm text-destructive text-center font-medium">{error}</p>
            )}

            {!roomCode ? (
              <Button
                onClick={handleCreate}
                disabled={loading}
                className="w-full h-13 text-base font-semibold rounded-2xl"
              >
                {loading ? 'Creating…' : 'Create Room'}
              </Button>
            ) : (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-4"
              >
                {/* Room Code Display */}
                <div className="bg-white/50 backdrop-blur-sm border border-white/70 rounded-2xl p-5 text-center space-y-2">
                  <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Your Room Code
                  </p>
                  <p className="text-3xl font-bold tracking-widest text-foreground font-mono">
                    {roomCode}
                  </p>
                  <button
                    onClick={handleCopy}
                    className="inline-flex items-center gap-1.5 text-xs font-medium text-[hsl(var(--primary))] hover:underline"
                  >
                    {copied ? <Check size={14} /> : <Copy size={14} />}
                    {copied ? 'Copied!' : 'Copy code'}
                  </button>
                </div>

                <Button
                  onClick={handleEnter}
                  className="w-full h-13 text-base font-semibold rounded-2xl gap-2"
                >
                  Enter Room
                  <ArrowRight size={18} />
                </Button>
              </motion.div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default CreateRoom;
