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

interface LoginRequest {
  email: string;
  password: string;
}

interface SignupRequest {
  email: string;
  password: string;
  full_name: string;
}

interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    full_name: string;
    is_active: boolean;
  };
}

interface ConversationMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface SessionInfo {
  session_id: string;
  message_count: number;
  last_message: string | null;
}

class ApiClient {
  private baseUrl: string;
  private accessToken: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
    if (typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('access_token');
    }
  }

  setToken(token: string | null) {
    this.accessToken = token;
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('access_token', token);
      } else {
        localStorage.removeItem('access_token');
      }
    }
  }

  getToken(): string | null {
    return this.accessToken;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options?.headers as Record<string, string>),
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Auth endpoints
  async login(request: LoginRequest): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', request.email);
    formData.append('password', request.password);

    const response = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  async signup(request: SignupRequest): Promise<AuthResponse> {
    const data = await this.fetch<AuthResponse>('/api/v1/auth/signup', {
      method: 'POST',
      body: JSON.stringify(request),
    });
    this.setToken(data.access_token);
    return data;
  }

  async logout(): Promise<void> {
    try {
      await this.fetch('/api/v1/auth/logout', { method: 'POST' });
    } finally {
      this.setToken(null);
    }
  }

  async getCurrentUser(): Promise<AuthResponse['user'] | null> {
    if (!this.accessToken) return null;
    try {
      return await this.fetch('/api/v1/auth/me');
    } catch {
      return null;
    }
  }

  // Chat endpoints
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.fetch<ChatResponse>('/api/v1/chat/', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getSession(sessionId: string): Promise<{ session_id: string; messages: ConversationMessage[] }> {
    return this.fetch(`/api/v1/chat/sessions/${sessionId}`);
  }

  async deleteSession(sessionId: string): Promise<{ status: string }> {
    return this.fetch(`/api/v1/chat/sessions/${sessionId}`, {
      method: 'DELETE',
    });
  }

  async listSessions(): Promise<{ sessions: SessionInfo[]; total: number }> {
    return this.fetch('/api/v1/chat/sessions');
  }

  // Document endpoints
  async searchDocuments(request: SearchRequest): Promise<SearchResult[]> {
    return this.fetch<SearchResult[]>('/api/v1/documents/search', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    return this.fetch('/health');
  }
}

export const apiClient = new ApiClient();
export type {
  ChatRequest,
  ChatResponse,
  SearchRequest,
  SearchResult,
  LoginRequest,
  SignupRequest,
  AuthResponse,
  ConversationMessage,
  SessionInfo
};
