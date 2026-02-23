import type { Room } from '@/types';

export const mockRooms: Room[] = [
  {
    code: '2A8FXY',
    sourceLanguage: 'Kikuyu',
    targetLanguage: 'English',
    createdAt: new Date(Date.now() - 3600000),
    participantCount: 2,
  },
  {
    code: '9K3DZW',
    sourceLanguage: 'English',
    targetLanguage: 'Kikuyu',
    createdAt: new Date(Date.now() - 7200000),
    participantCount: 1,
  },
  {
    code: '5M7P4Q',
    sourceLanguage: 'Kikuyu',
    targetLanguage: 'English',
    createdAt: new Date(Date.now() - 1800000),
    participantCount: 2,
  },
];

export function generateRoomCode(): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}
