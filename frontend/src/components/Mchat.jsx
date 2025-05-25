import React, { useEffect, useRef } from "react";
import {
  Send,
  Radio,
  MessageCircle,
  ExternalLink,
  Code,
  FileText,
  AlertCircle,
} from "lucide-react";
import logo2 from "../assets/logo2.jpg";

const MChat = ({
  activeConversation,
  repositoryName,
  chatHistory,
  currentMessage,
  setCurrentMessage,
  handleSendMessage,
  isTyping,
}) => {
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatHistory, isTyping]);

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Function to render markdown-like content
  const renderMarkdown = (content) => {
    // Simple markdown rendering for code blocks
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const inlineCodeRegex = /`([^`]+)`/g;
    const boldRegex = /\*\*(.*?)\*\*/g;
    const italicRegex = /\*(.*?)\*/g;

    let html = content;

    // Replace code blocks
    html = html.replace(codeBlockRegex, (match, language, code) => {
      return `<pre class="bg-slate-900 p-4 rounded-lg my-4 overflow-x-auto border border-purple-500/20"><code class="text-purple-300">${code.trim()}</code></pre>`;
    });

    // Replace inline code
    html = html.replace(
      inlineCodeRegex,
      '<code class="bg-slate-800 px-2 py-1 rounded text-purple-300">$1</code>'
    );

    // Replace bold text
    html = html.replace(
      boldRegex,
      '<strong class="font-semibold text-purple-300">$1</strong>'
    );

    // Replace italic text
    html = html.replace(
      italicRegex,
      '<em class="italic text-purple-200">$1</em>'
    );

    // Replace line breaks
    html = html.replace(/\n/g, "<br>");

    return html;
  };

  const suggestedQuestions = [
    "What is the main architecture of this project?",
    "Explain the authentication system",
    "How does the database interaction work?",
    "What are the main API endpoints?",
    "Show me the project structure",
    "What dependencies does this project use?",
  ];

  return (
    <div className="flex flex-col h-screen w-full">
      {activeConversation ? (
        <>
          {/* Header - Fixed height */}
          <div className="flex-shrink-0 p-4 border-b border-purple-500/20 bg-slate-900/30">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-white">
                  {repositoryName.split("/")[1]}
                </h2>
                <p className="text-gray-400 text-sm">{repositoryName}</p>
              </div>
              <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                <Radio/>
              </span>
            </div>
          </div>

          {/* Chat Messages - Fixed height with scrollbar */}
          <div
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto p-4"
            style={{
              scrollbarWidth: "thin",
              scrollbarColor: "#8b5cf6 #1e293b",
            }}
          >
            {chatHistory.length === 0 ? (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-gray-400">
                  <MessageCircle className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-semibold mb-2">
                    Repository Analyzed!
                  </h3>
                  <p className="mb-6">Ask me anything about the codebase...</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-4xl mx-auto">
                    {suggestedQuestions.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => setCurrentMessage(question)}
                        className="p-3 bg-purple-500/10 hover:bg-purple-500/20 rounded-lg text-left transition-colors border border-purple-500/20 hover:border-purple-500/40"
                      >
                        <div className="flex items-start">
                          <Code className="w-4 h-4 text-purple-400 mr-2 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-300">
                            {question}
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                {chatHistory.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${
                      msg.type === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[85%] p-4 rounded-lg ${
                        msg.type === "user"
                          ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white"
                          : msg.isError
                          ? "bg-red-500/10 text-red-300 border border-red-500/20"
                          : "bg-slate-800/50 text-gray-200 border border-purple-500/20"
                      }`}
                    >
                      {msg.type === "ai" && msg.isError && (
                        <div className="flex items-center mb-2">
                          <AlertCircle className="w-4 h-4 text-red-400 mr-2" />
                          <span className="text-sm font-medium text-red-400">
                            Error
                          </span>
                        </div>
                      )}

                      <div
                        className="prose prose-invert max-w-none"
                        dangerouslySetInnerHTML={{
                          __html:
                            msg.type === "ai"
                              ? renderMarkdown(msg.content)
                              : msg.content,
                        }}
                      />

                      {msg.sources && msg.sources.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-purple-500/20">
                          <div className="flex items-center mb-2">
                            <FileText className="w-4 h-4 text-purple-400 mr-2" />
                            <span className="text-sm font-medium text-purple-300">
                              Sources:
                            </span>
                          </div>
                          <div className="space-y-1">
                            {msg.sources.map((source, index) => (
                              <div
                                key={index}
                                className="flex items-center text-sm text-gray-400"
                              >
                                <ExternalLink className="w-3 h-3 mr-2" />
                                <span className="truncate">{source}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <p className="text-xs mt-3 opacity-70">{msg.timestamp}</p>
                    </div>
                  </div>
                ))}

                {isTyping && (
                  <div className="flex justify-start">
                    <div className="max-w-[85%] p-4 rounded-lg bg-slate-800/50 border border-purple-500/20">
                      <div className="flex items-center space-x-3">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                          <div
                            className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                            style={{ animationDelay: "0.1s" }}
                          ></div>
                          <div
                            className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"
                            style={{ animationDelay: "0.2s" }}
                          ></div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-gray-400 text-sm animate-pulse">
                            Analyzing codebase
                          </span>
                          <div className="text-purple-400 text-sm">
                            <span className="animate-ping">.</span>
                            <span
                              className="animate-ping"
                              style={{ animationDelay: "0.3s" }}
                            >
                              .
                            </span>
                            <span
                              className="animate-ping"
                              style={{ animationDelay: "0.6s" }}
                            >
                              .
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Invisible div to scroll to */}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area - Fixed height */}
          <div className="flex-shrink-0 p-4 border-t border-purple-500/20 bg-slate-900/30">
            <div className="flex items-end space-x-4">
              <textarea
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about the codebase..."
                className="flex-1 px-4 py-3 bg-slate-800/50 border border-purple-500/30 rounded-lg text-white placeholder-gray-400 resize-none focus:outline-none focus:border-purple-400 focus:ring-2 focus:ring-purple-400/20"
                rows="1"
                disabled={isTyping}
              />
              <button
                onClick={handleSendMessage}
                disabled={!currentMessage.trim() || isTyping}
                className="p-3 mb-0.75 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg text-white hover:shadow-lg hover:shadow-purple-500/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-5.5 h-5.5" />
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="flex-1 flex items-center justify-center text-center text-gray-400">
          <div>
            <img
              src={logo2}
              alt="Logo"
              className="w-80 h-80 rounded-full mx-auto mb-6 opacity-20 object-cover"
            />
            <h2 className="text-2xl font-semibold mb-4">
              Welcome to GitOracle
            </h2>
            <p className="text-lg mb-6">
              Analyze any GitHub repository to get started
            </p>
          </div>
        </div>
      )}

      <style jsx>{`
        /* Custom scrollbar styles for Webkit browsers */
        .overflow-y-auto::-webkit-scrollbar {
          width: 8px;
        }

        .overflow-y-auto::-webkit-scrollbar-track {
          background: #1e293b;
          border-radius: 4px;
        }

        .overflow-y-auto::-webkit-scrollbar-thumb {
          background: #8b5cf6;
          border-radius: 4px;
        }

        .overflow-y-auto::-webkit-scrollbar-thumb:hover {
          background: #a855f7;
        }

        /* Enhanced typing animation */
        @keyframes typewriter {
          from {
            opacity: 0.3;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes fade-in-out {
          0%,
          100% {
            opacity: 0.4;
          }
          50% {
            opacity: 1;
          }
        }

        .animate-ping {
          animation: fade-in-out 1.5s ease-in-out infinite;
        }

        .animate-pulse {
          animation: typewriter 1s ease-in-out infinite alternate;
        }
      `}</style>
    </div>
  );
};

export default MChat;
