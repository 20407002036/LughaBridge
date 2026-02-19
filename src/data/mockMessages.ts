export type MessageSender = 'A' | 'B';
export type MessageLanguage = 'Kikuyu' | 'English';
export type SystemState = 'idle' | 'listening' | 'transcribing' | 'translating' | 'completed' | 'error';

export interface ChatMessage {
  id: string;
  sender: MessageSender;
  originalText: string;
  translatedText: string;
  originalLanguage: MessageLanguage;
  timestamp: Date;
  confidence: number;
}

export const mockMessages: ChatMessage[] = [
  {
    id: '1',
    sender: 'A',
    originalText: 'Wĩ mwega? Nĩ ngũkena gũkuona.',
    translatedText: 'How are you? I am happy to see you.',
    originalLanguage: 'Kikuyu',
    timestamp: new Date(Date.now() - 300000),
    confidence: 0.94,
  },
  {
    id: '2',
    sender: 'B',
    originalText: 'I am doing well, thank you! How is your family?',
    translatedText: 'Ndĩ mwega, nĩ wega! Nyũmba yaku ĩrĩ atĩa?',
    originalLanguage: 'English',
    timestamp: new Date(Date.now() - 240000),
    confidence: 0.91,
  },
  {
    id: '3',
    sender: 'A',
    originalText: 'Andũ akwa othe nĩ ega. Tũrathiĩ mũgũnda.',
    translatedText: 'My people are all well. We are going to the farm.',
    originalLanguage: 'Kikuyu',
    timestamp: new Date(Date.now() - 180000),
    confidence: 0.88,
  },
  {
    id: '4',
    sender: 'B',
    originalText: 'That sounds wonderful. The harvest season is coming soon.',
    translatedText: 'Ũguo nĩ gwega mũno. Ihinda rĩa magetha rĩrĩkuhĩrĩria.',
    originalLanguage: 'English',
    timestamp: new Date(Date.now() - 120000),
    confidence: 0.87,
  },
  {
    id: '5',
    sender: 'A',
    originalText: 'Ĩĩ, tũrarehera na gĩkeno. Ngai atũrathime.',
    translatedText: 'Yes, we are preparing with joy. May God bless us.',
    originalLanguage: 'Kikuyu',
    timestamp: new Date(Date.now() - 60000),
    confidence: 0.92,
  },
];

export const demoSequence: { sender: MessageSender; originalText: string; translatedText: string; originalLanguage: MessageLanguage; confidence: number }[] = [
  {
    sender: 'A',
    originalText: 'Ũhoro waku? Nĩ ndĩramũkĩra.',
    translatedText: 'How is your news? I am greeting you.',
    originalLanguage: 'Kikuyu',
    confidence: 0.93,
  },
  {
    sender: 'B',
    originalText: 'Hello! I am learning Kikuyu. Can you help me?',
    translatedText: 'Ũhoro! Ndĩrĩkĩĩra Gĩkũyũ. Ũngĩteithia?',
    originalLanguage: 'English',
    confidence: 0.90,
  },
  {
    sender: 'A',
    originalText: 'Ĩĩ, ngũgũteithia na gĩkeno kĩnene!',
    translatedText: 'Yes, I will help you with great joy!',
    originalLanguage: 'Kikuyu',
    confidence: 0.95,
  },
  {
    sender: 'B',
    originalText: 'Thank you so much. Language connects us all.',
    translatedText: 'Nĩ wega mũno. Rũthiomi rũtũũnganĩtie othe.',
    originalLanguage: 'English',
    confidence: 0.89,
  },
];
