import type { Room } from '@/types';

export const mockRooms: Room[] = [
  {
    code: 'LUGHA-2A8F',
    sourceLanguage: 'Kikuyu',
    targetLanguage: 'English',
    createdAt: new Date(Date.now() - 3600000),
    participantCount: 2,
  },
  {
    code: 'LUGHA-9K3D',
    sourceLanguage: 'English',
    targetLanguage: 'Kikuyu',
    createdAt: new Date(Date.now() - 7200000),
    participantCount: 1,
  },
  {
    code: 'LUGHA-5M7P',
    sourceLanguage: 'Kikuyu',
    targetLanguage: 'English',
    createdAt: new Date(Date.now() - 1800000),
    participantCount: 2,
  },
];

export function generateRoomCode(): string {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = 'LUGHA-';
  for (let i = 0; i < 4; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}
