
import axios from 'axios';
// Lexi API integration
export const askLexi = async (query, mode = "github") => {
  // Replace with your deployed Lexi FastAPI endpoint
  const LEXI_API_URL = "https://your-lexi-api.onrender.com/api/v1/ask";
  const response = await fetch(LEXI_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, mode }),
  });
  if (!response.ok) throw new Error("Lexi API error");
  return await response.json(); // { answer, metadata, process_logs }
};

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  // Chat operations
  sendMessage: async (conversationId, message, githubModeEnabled = false, genZModeEnabled = false) => {
    const response = await apiClient.post('/chat', {
      conversation_id: conversationId,
      message: message,
      github_mode: githubModeEnabled,
      gen_z_mode: genZModeEnabled,
    });
    return response.data;
  },

  // Conversation operations
  createConversation: async (title = 'New Chat') => {
    const response = await apiClient.post('/conversations', {
      title: title,
    });
    return response.data;
  },

  getConversations: async () => {
    const response = await apiClient.get('/conversations');
    return response.data;
  },

  getConversationHistory: async (conversationId) => {
    const response = await apiClient.get(`/conversations/${conversationId}`);
    return response.data;
  },

  shareConversation: async (conversationId) => {
    const response = await apiClient.post(`/conversations/${conversationId}/share`);
    return response.data;
  },

  getSharedConversation: async (shareId) => {
    const response = await apiClient.get(`/shared/${shareId}`);
    return response.data;
  },

  deleteConversation: async (conversationId) => {
    const response = await apiClient.delete(`/conversations/${conversationId}`);
    return response.data;
  },

  updateConversation: async (conversationId, title) => {
    const response = await apiClient.patch(`/conversations/${conversationId}`, {
      title: title,
    });
    return response.data;
  },

  // Portfolio operations
  getPortfolioInfo: async () => {
    const response = await apiClient.get('/portfolio-info');
    return response.data;
  },

  healthCheck: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // GitHub operations
  getGitHubRepositories: async () => {
    const response = await apiClient.get('/github/repositories');
    return response.data;
  },

  getGitHubRepositoriesByLanguage: async (language) => {
    const response = await apiClient.get(`/github/repositories/language/${language}`);
    return response.data;
  },

  getGitHubRepositoryDetails: async (repoName) => {
    const response = await apiClient.get(`/github/repositories/${repoName}`);
    return response.data;
  },
};

export default apiClient;
