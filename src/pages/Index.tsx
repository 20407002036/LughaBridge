import { useState, useCallback, useRef } from 'react';
import ChatLayoutPro from '@/components/lugha/ChatLayoutPro';
import { mockMessages, demoSequence, type ChatMessage, type SystemState } from '@/data/mockMessages';

const Index = () => {
  const [messages, setMessages] = useState<ChatMessage[]>(mockMessages);
  const [systemState, setSystemState] = useState<SystemState>('idle');
  const [demoMode, setDemoMode] = useState(false);
  const demoIndex = useRef(0);
  const demoTimeout = useRef<ReturnType<typeof setTimeout>>();

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
    // Start demo auto-play
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
    <ChatLayoutPro
      messages={messages}
      systemState={systemState}
      demoMode={demoMode}
      onDemoToggle={handleDemoToggle}
      onMicPress={handleMicPress}
    />
  );
};

export default Index;
