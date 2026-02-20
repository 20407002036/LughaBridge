import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Hash } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { api } from '@/services/api';

const JoinRoom = () => {
  const navigate = useNavigate();
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleJoin = async () => {
    const trimmed = code.trim().toUpperCase();
    if (!trimmed) {
      setError('Please enter a room code');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await api.joinRoom(trimmed);
      navigate(`/room/${trimmed}`);
    } catch {
      setError('Room not found. Check the code and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[100dvh] flex flex-col bg-gradient-to-br from-indigo-100/60 via-slate-100/40 to-teal-100/50">
      {/* Decorative blurs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-teal-300/25 blur-3xl" />
        <div className="absolute bottom-1/4 -left-24 w-80 h-80 rounded-full bg-indigo-300/30 blur-3xl" />
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
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Join a Room</h2>
              <p className="text-sm text-muted-foreground">Enter the room code shared with you</p>
            </div>

            {/* Code Input */}
            <div className="space-y-3">
              <div className="relative">
                <Hash size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="text"
                  value={code}
                  onChange={(e) => {
                    setCode(e.target.value.toUpperCase());
                    setError(null);
                  }}
                  onKeyDown={(e) => e.key === 'Enter' && handleJoin()}
                  placeholder="LUGHA-XXXX"
                  maxLength={12}
                  className="w-full h-14 pl-11 pr-4 text-center text-xl font-mono font-bold tracking-widest bg-white/50 backdrop-blur-sm border border-white/70 rounded-2xl text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:ring-2 focus:ring-[hsl(var(--ring))] focus:ring-offset-2 focus:ring-offset-transparent transition-all"
                />
              </div>

              {error && (
                <p className="text-sm text-destructive text-center font-medium">{error}</p>
              )}
            </div>

            <Button
              onClick={handleJoin}
              disabled={loading || !code.trim()}
              className="w-full h-13 text-base font-semibold rounded-2xl gap-2"
            >
              {loading ? 'Joining…' : 'Join Room'}
              <ArrowRight size={18} />
            </Button>

            {/* Divider */}
            <div className="flex items-center gap-3">
              <div className="flex-1 h-px bg-black/5" />
              <span className="text-xs font-medium text-muted-foreground">or</span>
              <div className="flex-1 h-px bg-black/5" />
            </div>

            <Button
              onClick={() => navigate('/create')}
              variant="outline"
              className="w-full h-12 text-sm font-medium rounded-2xl bg-white/40 backdrop-blur-sm border-white/60 hover:bg-white/60"
            >
              Create your own room instead
            </Button>
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default JoinRoom;
