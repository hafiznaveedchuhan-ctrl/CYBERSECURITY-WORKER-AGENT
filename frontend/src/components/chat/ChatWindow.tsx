'use client';

import { useRef, useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agentType?: string;
  sources?: Array<{ title: string; score: number }>;
  timestamp: Date;
}

interface ChatWindowProps {
  messages: Message[];
  onSend: (message: string) => void;
  isLoading?: boolean;
  title?: string;
}

export function ChatWindow({
  messages,
  onSend,
  isLoading = false,
  title = 'AI SOC Assistant',
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Card className="flex h-[600px] flex-col">
      <CardHeader className="border-b">
        <CardTitle className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-green-500" />
          {title}
        </CardTitle>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              <div className="text-center">
                <p className="mb-2 text-lg">Welcome to AI SOC Assistant</p>
                <p className="text-sm">
                  Ask questions about security operations, incident response, threat intelligence,
                  and more.
                </p>
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                agentType={msg.agentType}
                sources={msg.sources}
                timestamp={msg.timestamp}
              />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </CardContent>

      <div className="border-t p-4">
        <ChatInput onSend={onSend} isLoading={isLoading} />
      </div>
    </Card>
  );
}
