'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { MessageBubble } from './MessageBubble';
import { AgentBadge } from './AgentBadge';
import { CitationsPanel } from './CitationsPanel';
import { ApprovalDialog } from './ApprovalDialog';
import { useAuth } from '@/lib/auth';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  citations?: Citation[];
  approval?: ApprovalRequest;
  timestamp: Date;
}

interface Citation {
  id: string;
  content: string;
  source: string;
  page?: string;
}

interface ApprovalRequest {
  id: string;
  action: string;
  description: string;
  risk_level: string;
  status: 'pending' | 'approved' | 'rejected';
}

interface ChatWidgetProps {
  selectedText?: string;
  currentPage?: string;
  className?: string;
}

export function ChatWidget({ selectedText, currentPage, className }: ChatWidgetProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showCitations, setShowCitations] = useState(false);
  const [activeCitations, setActiveCitations] = useState<Citation[]>([]);
  const [pendingApproval, setPendingApproval] = useState<ApprovalRequest | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const { token } = useAuth();

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  useEffect(() => {
    if (selectedText && inputRef.current) {
      setInput(`Explain this: "${selectedText}"`);
      inputRef.current.focus();
    }
  }, [selectedText]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: userMessage.content,
          context: {
            selected_text: selectedText,
            current_page: currentPage,
          },
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: data.id,
        role: 'assistant',
        content: data.content,
        agent: data.agent,
        citations: data.citations,
        approval: data.approval,
        timestamp: new Date(data.timestamp),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (data.approval?.status === 'pending') {
        setPendingApproval(data.approval);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
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

  const handleShowCitations = (citations: Citation[]) => {
    setActiveCitations(citations);
    setShowCitations(true);
  };

  const handleApprovalAction = async (approved: boolean) => {
    if (!pendingApproval) return;

    try {
      const endpoint = approved
        ? `/api/approvals/${pendingApproval.id}/approve`
        : `/api/approvals/${pendingApproval.id}/reject`;

      await fetch(endpoint, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPendingApproval(null);

      const statusMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: approved
          ? `Action approved: ${pendingApproval.action}`
          : `Action rejected: ${pendingApproval.action}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, statusMessage]);
    } catch (error) {
      console.error('Approval error:', error);
    }
  };

  const clearChat = async () => {
    try {
      await fetch('/api/chat/history/clear', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessages([]);
    } catch (error) {
      console.error('Clear chat error:', error);
    }
  };

  return (
    <div className={`flex flex-col h-full bg-gray-900 rounded-lg ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white">AI Security Assistant</h2>
        <button
          onClick={clearChat}
          className="text-sm text-gray-400 hover:text-white transition-colors"
        >
          Clear Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">Welcome to AI-SOC Assistant</p>
            <p className="text-sm">
              Ask questions about security alerts, get help with triage, or request incident
              reports.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className="animate-fadeIn">
            {message.agent && <AgentBadge agent={message.agent} />}
            <MessageBubble
              message={message}
              onShowCitations={message.citations ? () => handleShowCitations(message.citations!) : undefined}
            />
          </div>
        ))}

        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-400">
            <div className="animate-pulse flex space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-100" />
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-200" />
            </div>
            <span className="text-sm">Analyzing...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex items-end space-x-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about security alerts, request analysis, or get help..."
            className="flex-1 bg-gray-800 text-white rounded-lg p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
      </div>

      {/* Citations Panel */}
      {showCitations && (
        <CitationsPanel citations={activeCitations} onClose={() => setShowCitations(false)} />
      )}

      {/* Approval Dialog */}
      {pendingApproval && (
        <ApprovalDialog
          approval={pendingApproval}
          onApprove={() => handleApprovalAction(true)}
          onReject={() => handleApprovalAction(false)}
          onClose={() => setPendingApproval(null)}
        />
      )}
    </div>
  );
}
