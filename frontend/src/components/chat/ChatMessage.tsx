'use client';

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  agentType?: string;
  sources?: Array<{ title: string; score: number }>;
  timestamp?: Date;
}

const agentColors: Record<string, string> = {
  supervisor: 'bg-purple-600',
  triage: 'bg-red-600',
  enrichment: 'bg-blue-600',
  threatintel: 'bg-orange-500',
  detection: 'bg-green-600',
  incident: 'bg-pink-600',
  report: 'bg-cyan-600',
};

export function ChatMessage({ role, content, agentType, sources, timestamp }: ChatMessageProps) {
  const isUser = role === 'user';

  return (
    <div className={cn('flex w-full', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={cn(
          'max-w-[80%] rounded-lg px-4 py-3',
          isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'
        )}
      >
        {!isUser && agentType && (
          <div className="mb-2 flex items-center gap-2">
            <span
              className={cn(
                'inline-block h-2 w-2 rounded-full',
                agentColors[agentType] || 'bg-gray-500'
              )}
            />
            <span className="text-xs font-medium uppercase text-muted-foreground">{agentType}</span>
          </div>
        )}

        <div className="prose prose-sm dark:prose-invert max-w-none">
          <p className="whitespace-pre-wrap">{content}</p>
        </div>

        {sources && sources.length > 0 && (
          <div className="mt-3 border-t border-border pt-2">
            <p className="mb-1 text-xs text-muted-foreground">Sources:</p>
            <div className="flex flex-wrap gap-1">
              {sources.map((source, idx) => (
                <Badge key={idx} variant="outline" className="text-xs">
                  {source.title} ({(source.score * 100).toFixed(0)}%)
                </Badge>
              ))}
            </div>
          </div>
        )}

        {timestamp && (
          <p className="mt-2 text-right text-xs text-muted-foreground">
            {timestamp.toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}
