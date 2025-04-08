import api from './api';

export interface ChatMessage {
  content: string;
  metadata?: Record<string, any>;
}

export interface ChatResponse {
  message: string;
}

export interface AgentConfig {
  is_active: boolean;
  store_level: 'store' | 'product' | 'user_id';
  faq_threshold: number;
  custom_prompt?: string;
}

export interface AgentResponse {
  success: boolean;
  message: string;
}

export interface FAQQuery {
  question: string;
  context?: Record<string, any>;
}

export const sendChatMessage = async (message: ChatMessage): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/api/chat/send', message);
  return response.data;
};

export const getAgentConfig = async (): Promise<AgentConfig> => {
  const response = await api.get<AgentConfig>('/api/ai/config');
  return response.data;
};

export const configureAgent = async (config: AgentConfig): Promise<AgentResponse> => {
  const response = await api.post<AgentResponse>('/api/ai/configure', config);
  return response.data;
};

export const queryFAQ = async (query: FAQQuery): Promise<any> => {
  const response = await api.post('/api/ai/faq', query);
  return response.data;
};

export const getUserMemory = async (userId: number): Promise<any> => {
  const response = await api.get(`/api/ai/memory/${userId}`);
  return response.data;
};
