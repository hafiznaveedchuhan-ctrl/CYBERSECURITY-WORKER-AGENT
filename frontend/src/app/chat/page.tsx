'use client';

import { ChatWindow } from '@/components/chat/ChatWindow';
import { useChat } from '@/hooks/useChat';
import { Button } from '@/components/ui/button';

export default function ChatPage() {
  const { messages, isLoading, sendMessage, clearChat } = useChat();

  return (
    <main className="container mx-auto max-w-4xl p-4">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">AI SOC Chat</h1>
        <div className="flex gap-2">
          <Button variant="outline" onClick={clearChat}>
            New Chat
          </Button>
          <Button variant="outline" asChild>
            <a href="/">Home</a>
          </Button>
        </div>
      </div>

      <ChatWindow messages={messages} onSend={sendMessage} isLoading={isLoading} />

      <div className="mt-4 text-center text-sm text-muted-foreground">
        <p>
          Powered by AI SOC Platform. Ask questions about security operations, incident response,
          threat intelligence, and more.
        </p>
      </div>
    </main>
  );
}
