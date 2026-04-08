import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import SharedView from './components/SharedView';
import Profile from './components/Profile';
import { chatAPI } from './api';
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
        const username = 'sujanmhrjn1301'; // Replace with your GitHub username
        const response = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`);
        if (!response.ok) throw new Error('Failed to fetch GitHub projects');
        
        const repos = await response.json();
        // Filter out forks and map to project format
        const projectsData = repos
          .filter(repo => !repo.fork) // Only include original projects
          .map(repo => ({
            title: repo.name,
            description: repo.description || 'No description available',
            link: repo.html_url,
            language: repo.language,
            stars: repo.stargazers_count,
            updated: repo.updated_at
          }));
        
        setProjects(projectsData);
      } catch (error) {
        console.error('Error fetching GitHub projects:', error);
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
      const response = await chatAPI.sendMessage(convId, message, githubModeEnabled, genZModeEnabled);
      
      // Add assistant response after API call
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
            />

            {/* Profile Modal Overlay */}
            {showProfileModal && (
              <Profile portfolioInfo={portfolioInfo} projects={projects} onClose={handleCloseProfileModal} />
            )}
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
