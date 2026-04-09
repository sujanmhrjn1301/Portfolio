import React, { useState } from 'react';
import { Upload, X, Lock, AlertCircle } from 'lucide-react';

function AdminPanel({ onClose }) {
  const [password, setPassword] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
    } else {
      setError('Please select a valid PDF file');
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (!password || !selectedFile) {
      setError('Please enter password and select a file');
      return;
    }

    setUploading(true);
    setMessage('');
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('password', password);

      const response = await fetch('/upload-cv', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`✅ ${data.message}`);
        setPassword('');
        setSelectedFile(null);
        
        // Close admin panel after 2 seconds
        setTimeout(() => {
          onClose();
        }, 2000);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Upload failed');
      }
    } catch (err) {
      setError('Error uploading file: ' + err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-[#2a2a2a] border border-[#404040] rounded-lg max-w-md w-full shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-[#404040]">
          <div className="flex items-center gap-2">
            <Lock size={20} className="text-blue-400" />
            <h2 className="text-xl font-bold text-white">Admin Panel</h2>
          </div>
          <button
            onClick={onClose}
            className="text-[#9ca3af] hover:text-white transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {/* Admin Password Input */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Admin Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter admin password"
                disabled={uploading}
                className="w-full bg-[#1a1a1a] border border-[#404040] rounded-lg px-4 py-2 text-white placeholder-[#9ca3af] focus:outline-none focus:border-blue-400 transition-colors disabled:opacity-50"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9ca3af] hover:text-white"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          {/* File Upload Area */}
          <div>
            <label className="block text-sm font-medium text-white mb-2">
              Upload CV File
            </label>
            <label className="relative flex items-center justify-center w-full border-2 border-dashed border-[#404040] hover:border-blue-400 rounded-lg p-6 cursor-pointer transition-colors bg-[#1a1a1a]/50">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                disabled={uploading}
                className="hidden"
              />
              <div className="text-center">
                <Upload size={32} className="mx-auto mb-2 text-[#9ca3af]" />
                <p className="text-sm font-medium text-white">
                  {selectedFile ? selectedFile.name : 'Click to select PDF'}
                </p>
                <p className="text-xs text-[#9ca3af] mt-1">or drag and drop</p>
              </div>
            </label>
          </div>

          {/* Error Message */}
          {error && (
            <div className="flex gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
              <AlertCircle size={18} className="text-red-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          {/* Success Message */}
          {message && (
            <div className="flex gap-2 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
              <p className="text-sm text-green-400">{message}</p>
            </div>
          )}

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={!password || !selectedFile || uploading}
            className="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-2 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                Uploading...
              </>
            ) : (
              <>
                <Upload size={18} />
                Update CV
              </>
            )}
          </button>

          <p className="text-xs text-[#9ca3af] text-center">
            Your knowledge base will update instantly after upload
          </p>
        </div>
      </div>
    </div>
  );
}

export default AdminPanel;
