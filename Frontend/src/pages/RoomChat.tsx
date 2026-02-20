import { useState, useCallback, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChatLayout from '@/components/lugha/ChatLayout';
import { mockMessages, demoSequence, type ChatMessage, type SystemState } from '@/data/mockMessages';
import { api } from '@/services/api';
import { RoomWebSocket, normalizeMessage } from '@/services/websocket';
import { useVoiceRecording } from '@/hooks/useVoiceRecording';

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
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
  const [roomLanguages, setRoomLanguages] = useState<{ source: string; target: string } | null>(null);
  
  const wsRef = useRef<RoomWebSocket | null>(null);
  const demoIndex = useRef(0);
  const demoTimeout = useRef<ReturnType<typeof setTimeout>>();
  const processingMessageIds = useRef<Set<string>>(new Set());

  // Voice recording hook
  const { isRecording, startRecording, stopRecording } = useVoiceRecording({
    onRecordingComplete: (audioData) => {
      if (wsRef.current && roomLanguages) {
        // Send voice message via WebSocket
        const messageId = wsRef.current.sendVoiceMessage(audioData, roomLanguages.source);
        processingMessageIds.current.add(messageId);
        setSystemState('transcribing');
      }
    },
    onError: (error) => {
      console.error('Recording error:', error);
      setRoomError(error.message);
      setSystemState('error');
    },
  });

  // If no code, redirect to landing
  useEffect(() => {
    if (!code) navigate('/');
  }, [code, navigate]);

  // WebSocket connection management
  useEffect(() => {
    if (!code || isDemo || demoMode) return;

    let cancelled = false;
    const connectToRoom = async () => {
      setLoadingRoom(true);
      setRoomError(null);
      setConnectionStatus('connecting');

      try {
        // First, verify room exists via REST API
        const roomData = await api.joinRoom(code);
        
        if (cancelled) return;

        // Store room languages
        setRoomLanguages({
          source: roomData.source_language || roomData.source_lang || 'kikuyu',
          target: roomData.target_language || roomData.target_lang || 'english',
        });

        // Create WebSocket connection
        const ws = new RoomWebSocket(code);
        wsRef.current = ws;

        // Set up event listeners
        ws.on('open', () => {
          if (!cancelled) {
            console.log('WebSocket connected');
            setConnectionStatus('connected');
            setLoadingRoom(false);
          }
        });

        ws.on('connection_established', (data) => {
          if (!cancelled) {
            console.log('Connection established:', data);
            setRoomLanguages({
              source: data.source_lang || 'kikuyu',
              target: data.target_lang || 'english',
            });
          }
        });

        ws.on('message_history', (data) => {
          if (!cancelled && data.messages) {
            const normalized = data.messages.map(normalizeMessage);
            setMessages(normalized);
          }
        });

        ws.on('translation_complete', (data) => {
          if (!cancelled) {
            console.log('Translation complete:', data);
            const message = normalizeMessage(data);
            setMessages((prev) => [...prev, message]);
            
            // Remove from processing set
            if (data.id || data.message_id) {
              processingMessageIds.current.delete(data.id || data.message_id);
            }
            
            // Update state
            setSystemState('completed');
            setTimeout(() => setSystemState('idle'), 800);
          }
        });

        ws.on('chat_message', (data) => {
          if (!cancelled) {
            console.log('Chat message:', data);
            const message = normalizeMessage(data.message || data);
            setMessages((prev) => [...prev, message]);
          }
        });

        ws.on('processing', (data) => {
          if (!cancelled) {
            console.log('Processing:', data);
            setSystemState('transcribing');
          }
        });

        ws.on('translation_progress', (data) => {
          if (!cancelled) {
            console.log('Translation progress:', data);
            const status = data.status;
            if (status === 'transcribing') {
              setSystemState('transcribing');
            } else if (status === 'translating') {
              setSystemState('translating');
            } else if (status === 'synthesizing') {
              setSystemState('translating'); // We don't have a specific synthesizing state
            }
          }
        });

        ws.on('error', (data) => {
          if (!cancelled) {
            console.error('WebSocket error:', data);
            setRoomError(data.message || 'WebSocket error');
            setSystemState('error');
          }
        });

        ws.on('close', () => {
          if (!cancelled) {
            console.log('WebSocket closed');
            setConnectionStatus('disconnected');
          }
        });

        // Connect
        await ws.connect();

      } catch (error) {
        if (!cancelled) {
          console.error('Failed to connect to room:', error);
          setRoomError('Failed to connect to room. Please try again.');
          setConnectionStatus('error');
          setLoadingRoom(false);
          setSystemState('error');
        }
      }
    };

    connectToRoom();

    return () => {
      cancelled = true;
      if (wsRef.current) {
        wsRef.current.disconnect();
        wsRef.current = null;
      }
    };
  }, [code, isDemo, demoMode, navigate]);

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
    
    // Use demo simulation if in demo mode or on demo room
    if (demoMode || isDemo) {
      simulateMessage();
      return;
    }
    
    // Real voice recording
    if (isRecording) {
      stopRecording();
      setSystemState('transcribing');
    } else {
      setSystemState('listening');
      startRecording();
    }
  }, [systemState, demoMode, isDemo, isRecording, startRecording, stopRecording, simulateMessage]);

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

  const handleSendText = useCallback((text: string, language: string) => {
    if (wsRef.current && !demoMode && !isDemo) {
      // Send real text message via WebSocket
      wsRef.current.sendTextMessage(text, language);
      setSystemState('translating');
    } else {
      // Demo mode: simulate a message
      simulateMessage();
    }
  }, [demoMode, isDemo, simulateMessage]);

  return (
    <ChatLayout
      messages={messages}
      systemState={loadingRoom ? 'transcribing' : roomError ? 'error' : systemState}
      demoMode={demoMode}
      onDemoToggle={handleDemoToggle}
      onMicPress={handleMicPress}
      voiceMode={voiceMode}
      onToggleVoice={setVoiceMode}
      onSendText={handleSendText}
      sourceLanguage={roomLanguages?.source || 'kikuyu'}
      targetLanguage={roomLanguages?.target || 'english'}
      connectionStatus={isDemo || demoMode ? 'disconnected' : connectionStatus}
      roomCode={code || 'DEMO'}
      onBack={() => navigate('/')}
    />
  );
};

export default RoomChat;
