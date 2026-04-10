import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Loader } from 'lucide-react';
import { askLexi } from '../api';

function LexiTerminal({ isOpen, onClose, mode = 'github' }) {
  const [input, setInput] = useState('');
  const [terminal, setTerminal] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const terminalEndRef = useRef(null);

  const scrollToBottom = () => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [terminal]);

  useEffect(() => {
    if (isOpen && terminal.length === 0) {
      setTerminal([
        {
          type: 'system',
          content: '=== Lexi Terminal ===',
        },
        {
          type: 'system',
          content: 'Type your query and press Enter to ask Lexi',
        },
        {
          type: 'system',
          content: '',
        },
      ]);
    }
  }, [isOpen]);

  const handleSendQuery = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Add user input to terminal
    setTerminal(prev => [
      ...prev,
      {
        type: 'user',
        content: `> ${input}`,
      },
    ]);

    setIsLoading(true);
    const query = input;
    setInput('');

    try {
      const response = await askLexi(query, mode);

      // Add Lexi response to terminal
      setTerminal(prev => [
        ...prev,
        {
          type: 'lexi',
          content: response.answer,
        },
        ...(response.metadata
          ? [{ type: 'metadata', content: `📌 Source: ${response.metadata}` }]
          : []),
        ...(response.process_logs && response.process_logs.length > 0
          ? [
              {
                type: 'logs',
                content: response.process_logs
                  .map((log, idx) => `[${idx + 1}] ${log}`)
                  .join('\n'),
              },
            ]
          : []),
        {
          type: 'system',
          content: '',
        },
      ]);
    } catch (error) {
      setTerminal(prev => [
        ...prev,
        {
          type: 'error',
          content: `❌ Error: ${error.message}`,
        },
        {
          type: 'system',
          content: '',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-[#0d0d0d] border border-[#404040] rounded-lg shadow-2xl w-full max-w-2xl h-[70vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-[#404040] bg-[#1a1a1a]">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <h2 className="text-white font-semibold">Lexi Terminal</h2>
          </div>
          <button
            onClick={onClose}
            className="text-[#9ca3af] hover:text-white transition-colors p-1 hover:bg-[#2a2a2a] rounded"
            title="Close"
          >
            <X size={20} />
          </button>
        </div>

        {/* Terminal Output */}
        <div className="flex-1 overflow-y-auto bg-[#0d0d0d] p-4 font-mono text-sm space-y-2">
          {terminal.map((line, idx) => (
            <div
              key={idx}
              className={`${
                line.type === 'user'
                  ? 'text-blue-400'
                  : line.type === 'lexi'
                  ? 'text-green-400'
                  : line.type === 'error'
                  ? 'text-red-400'
                  : line.type === 'metadata'
                  ? 'text-yellow-400'
                  : line.type === 'logs'
                  ? 'text-[#9ca3af]'
                  : 'text-[#9ca3af]'
              }`}
              style={{
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                lineHeight: '1.5',
              }}
            >
              {line.content}
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-green-400">
              <Loader size={16} className="animate-spin" />
              <span>Lexi is thinking...</span>
            </div>
          )}
          <div ref={terminalEndRef} />
        </div>

        {/* Input Area */}
        <form
          onSubmit={handleSendQuery}
          className="border-t border-[#404040] bg-[#1a1a1a] p-4"
        >
          <div className="flex gap-2">
            <span className="text-green-400 font-mono text-sm flex-shrink-0">$</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your query..."
              disabled={isLoading}
              className="flex-1 bg-transparent text-white placeholder-[#9ca3af] focus:outline-none font-mono text-sm"
              autoFocus
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="text-white hover:text-green-400 disabled:opacity-50 transition-colors p-1 hover:bg-[#2a2a2a] rounded disabled:hover:bg-transparent"
              title="Send"
            >
              <Send size={18} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LexiTerminal;
