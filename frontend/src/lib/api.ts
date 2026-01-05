/**
 * API client for AI SOC Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ChatRequest {
  message: string;
  session_id?: string;
  agent_type?: string;
}

interface ChatResponse {
  message: string;
  session_id: string;
  agent_type: string;
  sources: Array<{ title: string; source_path: string; score: number }>;
}

interface SearchRequest {
  query: string;
  limit?: number;
  category?: string;
}

interface SearchResult {
  content: string;
  document_title: string;
  score: number;
  metadata: Record<string, unknown>;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Chat endpoints
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.fetch<ChatResponse>('/api/v1/chat/', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getSession(sessionId: string): Promise<{ session_id: string; messages: unknown[] }> {
    return this.fetch(`/api/v1/chat/sessions/${sessionId}`);
  }

  async deleteSession(sessionId: string): Promise<{ status: string }> {
    return this.fetch(`/api/v1/chat/sessions/${sessionId}`, {
      method: 'DELETE',
    });
  }

  // Document endpoints
  async searchDocuments(request: SearchRequest): Promise<SearchResult[]> {
    return this.fetch<SearchResult[]>('/api/v1/documents/search', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async listDocuments(
    category?: string,
    limit = 50,
    offset = 0
  ): Promise<
    Array<{
      id: number;
      title: string;
      source_path: string;
      category: string | null;
      chunk_count: number;
    }>
  > {
    const params = new URLSearchParams();
    if (category) params.set('category', category);
    params.set('limit', limit.toString());
    params.set('offset', offset.toString());

    return this.fetch(`/api/v1/documents/?${params}`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.fetch('/api/v1/health');
  }
}

export const apiClient = new ApiClient();
export type { ChatRequest, ChatResponse, SearchRequest, SearchResult };
