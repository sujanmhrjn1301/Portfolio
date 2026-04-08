import React, { useState } from 'react';
import { Plus, Trash2, Share2, Menu, X, Github, Linkedin, Mail, Phone, MapPin, Sparkles, MessageCircle } from 'lucide-react';

function Sidebar({
  conversations,
  currentConversation,
  onNewChat,
  onSelectConversation,
  onDeleteConversation,
  onShareConversation,
  portfolioInfo,
  isOpen,
  onToggle,
  onProfileClick,
}) {
  const [hoverConvId, setHoverConvId] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);

  return (
    <>
      {/* Mobile toggle button */}
      <button
        onClick={onToggle}
        className="absolute top-4 left-4 md:hidden bg-[#1a1a1a] hover:bg-[#2a2a2a] text-white p-2 rounded-lg z-50"
      >
        {isOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed md:relative w-64 h-screen bg-[#0d0d0d] flex flex-col transition-transform duration-300 z-40 shadow-lg shadow-black/40
          ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        {/* Header */}
        <div className="p-3 sm:p-4 bg-[#0d0d0d]">
          {/* AI Name */}
          <div className="mb-4 sm:mb-6">
            <div className="flex items-center gap-2">
              <Sparkles size={18} className="sm:w-5 sm:h-5 text-blue-400" />
              <h1 className="font-caveat text-2xl sm:text-4xl font-bold text-white">Memora</h1>
            </div>
          </div>

          {/* New Chat Button */}
          <button
            onClick={onNewChat}
            className="w-full flex items-center justify-start gap-2 bg-[#1a1a1a] hover:bg-[#2a2a2a] active:bg-[#2a2a2a] text-white py-2.5 sm:py-3 px-3 sm:px-4 rounded-lg font-medium transition-all duration-300 group whitespace-nowrap mb-2 sm:mb-3 min-h-10"
          >
            <Plus size={18} className="group-hover:rotate-90 transition-transform duration-300" />
            <span className="text-sm sm:text-base">New Chat</span>
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto px-2 sm:px-3 py-3 sm:py-4">
          <p className="text-xs font-semibold text-[#9ca3af] uppercase mb-2 sm:mb-3 px-2 tracking-wider">
            Chat History
          </p>

          {conversations.length === 0 ? (
            <div className="text-center py-8">
              <Sparkles size={24} className="text-[#404040] mx-auto mb-2 opacity-50" />
              <p className="text-sm text-[#9ca3af]">No conversations yet</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                onMouseEnter={() => setHoverConvId(conv.id)}
                onMouseLeave={() => setHoverConvId(null)}
                className={`p-2 sm:p-3 rounded-lg mb-1 sm:mb-2 cursor-pointer transition-colors duration-300 relative min-h-10 ${
                    currentConversation?.id === conv.id
                      ? 'bg-[#1a1a1a]'
                      : 'bg-transparent hover:bg-[#1a1a1a]'
                  }`}
                onClick={() => onSelectConversation(conv)}
              >
                <div className="relative flex justify-between items-start gap-2">
                  <div className="flex items-start gap-2 flex-1 min-w-0">
                    <MessageCircle size={14} className="text-[#9ca3af] flex-shrink-0 mt-1" />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-medium text-[#d1d5db] truncate">
                        {conv.title}
                      </p>
                    </div>
                  </div>

                  <div className={`flex gap-1 transition-opacity duration-200 ${hoverConvId === conv.id ? 'opacity-100' : 'opacity-0 pointer-events-none'} flex-shrink-0`}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onShareConversation(conv.id);
                      }}
                      className="p-1.5 sm:p-2 rounded transition-opacity duration-200 active:bg-[#2a2a2a] min-h-8 min-w-8"
                      title="Share chat"
                    >
                      <Share2 size={14} className="text-[#d1d5db] hover:text-white" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setDeleteConfirm(conv.id);
                      }}
                      className="p-1.5 sm:p-2 rounded transition-opacity duration-200 active:bg-[#2a2a2a] min-h-8 min-w-8"
                      title="Delete chat"
                    >
                      <Trash2 size={14} className="text-[#d1d5db] hover:text-red-300" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Portfolio Info Section - Enhanced */}
        {portfolioInfo && (
          <div className="p-3 sm:p-4 bg-[#0d0d0d]">
            <div className="flex items-center justify-between gap-2 sm:gap-3 group">
              {/* Name - Clickable to Profile (Left) */}
              <button
                onClick={onProfileClick}
                className="text-left hover:text-gray-300 transition-all flex-1 cursor-pointer"
              >
                <div className="flex items-center gap-2 mb-0.5 sm:mb-1">
                  <div className="h-8 w-8 bg-[#404040] rounded-full flex items-center justify-center text-white text-xs font-bold group-hover:scale-110 transition-transform">
                    {portfolioInfo.name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0 hidden sm:block">
                    <h3 className="font-bold text-[#d1d5db] text-sm group-hover:text-white transition-colors truncate">
                      {portfolioInfo.name}
                    </h3>
                    <p className="text-xs text-[#9ca3af] group-hover:text-gray-300 transition-colors">View Profile</p>
                  </div>
                </div>
              </button>

              {/* Social Links (Right) */}
              <div className="flex gap-1 sm:gap-1.5 flex-shrink-0">
                {portfolioInfo.github && (
                  <a
                    href={portfolioInfo.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-[#d1d5db] hover:text-white rounded-lg transition-all duration-300 hover:scale-110 min-h-8 min-w-8 flex items-center justify-center"
                    title="GitHub"
                  >
                    <Github size={16} />
                  </a>
                )}

                {portfolioInfo.linkedin && (
                  <a
                    href={portfolioInfo.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="p-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-[#d1d5db] hover:text-white rounded-lg transition-all duration-300 hover:scale-110 min-h-8 min-w-8 flex items-center justify-center"
                    title="LinkedIn"
                  >
                    <Linkedin size={16} />
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 md:hidden z-30"
          onClick={onToggle}
        />
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-[#202123] rounded-lg p-6 shadow-2xl max-w-sm mx-4 border border-[#2d2d3d]">
            <h3 className="text-lg font-semibold text-white mb-2">Delete chat?</h3>
            <p className="text-sm text-[#d1d5db] mb-6">This conversation will be deleted permanently.</p>
            
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setDeleteConfirm(null)}
                className="px-4 py-2 text-white bg-transparent border border-[#565869] hover:bg-[#2d2d3d] rounded-lg transition-colors duration-200 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  onDeleteConversation(deleteConfirm);
                  setDeleteConfirm(null);
                }}
                className="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors duration-200 font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Sidebar;
