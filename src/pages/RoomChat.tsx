import { useState, useCallback, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChatLayout from '@/components/lugha/ChatLayout';
import { mockMessages, demoSequence, type ChatMessage, type SystemState } from '@/data/mockMessages';
import { api } from '@/services/api';

const RoomChat = () => {
  const { code } = useParams<{ code: string }>();
  const navigate = useNavigate();
  const isDemo = code === 'demo';

  const [messages, setMessages] = useState<ChatMessage[]>(isDemo ? mockMessages : []);
  const [systemState, setSystemState] = useState<SystemState>('idle');
  const [demoMode, setDemoMode] = useState(false);
  const [voiceMode, setVoiceMode] = useState(true);
  const [loadingRoom, setLoadingRoom] = useState(!isDemo);
  const [roomError, setRoomError] = useState<string | null>(null);
  const demoIndex = useRef(0);
  const demoTimeout = useRef<ReturnType<typeof setTimeout>>();

  // If no code, redirect to landing
  useEffect(() => {
    if (!code) navigate('/');
  }, [code, navigate]);

  useEffect(() => {
    if (!code || isDemo) return;
    let cancelled = false;
    const load = async () => {
      setLoadingRoom(true);
      setRoomError(null);
      try {
        const res = await api.joinRoom(code);
        const normalized = api.normalizeMessages((res as any).messages || []);
        if (!cancelled) {
          setMessages(normalized);
          setSystemState('idle');
        }
      } catch (err) {
        if (!cancelled) {
          setMessages(mockMessages);
          setRoomError('Live room unavailable. Showing demo messages.');
          setSystemState('error');
        }
      } finally {
        if (!cancelled) setLoadingRoom(false);
      }
    };
    load();
    return () => {
      cancelled = true;
    };
  }, [code, isDemo]);

  const simulateMessage = useCallback(() => {
    const seq = demoSequence[demoIndex.current % demoSequence.length];

    setSystemState('listening');

    demoTimeout.current = setTimeout(() => {
      setSystemState('transcribing');

      demoTimeout.current = setTimeout(() => {
        setSystemState('translating');

        demoTimeout.current = setTimeout(() => {
          const newMsg: ChatMessage = {
            id: `demo-${Date.now()}`,
            sender: seq.sender,
            originalText: seq.originalText,
            translatedText: seq.translatedText,
            originalLanguage: seq.originalLanguage,
            timestamp: new Date(),
            confidence: seq.confidence,
          };
          setMessages((prev) => [...prev, newMsg]);
          setSystemState('completed');
          demoIndex.current += 1;

          demoTimeout.current = setTimeout(() => {
            setSystemState('idle');
          }, 800);
        }, 900);
      }, 700);
    }, 1200);
  }, []);

  const handleMicPress = useCallback(() => {
    if (systemState !== 'idle' && systemState !== 'completed') return;
    simulateMessage();
  }, [systemState, simulateMessage]);

  const handleDemoToggle = useCallback((val: boolean) => {
    setDemoMode(val);
    if (!val) {
      if (demoTimeout.current) clearTimeout(demoTimeout.current);
      setSystemState('idle');
      return;
    }
    const runDemo = (i: number) => {
      if (i >= demoSequence.length) return;
      demoIndex.current = i;

      demoTimeout.current = setTimeout(() => {
        setSystemState('listening');

        demoTimeout.current = setTimeout(() => {
          setSystemState('transcribing');

          demoTimeout.current = setTimeout(() => {
            setSystemState('translating');

            demoTimeout.current = setTimeout(() => {
              const seq = demoSequence[i];
              const newMsg: ChatMessage = {
                id: `demo-auto-${Date.now()}`,
                sender: seq.sender,
                originalText: seq.originalText,
                translatedText: seq.translatedText,
                originalLanguage: seq.originalLanguage,
                timestamp: new Date(),
                confidence: seq.confidence,
              };
              setMessages((prev) => [...prev, newMsg]);
              setSystemState('completed');

              demoTimeout.current = setTimeout(() => {
                setSystemState('idle');
                runDemo(i + 1);
              }, 1000);
            }, 900);
          }, 700);
        }, 1200);
      }, 500);
    };
    runDemo(0);
  }, []);

  return (
    <ChatLayout
      messages={messages}
      systemState={loadingRoom ? 'transcribing' : roomError ? 'error' : systemState}
      demoMode={demoMode}
      onDemoToggle={handleDemoToggle}
      onMicPress={handleMicPress}
      voiceMode={voiceMode}
      onToggleVoice={setVoiceMode}
      roomCode={code || 'DEMO'}
      onBack={() => navigate('/')}
    />
  );
};

export default RoomChat;
