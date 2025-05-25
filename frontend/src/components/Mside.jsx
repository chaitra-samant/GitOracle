import React from "react";
import { useNavigate } from "react-router-dom";
import {
  Plus,
  Trash2,
  ExternalLink,
  MessageCircle,
  GitBranch,
} from "lucide-react";
import logo2 from "../assets/logo2.jpg";

const Mside = ({
  conversations,
  activeConversation,
  selectConversation,
  deleteConversation,
  startNewChat,
}) => {
  const navigate = useNavigate();

  const formatTimeAgo = (timestamp) => {
    // Simple time ago formatting - you might want to use a library like date-fns
    const now = new Date().getTime();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return "Just now";
  };

  return (
    <div className="w-80 bg-slate-900/50 backdrop-blur-sm border-r border-purple-500/20 flex flex-col">
      <div className="p-4 border-b border-purple-500/20">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <img
              src={logo2}
              alt="Logo"
              className="w-10 h-10 mr-2 rounded-full object-cover"
            />
            <h1 className="text-xl font-bold text-white">
              <button
                onClick={() => navigate("/")}
                className="hover:text-purple-300 transition-colors"
              >
                GitOracle
              </button>
            </h1>
          </div>
          <button
            onClick={startNewChat}
            className="p-2 hover:bg-purple-500/20 rounded-lg transition-colors group"
            title="Analyze New Repository"
          >
            <Plus className="w-5 h-5 text-purple-400 group-hover:text-purple-300" />
          </button>
        </div>

        {conversations.length > 0 && (
          <div className="text-xs text-gray-400">
            {conversations.length}{" "}
            {conversations.length === 1 ? "repository" : "repositories"}{" "}
            analyzed
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {conversations.length === 0 ? (
          <div className="text-center text-gray-400 mt-8">
            <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="font-medium">No conversations yet</p>
            <p className="text-sm mt-1">Start by analyzing a repository</p>
            <button
              onClick={startNewChat}
              className="mt-4 px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 rounded-lg text-sm text-purple-300 transition-colors"
            >
              Get Started
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="text-xs text-gray-500 uppercase tracking-wide mb-3 px-2">
              Recent Analyses
            </div>
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`group p-3 rounded-lg cursor-pointer transition-all hover:bg-purple-500/10 ${
                  activeConversation === conversation.id
                    ? "bg-purple-500/20 border border-purple-500/30"
                    : "hover:border hover:border-purple-500/20"
                }`}
                onClick={() => selectConversation(conversation.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center mb-1">
                      <GitBranch className="w-3 h-3 text-purple-400 mr-1.5 flex-shrink-0" />
                      <h3 className="text-white font-medium text-sm truncate">
                        {conversation.repository.split("/")[1]}
                      </h3>
                    </div>
                    <p className="text-gray-400 text-xs truncate">
                      {conversation.repository}
                    </p>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-gray-500 text-xs">
                        {conversation.messages.length}{" "}
                        {conversation.messages.length === 1
                          ? "message"
                          : "messages"}
                      </span>
                      <span className="text-gray-500 text-xs">
                        {formatTimeAgo(conversation.id)}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity ml-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        window.open(conversation.url, "_blank");
                      }}
                      className="p-1 hover:bg-purple-500/20 rounded transition-colors"
                      title="Open Repository"
                    >
                      <ExternalLink className="w-3 h-3 text-gray-400" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (window.confirm("Delete this conversation?")) {
                          deleteConversation(conversation.id);
                        }
                      }}
                      className="p-1 hover:bg-red-500/20 rounded transition-colors"
                      title="Delete Conversation"
                    >
                      <Trash2 className="w-3 h-3 text-red-400" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-purple-500/20">
        <div className="text-xs text-gray-500 text-center">
          <span>Powered by </span>
          <span className="text-purple-400 font-medium">GitOracle RAG</span>
        </div>
      </div>
    </div>
  );
};

export default Mside;
