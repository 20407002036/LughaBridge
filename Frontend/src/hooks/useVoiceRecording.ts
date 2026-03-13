import { useState, useRef, useCallback, useEffect } from 'react';
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
  const isStartingRef = useRef(false);

  const cleanupStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
  }, []);

  const resetRecorderState = useCallback(() => {
    mediaRecorderRef.current = null;
    audioChunksRef.current = [];
    setIsRecording(false);
    isStartingRef.current = false;
  }, []);

  const startRecording = useCallback(async () => {
    if (isStartingRef.current) {
      return;
    }

    const existingRecorder = mediaRecorderRef.current;
    if (existingRecorder && existingRecorder.state === 'recording') {
      setIsRecording(true);
      return;
    }

    try {
      isStartingRef.current = true;
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

      stream.getAudioTracks().forEach((track) => {
        track.onended = () => {
          resetRecorderState();
          cleanupStream();
        };
      });

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
        setIsRecording(false);

        try {
          // Combine audio chunks into a blob
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          
          // Convert to base64
          const base64Audio = await blobToBase64(audioBlob);
          
          // Call the callback
          if (onRecordingComplete) {
            onRecordingComplete(base64Audio);
          }
        } catch (err) {
          const error = err instanceof Error ? err : new Error('Failed to process audio');
          console.error('Error processing recording:', error);
          setError(error.message);
          if (onError) {
            onError(error);
          }
        } finally {
          cleanupStream();
          resetRecorderState();
        }
      };

      mediaRecorder.onerror = (event) => {
        const error = new Error('MediaRecorder error');
        console.error('MediaRecorder error:', event);
        setError(error.message);
        cleanupStream();
        resetRecorderState();
        if (onError) {
          onError(error);
        }
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
      isStartingRef.current = false;
      console.log('Recording started');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to start recording');
      console.error('Error starting recording:', error);
      cleanupStream();
      resetRecorderState();
      
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
    } finally {
      isStartingRef.current = false;
    }
  }, [sampleRate, onRecordingComplete, onError, cleanupStream, resetRecorderState]);

  const stopRecording = useCallback(() => {
    const mediaRecorder = mediaRecorderRef.current;

    if (!mediaRecorder) {
      setIsRecording(false);
      cleanupStream();
      return;
    }

    if (mediaRecorder.state === 'inactive') {
      setIsRecording(false);
      cleanupStream();
      resetRecorderState();
      return;
    }

    try {
      mediaRecorder.stop();
      setIsRecording(false);
      console.log('Recording stopped');
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to stop recording');
      console.error('Error stopping recording:', error);
      setError(error.message);
      cleanupStream();
      resetRecorderState();
      if (onError) {
        onError(error);
      }
    }
  }, [cleanupStream, resetRecorderState, onError]);

  useEffect(() => {
    return () => {
      const mediaRecorder = mediaRecorderRef.current;
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        try {
          mediaRecorder.stop();
        } catch {
          // no-op
        }
      }
      cleanupStream();
      resetRecorderState();
    };
  }, [cleanupStream, resetRecorderState]);

  return {
    isRecording,
    startRecording,
    stopRecording,
    error,
  };
}
