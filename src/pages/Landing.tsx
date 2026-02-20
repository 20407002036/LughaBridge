import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus, Users, Globe, Mic, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-[100dvh] flex flex-col bg-gradient-to-br from-indigo-100/60 via-slate-100/40 to-teal-100/50">
      {/* Decorative blurred circles for glass depth */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute -top-32 -left-32 w-96 h-96 rounded-full bg-indigo-300/30 blur-3xl" />
        <div className="absolute top-1/3 -right-24 w-80 h-80 rounded-full bg-teal-300/25 blur-3xl" />
        <div className="absolute bottom-0 left-1/4 w-72 h-72 rounded-full bg-purple-200/20 blur-3xl" />
      </div>

      {/* Header */}
      <header className="w-full px-6 py-5">
        <div className="max-w-lg mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold tracking-tight text-foreground">
            Lugha<span className="text-[hsl(var(--primary))]">Bridge</span>
          </h1>
          <span className="text-xs font-medium text-muted-foreground bg-white/50 backdrop-blur-sm border border-white/60 rounded-full px-3 py-1">
            v1.0
          </span>
        </div>
      </header>

      {/* Hero */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 pb-12">
        <div className="max-w-lg w-full space-y-8">
          {/* Hero Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white/40 backdrop-blur-2xl border border-white/60 rounded-3xl p-8 shadow-lg text-center space-y-5"
          >
            {/* Mic Icon */}
            <div className="mx-auto w-20 h-20 rounded-full bg-gradient-to-br from-[hsl(var(--primary))] to-[hsl(var(--accent))] flex items-center justify-center shadow-lg">
              <Mic className="w-9 h-9 text-white" strokeWidth={1.8} />
            </div>

            <div className="space-y-2">
              <h2 className="text-2xl font-bold text-foreground tracking-tight">
                Bridge Languages in Real-Time
              </h2>
              <p className="text-sm text-muted-foreground leading-relaxed max-w-xs mx-auto">
                Speak in Kikuyu or English and get instant, high-accuracy voice translation.
              </p>
            </div>

            {/* Feature pills */}
            <div className="flex flex-wrap justify-center gap-2">
              {[
                { icon: Globe, label: 'Kikuyu ↔ English' },
                { icon: Mic, label: 'Voice-first' },
                { icon: Users, label: 'Live rooms' },
              ].map((f) => (
                <span
                  key={f.label}
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground bg-white/50 backdrop-blur-sm border border-white/60 rounded-full px-3 py-1.5"
                >
                  <f.icon size={13} />
                  {f.label}
                </span>
              ))}
            </div>
          </motion.div>

          {/* Actions */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="space-y-3"
          >
            <Button
              onClick={() => navigate('/create')}
              className="w-full h-14 text-base font-semibold rounded-2xl gap-3 shadow-md"
            >
              <Plus size={20} strokeWidth={2.2} />
              Create a Room
              <ArrowRight size={16} className="ml-auto opacity-60" />
            </Button>

            <Button
              onClick={() => navigate('/join')}
              variant="outline"
              className="w-full h-14 text-base font-semibold rounded-2xl gap-3 bg-white/50 backdrop-blur-sm border-white/70 hover:bg-white/70"
            >
              <Users size={20} strokeWidth={2.2} />
              Join a Room
              <ArrowRight size={16} className="ml-auto opacity-60" />
            </Button>
          </motion.div>

          {/* Demo link */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-center"
          >
            <button
              onClick={() => navigate('/room/demo')}
              className="text-xs font-medium text-muted-foreground hover:text-foreground transition-colors underline underline-offset-4"
            >
              Try the demo without a room →
            </button>
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default Landing;
