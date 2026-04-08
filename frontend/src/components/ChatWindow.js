import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader, Download, MessageSquare, Zap, Brain, BookMarked, Github, Sparkles } from 'lucide-react';
import MessageBubble from './MessageBubble';

function ChatWindow({
  messages,
  isLoading,
  onSendMessage,
  portfolioInfo,
  currentConversation,
  githubModeEnabled,
  onToggleGithubMode,
  genZModeEnabled,
  onToggleGenZMode,
}) {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const prevConversationIdRef = useRef(currentConversation?.id);
  const prevMessageCountRef = useRef(messages.length);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
    // Update refs after rendering
    prevConversationIdRef.current = currentConversation?.id;
    prevMessageCountRef.current = messages.length;
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    setIsTyping(true);

    // Clear input immediately
    const messageToSend = input;
    setInput('');

    try {
      await onSendMessage(messageToSend);
    } finally {
      setIsTyping(false);
    }
  };

  const handleDownloadCV = () => {
    // Try to download CV from public folder
    const cvPath = '/Sujan-Maharjan-CV.pdf';
    const link = document.createElement('a');
    link.href = cvPath;
    link.download = 'Sujan-Maharjan-CV.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <main className="flex-1 flex flex-col bg-[#1a1a1a]">
      {/* Welcome Screen or Chat Area */}
      {messages.length === 0 && !isLoading ? (
        <div className="flex-1 flex flex-col items-center justify-center p-4 sm:p-6 bg-[#1a1a1a]">
          <div className="max-w-2xl w-full text-center">
            {/* Logo/Avatar */}
            <div className="mb-6 sm:mb-8">
              <div className="h-16 sm:h-20 w-16 sm:w-20 bg-gradient-to-br from-white to-gray-400 rounded-full mx-auto flex items-center justify-center shadow-lg shadow-white/30 animate-pulse-subtle">
                <Brain size={32} className="sm:w-10 sm:h-10 w-8 h-8 text-black" />
              </div>
            </div>

            <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold mb-2 sm:mb-4 text-white leading-tight">
              Hi, I'm <span className="font-caveat">Memora</span>
            </h1>
            <p className="text-base sm:text-xl text-white font-semibold mb-3">Sujan's AI Portfolio Assistant</p>
            {/* <p className="text-base text-[#d1d5db] mb-12 leading-relaxed max-w-xl mx-auto">
              Ask me anything about Sujan's experience, skills, projects, and background. 
              I'm here to help you learn more about him!
            </p> */}

            {/* Quick prompts */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 mb-8 sm:mb-10">
              {[
                {
                  title: "Tell me about Sujan's experience",
                  subtitle: 'Work history and roles',
                  icon: Zap,
                  color: 'from-gray-600 to-gray-400',
                },
                {
                  title: "What are Sujan's main skills?",
                  subtitle: 'Technical and soft skills',
                  icon: Brain,
                  color: 'from-gray-700 to-gray-500',
                },
                {
                  title: "Show me Sujan's projects",
                  subtitle: 'Notable works and contributions',
                  icon: BookMarked,
                  color: 'from-gray-600 to-gray-400',
                },
                {
                  title: "What is Sujan's education?",
                  subtitle: 'Academic background',
                  icon: MessageSquare,
                  color: 'from-gray-700 to-gray-500',
                },
              ].map((prompt, idx) => {
                const IconComponent = prompt.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      setInput(prompt.title);
                    }}
                    className="group relative p-3 sm:p-4 bg-[#1a1a1a] hover:bg-[#2a2a2a] active:bg-[#2a2a2a] rounded-lg text-left transition-all duration-300 border border-[#404040] hover:border-white/30 hover:shadow-lg hover:shadow-white/10 overflow-hidden"
                  >
                    {/* Hover gradient overlay */}
                    <div className={`absolute inset-0 bg-gradient-to-r ${prompt.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300 rounded-lg`}></div>
                    
                    <div className="relative flex items-start gap-3">
                      <div className={`bg-gradient-to-br ${prompt.color} p-2 rounded-lg flex-shrink-0 group-hover:shadow-lg group-hover:shadow-current/50 transition-all duration-300 transform group-hover:scale-110`}>
                        <IconComponent size={16} className="text-white" />
                      </div>
                      <div className="text-left flex-1">
                        <p className="font-medium text-white mb-1 text-xs sm:text-sm leading-snug group-hover:text-blue-300 transition-colors">{prompt.title}</p>
                        <p className="text-xs text-[#9ca3af] group-hover:text-[#d1d5db] transition-colors">{prompt.subtitle}</p>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Download CV Button */}
            {/* <button
              onClick={handleDownloadCV}
              className="inline-flex items-center gap-2 bg-gradient-to-r from-gray-700 to-gray-600 hover:from-gray-200 hover:to-gray-100 text-white hover:text-black font-medium py-3 px-8 rounded-lg transition-all duration-300 shadow-lg shadow-white/20 hover:shadow-white/40 hover:scale-105 group"
            >
              <Download size={18} className="group-hover:translate-y-1 transition-transform" />
              <span>Download CV</span>
            </button> */}
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto bg-[#1a1a1a]">
          <div className="max-w-3xl mx-auto px-3 sm:px-6 py-4 sm:py-8 space-y-3 sm:space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <Loader className="animate-spin mx-auto mb-3 text-[#404040]" size={24} />
                <p className="text-sm text-[#9ca3af]">Starting conversation...</p>
              </div>
            )}

            {messages.map((message, idx) => {
              // Only animate last AI message if: same conversation, new message added, and previous was user message
              const isSameConversation = prevConversationIdRef.current === currentConversation?.id;
              const isNewMessageAdded = messages.length > prevMessageCountRef.current;
              const isNew = isSameConversation && isNewMessageAdded && message.role !== 'user' && idx === messages.length - 1 && idx > 0 && messages[idx - 1].role === 'user';
              return <MessageBubble key={idx} message={message} isNew={isNew} />;
            })}

            {isLoading && (
              <p className="text-sm shimmer-text font-medium">Thinking...</p>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-[#1a1a1a] p-[0.625rem] md:p-[0.875rem]">
        {/* GitHub Mode Indicator */}
        {(githubModeEnabled || genZModeEnabled) && (
          <div className="max-w-3xl mx-auto mb-2 px-3 sm:px-4 py-2 bg-[#2a2a2a] border border-[#404040] rounded-lg flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
              {githubModeEnabled && (
                <>
                  <div className="flex items-center gap-2">
                    <Github size={14} className="sm:w-4 sm:h-4 w-3.5 h-3.5 text-blue-400" />
                    <span className="text-xs sm:text-sm font-medium text-blue-400">GitHub Mode</span>
                  </div>
                  <span className="text-xs text-[#9ca3af]">•</span>
                </>
              )}
              {genZModeEnabled && (
                <>
                  {githubModeEnabled && <span className="text-xs text-[#9ca3af]">•</span>}
                  <div className="flex items-center gap-2">
                    <Sparkles size={14} className="sm:w-4 sm:h-4 w-3.5 h-3.5 text-pink-400" />
                    <span className="text-xs sm:text-sm font-medium text-pink-400">Gen-Z Mode</span>
                  </div>
                </>
              )}
            </div>
            <button
              onClick={() => {
                if (githubModeEnabled && !genZModeEnabled) {
                  onToggleGithubMode(false);
                } else if (genZModeEnabled && !githubModeEnabled) {
                  onToggleGenZMode(false);
                } else {
                  onToggleGenZMode(false);
                }
              }}
              className="text-xs px-2 py-1 text-[#9ca3af] hover:text-white hover:bg-[#3a3a3a] rounded transition-colors"
            >
              Turn Off
            </button>
          </div>
        )}

        <form onSubmit={handleSendMessage} className="max-w-3xl mx-auto w-full">
          <div className="flex flex-col gap-3">
            {/* Mode Toggles */}
            <div className="flex items-center gap-2 px-3 sm:px-4 flex-wrap">
              <button
                type="button"
                onClick={() => onToggleGithubMode(!githubModeEnabled)}
                className={`flex items-center gap-2 px-3 py-2 sm:py-2 rounded-lg font-medium text-xs sm:text-sm transition-all duration-300 min-h-10 sm:min-h-auto ${
                  githubModeEnabled
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-400/50 shadow-lg shadow-blue-500/20'
                    : 'bg-[#2a2a2a] text-[#9ca3af] border border-[#404040] hover:border-[#505050] hover:text-white'
                }`}
                title="Toggle GitHub Mode"
              >
                <Github size={16} />
                <span className="hidden sm:inline">GitHub Mode</span>
                <span className="sm:hidden">GitHub</span>
              </button>
              {githubModeEnabled && (
                <span className="text-xs text-blue-400 animate-pulse">● Active</span>
              )}

              <button
                type="button"
                onClick={() => onToggleGenZMode(!genZModeEnabled)}
                className={`flex items-center gap-2 px-3 py-2 sm:py-2 rounded-lg font-medium text-xs sm:text-sm transition-all duration-300 min-h-10 sm:min-h-auto ${
                  genZModeEnabled
                    ? 'bg-pink-500/20 text-pink-400 border border-pink-400/50 shadow-lg shadow-pink-500/20'
                    : 'bg-[#2a2a2a] text-[#9ca3af] border border-[#404040] hover:border-[#505050] hover:text-white'
                }`}
                title="Toggle Gen-Z Mode"
              >
                <Sparkles size={16} />
                <span className="hidden sm:inline">Gen-Z Mode</span>
                <span className="sm:hidden">Gen-Z</span>
              </button>
              {genZModeEnabled && (
                <span className="text-xs text-pink-400 animate-pulse">● Active</span>
              )}
            </div>

            {/* Input Row */}
            <div className="flex gap-2 sm:gap-3 group w-full px-3 sm:px-4">
              <div className="flex-1 searchbar-aurora rounded-lg">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage(e);
                    }
                  }}
                  placeholder={
                    genZModeEnabled && githubModeEnabled
                      ? "Ask me anything (no cap)..."
                      : genZModeEnabled
                      ? "Ask me anything fr fr..."
                      : githubModeEnabled
                      ? "Ask me anything about the projects..."
                      : "Ask me about Sujan..."
                  }
                  disabled={isTyping || isLoading}
                  className="relative w-full bg-transparent rounded-lg px-3 sm:px-4 py-3 sm:py-3 text-white placeholder-[#9ca3af] focus:outline-none transition-all duration-300 disabled:opacity-50 text-sm min-h-10"
                />
              </div>
              <button
                type="submit"
                disabled={!input.trim() || isTyping || isLoading}
                className="bg-gradient-to-r from-gray-700 to-gray-600 hover:from-gray-200 hover:to-gray-100 hover:text-black disabled:opacity-40 text-white font-medium py-2 sm:py-3 px-3 sm:px-4 rounded-lg transition-all duration-300 flex items-center justify-center cursor-pointer shadow-lg shadow-white/20 hover:shadow-white/40 disabled:shadow-none hover:scale-105 disabled:hover:scale-100 group min-h-10"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </form>
      </div>
    </main>
  );
}

export default ChatWindow;
