'use client';

import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiClient, type ChatResponse } from '@/lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agentType?: string;
  sources?: Array<{ title: string; score: number }>;
  timestamp: Date;
}

export function useChat(initialSessionId?: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>(initialSessionId);

  const sendMessageMutation = useMutation({
    mutationFn: async (message: string) => {
      return apiClient.sendMessage({
        message,
        session_id: sessionId,
      });
    },
    onSuccess: (response: ChatResponse) => {
      // Update session ID if this is the first message
      if (!sessionId) {
        setSessionId(response.session_id);
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        agentType: response.agent_type,
        sources: response.sources.map((s) => ({ title: s.title, score: s.score })),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    },
  });

  const sendMessage = useCallback(
    (content: string) => {
      // Add user message immediately
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        role: 'user',
        content,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);

      // Send to API
      sendMessageMutation.mutate(content);
    },
    [sendMessageMutation]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(undefined);
  }, []);

  return {
    messages,
    sessionId,
    isLoading: sendMessageMutation.isPending,
    error: sendMessageMutation.error,
    sendMessage,
    clearChat,
  };
}
