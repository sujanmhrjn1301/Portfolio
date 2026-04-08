import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { ExternalLink } from 'lucide-react';

function MessageBubble({ message, isNew = false }) {
  const isUser = message.role === 'user';
  const [displayedText, setDisplayedText] = useState(isUser ? message.content : '');

  // Typewriter effect only for NEW AI messages
  useEffect(() => {
    if (isUser) {
      setDisplayedText(message.content);
      return;
    }

    // If not a new message, display all text instantly (from history)
    if (!isNew) {
      setDisplayedText(message.content);
      return;
    }

    let currentIndex = 0;
    const fullText = message.content;
    
    const typeInterval = setInterval(() => {
      if (currentIndex <= fullText.length) {
        setDisplayedText(fullText.slice(0, currentIndex));
        currentIndex++;
      } else {
        clearInterval(typeInterval);
      }
    }, 15); // Adjust speed: lower = faster (15ms per character)

    return () => clearInterval(typeInterval);
  }, [message.content, isUser, isNew]);

  const markdownComponents = {
    p: ({ children }) => <p className="mb-2 last:mb-0 text-[#ececf1] leading-relaxed">{children}</p>,
    strong: ({ children }) => <strong className="font-semibold text-white">{children}</strong>,
    em: ({ children }) => <em className="italic text-[#b3bcc6]">{children}</em>,
    a: ({ href, children }) => (
      <a 
        href={href} 
        target="_blank" 
        rel="noopener noreferrer" 
        className="inline-flex items-center gap-1 text-[#d1d5db] hover:text-white font-medium transition-colors duration-200"
      >
        {children}
        <ExternalLink size={14} className="flex-shrink-0" />
      </a>
    ),
    ul: ({ children }) => <ul className="list-none mb-3 space-y-2 pl-6 text-[#ececf1]">{children}</ul>,
    ol: ({ children }) => <ol className="list-decimal list-inside mb-3 space-y-2 pl-4 text-[#ececf1]">{children}</ol>,
    li: ({ children }) => <li className="text-[#ececf1] leading-relaxed">• {children}</li>,
    code: ({ inline, children }) => {
      if (inline) {
        return <code className="bg-[#2d2d30] px-2 py-1 rounded text-[#ce9178] font-mono text-sm border border-[#404040]">{children}</code>;
      }
      return <code className="block bg-[#2d2d30] p-3 rounded my-2 text-[#ce9178] font-mono text-sm overflow-x-auto border border-[#404040]">{children}</code>;
    },
    pre: ({ children }) => <pre className="bg-[#2d2d30] p-3 rounded my-2 overflow-x-auto border border-[#404040]">{children}</pre>,
    blockquote: ({ children }) => (
      <blockquote className="border-l-3 border-[#404040] pl-4 my-2 italic text-[#9ca3af]">{children}</blockquote>
    ),
    hr: () => <hr className="my-4 border-[#404040]" />,
    h1: ({ children }) => <h1 className="text-lg font-bold mb-3 text-white leading-tight mt-3">{children}</h1>,
    h2: ({ children }) => <h2 className="text-base font-bold mb-2 text-white leading-tight mt-2">{children}</h2>,
    h3: ({ children }) => <h3 className="font-semibold mb-1 text-white leading-tight mt-1">{children}</h3>,
  };

  return (
    <div className={`flex gap-2 sm:gap-3 mb-3 sm:mb-4 px-2 sm:px-0 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Message Content */}
      <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-xs sm:max-w-2xl`}>
        <div
          className={`rounded-lg px-3 sm:px-4 py-2 sm:py-3 transition-all duration-300 ${
            isUser
              ? 'bg-[#3a3a3a] text-white'
              : 'bg-transparent text-[#ececf1]'
          }`}
        >
          {isUser ? (
            <p className="leading-relaxed whitespace-pre-wrap text-sm sm:text-base">{message.content}</p>
          ) : (
            <div className="leading-relaxed max-w-none text-sm sm:text-base">
              <ReactMarkdown components={markdownComponents}>
                {displayedText}
              </ReactMarkdown>
              {displayedText.length < message.content.length && (
                <span className="inline-block ml-1 w-2 h-5 bg-white animate-pulse"></span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
