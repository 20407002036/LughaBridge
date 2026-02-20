import { useState, useRef, useCallback } from 'react';
import { blobToBase64 } from '@/services/websocket';

interface UseVoiceRecordingOptions {
  onRecordingComplete?: (audioData: string) => void;
  onError?: (error: Error) => void;
  sampleRate?: number;
}

interface UseVoiceRecordingReturn {
  isRecording: boolean;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  error: string | null;
}

export function useVoiceRecording(options: UseVoiceRecordingOptions = {}): UseVoiceRecordingReturn {
  const {
    onRecordingComplete,
    onError,
    sampleRate = 16000,
  } = options;

  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  const startRecording = useCallback(async () => {
    try {
      setError(null);

      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: sampleRate,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      streamRef.current = stream;
      audioChunksRef.current = [];

      // Create MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });

      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        try {
          // Combine audio chunks into a blob
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          
          // Convert to base64
          const base64Audio = await blobToBase64(audioBlob);
          
          // Call the callback
          if (onRecordingComplete) {
            onRecordingComplete(base64Audio);
          }

          // Clean up stream
          if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => track.stop());
            streamRef.current = null;
          }
        } catch (err) {
          const error = err instanceof Error ? err : new Error('Failed to process audio');
          console.error('Error processing recording:', error);
          setError(error.message);
          if (onError) {
            onError(error);
          }
        }
      };

      mediaRecorder.onerror = (event) => {
        const error = new Error('MediaRecorder error');
        console.error('MediaRecorder error:', event);
        setError(error.message);
        if (onError) {
          onError(error);
        }
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
      console.log('Recording started');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to start recording');
      console.error('Error starting recording:', error);
      
      if (error.name === 'NotAllowedError') {
        setError('Microphone access denied. Please allow microphone access and try again.');
      } else if (error.name === 'NotFoundError') {
        setError('No microphone found. Please connect a microphone and try again.');
      } else {
        setError('Failed to access microphone: ' + error.message);
      }
      
      if (onError) {
        onError(error);
      }
    }
  }, [sampleRate, onRecordingComplete, onError]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      console.log('Recording stopped');
    }
  }, [isRecording]);

  return {
    isRecording,
    startRecording,
    stopRecording,
    error,
  };
}
