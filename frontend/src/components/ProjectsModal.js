import React, { useState, useEffect } from 'react';
import { X, ExternalLink, Star, GitFork, Loader, Github } from 'lucide-react';
import { chatAPI } from '../api';

function ProjectsModal({ isOpen, onClose }) {
  const [repositories, setRepositories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [languages, setLanguages] = useState(new Set());

  useEffect(() => {
    if (isOpen) {
      fetchRepositories();
    }
  }, [isOpen]);

  const fetchRepositories = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const repos = await chatAPI.getGitHubRepositories();
      setRepositories(repos);

      // Extract unique languages
      const uniqueLanguages = new Set();
      repos.forEach(repo => {
        if (repo.language) {
          uniqueLanguages.add(repo.language);
        }
      });
      setLanguages(uniqueLanguages);
      setSelectedLanguage('all');
    } catch (err) {
      console.error('Error fetching repositories:', err);
      setError('Failed to load projects. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredRepositories = selectedLanguage === 'all'
    ? repositories
    : repositories.filter(repo => repo.language === selectedLanguage);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-[#1a1a1a] rounded-lg shadow-2xl shadow-black/50 max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col border border-[#404040]">
        {/* Header */}
        <div className="flex items-center justify-between p-6 bg-[#0d0d0d] border-b border-[#404040]">
          <div className="flex items-center gap-3">
            <Github size={24} className="text-white" />
            <div>
              <h2 className="text-2xl font-bold text-white">Projects & Repositories</h2>
              <p className="text-sm text-[#9ca3af] mt-1">View Sujan's latest work on GitHub</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-[#9ca3af] hover:text-white transition-colors p-2 hover:bg-[#2a2a2a] rounded-lg"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <Loader className="animate-spin mx-auto mb-3 text-[#404040]" size={32} />
                <p className="text-[#9ca3af]">Loading projects...</p>
              </div>
            </div>
          ) : error ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <p className="text-red-400 mb-4">{error}</p>
                <button
                  onClick={fetchRepositories}
                  className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors"
                >
                  Try Again
                </button>
              </div>
            </div>
          ) : (
            <div className="p-6 space-y-6">
              {/* Language Filter */}
              {languages.size > 0 && (
                <div>
                  <p className="text-sm font-medium text-white mb-3">Filter by Language:</p>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => setSelectedLanguage('all')}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                        selectedLanguage === 'all'
                          ? 'bg-white text-black'
                          : 'bg-[#2a2a2a] text-[#d1d5db] hover:bg-[#3a3a3a]'
                      }`}
                    >
                      All ({repositories.length})
                    </button>
                    {Array.from(languages).sort().map(language => {
                      const count = repositories.filter(r => r.language === language).length;
                      return (
                        <button
                          key={language}
                          onClick={() => setSelectedLanguage(language)}
                          className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                            selectedLanguage === language
                              ? 'bg-white text-black'
                              : 'bg-[#2a2a2a] text-[#d1d5db] hover:bg-[#3a3a3a]'
                          }`}
                        >
                          {language} ({count})
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Repositories Grid */}
              <div className="grid gap-4">
                {filteredRepositories.length === 0 ? (
                  <p className="text-center text-[#9ca3af] py-8">No projects found with this filter.</p>
                ) : (
                  filteredRepositories.map((repo, idx) => (
                    <a
                      key={idx}
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group p-4 bg-[#2a2a2a] hover:bg-[#3a3a3a] rounded-lg border border-[#404040] hover:border-[#505050] transition-all duration-300 cursor-pointer hover:shadow-lg hover:shadow-white/10"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h3 className="font-bold text-white group-hover:text-blue-300 transition-colors text-lg">
                            {repo.name}
                            <ExternalLink size={14} className="inline ml-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                          </h3>
                          {repo.language && (
                            <p className="text-xs text-[#9ca3af] font-medium">
                              {repo.language}
                            </p>
                          )}
                        </div>
                        <div className="flex items-center gap-4 ml-4 text-sm text-[#9ca3af] flex-shrink-0">
                          <div className="flex items-center gap-1">
                            <Star size={14} />
                            <span>{repo.stars}</span>
                          </div>
                          {repo.forks > 0 && (
                            <div className="flex items-center gap-1">
                              <GitFork size={14} />
                              <span>{repo.forks}</span>
                            </div>
                          )}
                        </div>
                      </div>

                      <p className="text-sm text-[#d1d5db] mb-3">
                        {repo.description || 'No description available'}
                      </p>

                      {repo.topics && repo.topics.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {repo.topics.slice(0, 5).map((topic, i) => (
                            <span
                              key={i}
                              className="px-2 py-1 bg-[#1a1a1a] text-[#9ca3af] text-xs rounded-full border border-[#404040]"
                            >
                              {topic}
                            </span>
                          ))}
                        </div>
                      )}
                    </a>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-[#0d0d0d] border-t border-[#404040] px-6 py-4 text-center">
          <p className="text-xs text-[#9ca3af]">
            Visit{' '}
            <a
              href="https://github.com/sujanmhrjn1301"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 transition-colors underline"
            >
              GitHub profile
            </a>
            {' '}to see all projects
          </p>
        </div>
      </div>
    </div>
  );
}

export default ProjectsModal;
