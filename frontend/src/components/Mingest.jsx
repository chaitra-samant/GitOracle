import React from "react";
import { Github, AlertCircle, X } from "lucide-react";
import logo2 from "../assets/logo2.jpg";

const Mingest = ({
  githubUrl,
  setGithubUrl,
  isIngesting,
  ingestError,
  handleIngest,
  onClose,
}) => {
  const exampleUrls = [
    "https://github.com/facebook/react",
    "https://github.com/vercel/next.js",
    "https://github.com/microsoft/vscode",
  ];

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !isIngesting) {
      handleIngest();
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 backdrop-blur-lg rounded-2xl border border-purple-500/20 p-8 max-w-md w-full relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="text-center mb-6">
          <div className="flex items-center justify-center mb-4">
            <img
              src={logo2}
              alt="Logo"
              className="w-8 h-8 mr-2 rounded-full object-cover"
            />
            <h2 className="text-2xl font-bold text-white">GitOracle</h2>
          </div>
          <p className="text-gray-300">
            Enter GitHub repository URL to analyze
          </p>
        </div>

        <div className="mb-6">
          <div className="flex items-center">
            <Github className="w-6 h-6 text-purple-400 mr-2 mb-2" />
            <label className="block text-gray-300 mb-2 font-medium">
              Enter GitHub URL
            </label>
          </div>
          <input
            type="url"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="https://github.com/user/repository"
            className="w-full px-4 py-3 bg-slate-800/50 border border-purple-500/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
            disabled={isIngesting}
          />

          {ingestError && (
            <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start">
              <AlertCircle className="w-5 h-5 text-red-400 mr-2 mt-0.5 flex-shrink-0" />
              <p className="text-red-300 text-sm">{ingestError}</p>
            </div>
          )}
        </div>

        <div className="mb-6">
          <p className="text-gray-400 text-sm mb-3">Example repositories:</p>
          <div className="flex flex-wrap gap-2">
            {exampleUrls.map((url, index) => (
              <button
                key={index}
                onClick={() => setGithubUrl(url)}
                className="px-3 py-1 bg-purple-500/20 hover:bg-purple-500/30 rounded-full text-xs text-purple-300 transition-colors"
                disabled={isIngesting}
              >
                {url.split("/").pop()}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleIngest}
          disabled={!githubUrl.trim() || isIngesting}
          className="w-full bg-gradient-to-r from-purple-500 to-pink-500 px-6 py-3 rounded-lg text-white font-semibold hover:shadow-lg hover:shadow-purple-500/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {isIngesting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Analyzing Repository...
            </>
          ) : (
            "ANALYZE REPOSITORY"
          )}
        </button>

        {isIngesting && (
          <p className="text-center text-gray-400 text-sm mt-3">
            This may take a few minutes for large repositories...
          </p>
        )}
      </div>
    </div>
  );
};

export default Mingest;
