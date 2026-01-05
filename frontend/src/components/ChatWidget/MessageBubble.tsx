'use client';

import { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Citation {
  id: string;
  content: string;
  source: string;
  page?: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  citations?: Citation[];
  timestamp: Date;
}

interface MessageBubbleProps {
  message: Message;
  onShowCitations?: () => void;
}

export function MessageBubble({ message, onShowCitations }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  const formattedTime = useMemo(() => {
    return new Intl.DateTimeFormat('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    }).format(message.timestamp);
  }, [message.timestamp]);

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-800 text-gray-100 border border-gray-700'
        }`}
      >
        {/* Message Content */}
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown
            components={{
              code({ node, className, children, ...props }) {
                const inline = !className;
                const match = /language-(\w+)/.exec(className || '');
                const language = match ? match[1] : '';

                if (!inline && language) {
                  return (
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language={language}
                      PreTag="div"
                      className="rounded-md"
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  );
                }

                return (
                  <code
                    className={`${
                      inline
                        ? 'bg-gray-700 px-1 py-0.5 rounded text-sm'
                        : 'block bg-gray-700 p-2 rounded'
                    }`}
                    {...props}
                  >
                    {children}
                  </code>
                );
              },
              table({ children }) {
                return (
                  <div className="overflow-x-auto my-4">
                    <table className="min-w-full divide-y divide-gray-600">
                      {children}
                    </table>
                  </div>
                );
              },
              th({ children }) {
                return (
                  <th className="px-3 py-2 text-left text-xs font-medium text-gray-300 uppercase tracking-wider bg-gray-700">
                    {children}
                  </th>
                );
              },
              td({ children }) {
                return (
                  <td className="px-3 py-2 text-sm text-gray-300 border-t border-gray-700">
                    {children}
                  </td>
                );
              },
              ul({ children }) {
                return <ul className="list-disc list-inside space-y-1">{children}</ul>;
              },
              ol({ children }) {
                return <ol className="list-decimal list-inside space-y-1">{children}</ol>;
              },
              a({ href, children }) {
                return (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 underline"
                  >
                    {children}
                  </a>
                );
              },
              blockquote({ children }) {
                return (
                  <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-400">
                    {children}
                  </blockquote>
                );
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between mt-3 pt-2 border-t border-gray-700/50">
          <span className="text-xs text-gray-400">{formattedTime}</span>

          {message.citations && message.citations.length > 0 && (
            <button
              onClick={onShowCitations}
              className="text-xs text-blue-400 hover:text-blue-300 flex items-center space-x-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-3 w-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
              <span>{message.citations.length} sources</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
