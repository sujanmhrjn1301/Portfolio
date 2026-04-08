import React, { useState, useEffect } from 'react';
import { ArrowLeft, Loader } from 'lucide-react';
import { useParams, useNavigate } from 'react-router-dom';
import { chatAPI } from '../api';
import MessageBubble from '../components/MessageBubble';

function SharedView() {
  const { shareId } = useParams();
  const navigate = useNavigate();
  const [conversation, setConversation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadSharedConversation = async () => {
      try {
        setLoading(true);
        const data = await chatAPI.getSharedConversation(shareId);
        setConversation(data);
      } catch (err) {
        setError('Could not load this shared conversation. It may have been deleted.');
        console.error('Error loading shared conversation:', err);
      } finally {
        setLoading(false);
      }
    };

    loadSharedConversation();
  }, [shareId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-dark-gray">
        <div className="text-center">
          <Loader className="animate-spin mx-auto mb-2 text-blue-600" size={32} />
          <p className="text-lighter-gray">Loading shared conversation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-dark-gray">
        <div className="text-center max-w-md">
          <h2 className="text-2xl font-bold text-lighter-gray mb-2">Oops!</h2>
          <p className="text-light-gray mb-4">{error}</p>
          <a
            href="/"
            className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            <ArrowLeft size={18} />
            Back to Portfolio
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-gray text-lighter-gray">
      {/* Header */}
      <div className="bg-medium-gray border-b border-light-gray p-4">
        <div className="max-w-4xl mx-auto">
          <a
            href="/"
            className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors mb-4"
          >
            <ArrowLeft size={18} />
            Back to Portfolio
          </a>
          {conversation && (
            <h1 className="text-2xl font-bold">{conversation.title}</h1>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="max-w-4xl mx-auto p-4 md:p-6">
        {conversation?.messages && conversation.messages.length > 0 ? (
          <div className="space-y-4">
            {conversation.messages.map((message, idx) => (
              <MessageBubble key={idx} message={message} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-light-gray">No messages in this conversation</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-medium-gray border-t border-light-gray p-4 text-center text-sm text-light-gray">
        <p>This is a shared conversation from Sujan Maharjan's Portfolio</p>
      </div>
    </div>
  );
}

export default SharedView;
