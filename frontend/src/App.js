import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import SharedView from './components/SharedView';
import Profile from './components/Profile';
import AdminPanel from './components/AdminPanel';
import LexiTerminal from './components/LexiTerminal';
import { chatAPI, askLexi } from './api';
import './index.css';

function AppContent() {
  const navigate = useNavigate();
  const { sharedId } = useParams();
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [portfolioInfo, setPortfolioInfo] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [githubModeEnabled, setGithubModeEnabled] = useState(false);
  const [genZModeEnabled, setGenZModeEnabled] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [projects, setProjects] = useState([]);
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [lexiModeEnabled, setLexiModeEnabled] = useState(false);
  const [showLexiTerminal, setShowLexiTerminal] = useState(false);

  // Load portfolio info and GitHub projects on mount
  useEffect(() => {
    const loadPortfolioInfo = async () => {
      try {
        const info = await chatAPI.getPortfolioInfo();
        setPortfolioInfo(info);
      } catch (error) {
        console.error('Error loading portfolio info:', error);
      }
    };

    const fetchGitHubProjects = async () => {
      try {
        // Use backend API instead of direct GitHub API call
        // This allows the backend to handle auth and rate limiting
        const repos = await chatAPI.getGitHubRepositories();
        
        // Filter out forks and map to project format
        const projectsData = repos
          .filter(repo => !repo.fork_count || repo.fork_count === 0) // Only include original projects
          .map(repo => ({
            title: repo.name,
            description: repo.description || 'No description available',
            link: repo.url,
            language: repo.language,
            stars: repo.stars,
          }));
        
        setProjects(projectsData);
      } catch (error) {
        console.error('Error fetching GitHub projects:', error);
        // Silently fail - projects just won't show
      }
    };

    loadPortfolioInfo();
    fetchGitHubProjects();
    loadConversations();
  }, []);

  // Load conversation history when current conversation changes
  useEffect(() => {
    if (currentConversation) {
      loadMessages();
    } else {
      setMessages([]);
    }
  }, [currentConversation]);

  const loadConversations = async () => {
    try {
      const convs = await chatAPI.getConversations();
      setConversations(convs);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadMessages = async () => {
    if (!currentConversation) return;
    
    try {
      const msgs = await chatAPI.getConversationHistory(currentConversation.id);
      setMessages(msgs);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      const newConv = await chatAPI.createConversation('New Chat');
      setCurrentConversation(newConv);
      await loadConversations();
    } catch (error) {
      console.error('Error creating new conversation:', error);
    }
  };

  const handleSelectConversation = (conversation) => {
    setCurrentConversation(conversation);
  };

  const handleSendMessage = async (message) => {
    let convId = currentConversation?.id;
    let isNewConversation = false;
    let isFirstMessage = messages.length === 0; // Check if this is the first message
    
    // If no conversation exists, create one first
    if (!convId) {
      try {
        const newConv = await chatAPI.createConversation();
        convId = newConv.id;
        setCurrentConversation(newConv);
        isNewConversation = true;
      } catch (error) {
        console.error('Error creating conversation:', error);
        return;
      }
    }

    // Add user message immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      created_at: new Date().toISOString()
    }]);

    setIsLoading(true);
    try {
      if (lexiModeEnabled) {
        // Lexi mode: send to Lexi API
        const mode = githubModeEnabled ? "github" : genZModeEnabled ? "gen-z" : "github";
        const response = await askLexi(message, mode);
        setMessages(prev => [
          ...prev,
          {
            role: 'lexi',
            content: response.answer,
            metadata: response.metadata,
            process_logs: response.process_logs,
            created_at: new Date().toISOString()
          }
        ]);
      } else {
        // Default: send to your own backend
        const response = await chatAPI.sendMessage(convId, message, githubModeEnabled, genZModeEnabled);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: response.response,
          created_at: new Date().toISOString()
        }]);

        // Update conversation title only for the FIRST message
        if (isFirstMessage && (isNewConversation || currentConversation?.title === 'New Chat')) {
          try {
            const titlepreview = message.substring(0, 50).trim();
            await chatAPI.updateConversation(convId, titlepreview);
          } catch (error) {
            console.error('Error updating conversation title:', error);
          }
        }

        await loadConversations();
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteConversation = async (conversationId) => {
    try {
      await chatAPI.deleteConversation(conversationId);
      if (currentConversation?.id === conversationId) {
        setCurrentConversation(null);
        setMessages([]);
      }
      await loadConversations();
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const handleShareConversation = async (conversationId) => {
    try {
      const result = await chatAPI.shareConversation(conversationId);
      const shareUrl = `${window.location.origin}/shared/${result.share_id}`;
      
      // Copy to clipboard
      navigator.clipboard.writeText(shareUrl);
      alert('Share link copied to clipboard!');
    } catch (error) {
      console.error('Error sharing conversation:', error);
    }
  };

  const handleProfileClick = () => {
    setShowProfileModal(true);
    window.history.pushState(null, '', '/profile');
  };

  const handleCloseProfileModal = () => {
    setShowProfileModal(false);
    window.history.pushState(null, '', '/');
  };

  const handleAdminClick = () => {
    setShowAdminPanel(true);
  };

  const handleCloseAdminPanel = () => {
    setShowAdminPanel(false);
  };

  const handleToggleLexiMode = (enabled) => {
    setLexiModeEnabled(enabled);
    if (enabled) {
      setShowLexiTerminal(true);
    }
  };

  return (
    <Routes>
      <Route path="/shared/:shareId" element={<SharedView />} />
      <Route
        path="/*"
        element={
          <div className="flex h-screen bg-dark-gray text-lighter-gray overflow-hidden">
            {/* Sidebar */}
            <Sidebar
              conversations={conversations}
              currentConversation={currentConversation}
              onNewChat={handleNewChat}
              onSelectConversation={handleSelectConversation}
              onDeleteConversation={handleDeleteConversation}
              onShareConversation={handleShareConversation}
              portfolioInfo={portfolioInfo}
              isOpen={sidebarOpen}
              onToggle={() => setSidebarOpen(!sidebarOpen)}
              onProfileClick={handleProfileClick}
              onAdminClick={handleAdminClick}
            />

            {/* Main Chat Window */}
            <ChatWindow
              messages={messages}
              isLoading={isLoading}
              onSendMessage={handleSendMessage}
              portfolioInfo={portfolioInfo}
              currentConversation={currentConversation}
              githubModeEnabled={githubModeEnabled}
              onToggleGithubMode={setGithubModeEnabled}
              genZModeEnabled={genZModeEnabled}
              onToggleGenZMode={setGenZModeEnabled}
              lexiModeEnabled={lexiModeEnabled}
              onToggleLexiMode={handleToggleLexiMode}
            />

            {/* Profile Modal Overlay */}
            {showProfileModal && (
              <Profile portfolioInfo={portfolioInfo} projects={projects} onClose={handleCloseProfileModal} />
            )}

            {/* Admin Panel Modal */}
            {showAdminPanel && (
              <AdminPanel onClose={handleCloseAdminPanel} />
            )}

            {/* Lexi Terminal Modal */}
            <LexiTerminal
              isOpen={showLexiTerminal}
              onClose={() => setShowLexiTerminal(false)}
              mode={githubModeEnabled ? 'github' : genZModeEnabled ? 'gen-z' : 'github'}
            />
          </div>
        }
      />
    </Routes>
  );
  }

  function App() {
    return (
      <Router>
        <AppContent />
      </Router>
    );
  }

  export default App;
