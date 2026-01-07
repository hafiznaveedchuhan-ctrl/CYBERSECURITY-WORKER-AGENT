'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Loader2 } from 'lucide-react';
import { useAuth } from '@/lib/auth';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  timestamp: Date;
}

interface ChatWidgetProps {
  className?: string;
}

export function ChatWidget({ className = '' }: ChatWidgetProps) {
  const { token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${apiUrl}/api/v1/chat/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          message: userMessage.content,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.message || data.response || 'No response',
        agent: data.agent_type || data.agent,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`flex flex-col bg-slate-900 ${className}`}>
      {/* Chat Header */}
      <div className="flex items-center gap-3 p-4 border-b border-cyan-500/20 bg-slate-900/95">
        <div className="relative">
          <div className="absolute inset-0 bg-cyan-500 blur-lg opacity-30" />
          <div className="relative h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
            <Bot className="h-6 w-6 text-white" />
          </div>
        </div>
        <div>
          <h3 className="font-semibold text-white">AI Employ Assistant</h3>
          <p className="text-xs text-cyan-400">Security Operations Support</p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-xs text-slate-400">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 flex items-center justify-center mb-4 border border-cyan-500/30">
              <Sparkles className="h-8 w-8 text-cyan-400" />
            </div>
            <h4 className="text-lg font-semibold text-white mb-2">AI Employ Ready</h4>
            <p className="text-sm text-slate-400 max-w-xs">
              Ask me about threat analysis, IOC enrichment, MITRE mapping, or security incidents.
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className={`flex-shrink-0 h-8 w-8 rounded-lg flex items-center justify-center ${
                message.role === 'user'
                  ? 'bg-purple-500/20 border border-purple-500/30'
                  : 'bg-cyan-500/20 border border-cyan-500/30'
              }`}
            >
              {message.role === 'user' ? (
                <User className="h-4 w-4 text-purple-400" />
              ) : (
                <Bot className="h-4 w-4 text-cyan-400" />
              )}
            </div>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-purple-500/20 border border-purple-500/30 text-white'
                  : 'bg-slate-800 border border-slate-700 text-slate-200'
              }`}
            >
              {message.agent && (
                <span className="text-xs text-cyan-400 font-medium block mb-1">
                  [{message.agent}]
                </span>
              )}
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <span className="text-xs text-slate-500 mt-2 block">
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3">
            <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center">
              <Bot className="h-4 w-4 text-cyan-400" />
            </div>
            <div className="bg-slate-800 border border-slate-700 rounded-2xl px-4 py-3">
              <div className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 text-cyan-400 animate-spin" />
                <span className="text-sm text-slate-400">Analyzing...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-cyan-500/20 bg-slate-900/95">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your security concern..."
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
