const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000'  // Development
  : 'https://your-production-api.com';  // Update this with your production URL

export interface ChatMessage {
  message: string;
}

export interface ChatResponse {
  response: string;
  message_id: string;
  user_id?: string;
}

class ApiService {
  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async sendChatMessage(message: string): Promise<ChatResponse> {
    const chatMessage: ChatMessage = { message };
    
    return this.makeRequest<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify(chatMessage),
    });
  }

  async checkHealth(): Promise<any> {
    return this.makeRequest('/health');
  }
}

export const apiService = new ApiService();