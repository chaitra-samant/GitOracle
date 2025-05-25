import React, { useState } from "react";
import Mingest from "./Mingest";
import Mside from "./Mside";
import MChat from "./MChat";

const API_BASE_URL = "http://localhost:8000"; // Adjust this to your FastAPI server URL

const Main = () => {
  const [showPopup, setShowPopup] = useState(true);
  const [githubUrl, setGithubUrl] = useState("");
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestError, setIngestError] = useState("");
  const [currentMessage, setCurrentMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [repositoryName, setRepositoryName] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  // Function to handle repository ingestion
  const handleIngest = async () => {
    if (!githubUrl.trim()) return;

    setIsIngesting(true);
    setIngestError("");

    try {
      const response = await fetch(`${API_BASE_URL}/ingest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ github_url: githubUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to ingest repository");
      }

      if (data.success) {
        // Extract repository name from URL
        const repoMatch = githubUrl.match(/github\.com\/([^\/]+\/[^\/]+)/);
        const repoName = repoMatch ? repoMatch[1] : "Unknown Repository";
        setRepositoryName(repoName);

        // Create new conversation
        const newConversation = {
          id: Date.now(),
          title: `${repoName.split("/")[1]} - Analysis`,
          repository: repoName,
          url: githubUrl,
          messages: [],
        };

        setConversations((prev) => [newConversation, ...prev]);
        setActiveConversation(newConversation.id);
        setChatHistory([]);
        setShowPopup(false);
      } else {
        setIngestError(data.message || "Failed to ingest repository");
      }
    } catch (error) {
      console.error("Ingestion error:", error);
      setIngestError(error.message || "Failed to ingest repository");
    } finally {
      setIsIngesting(false);
    }
  };

  // Function to handle sending messages to RAG
  const handleSendMessage = async () => {
    if (!currentMessage.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: currentMessage,
      timestamp: new Date().toLocaleTimeString(),
    };

    const newChatHistory = [...chatHistory, userMessage];
    setChatHistory(newChatHistory);
    setCurrentMessage("");
    setIsTyping(true);

    try {
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: currentMessage }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get response");
      }

      const aiMessage = {
        id: Date.now() + 1,
        type: "ai",
        content: data.response,
        sources: data.sources || [],
        timestamp: new Date().toLocaleTimeString(),
      };

      const updatedHistory = [...newChatHistory, aiMessage];
      setChatHistory(updatedHistory);

      // Update conversation in the list
      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === activeConversation
            ? { ...conv, messages: updatedHistory }
            : conv
        )
      );
    } catch (error) {
      console.error("Query error:", error);
      const errorMessage = {
        id: Date.now() + 1,
        type: "ai",
        content: `Sorry, I encountered an error: ${error.message}`,
        sources: [],
        timestamp: new Date().toLocaleTimeString(),
        isError: true,
      };

      const updatedHistory = [...newChatHistory, errorMessage];
      setChatHistory(updatedHistory);

      setConversations((prev) =>
        prev.map((conv) =>
          conv.id === activeConversation
            ? { ...conv, messages: updatedHistory }
            : conv
        )
      );
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex">
      {showPopup && (
        <Mingest
          githubUrl={githubUrl}
          setGithubUrl={setGithubUrl}
          isIngesting={isIngesting}
          ingestError={ingestError}
          handleIngest={handleIngest}
          onClose={() => setShowPopup(false)}
        />
      )}
      <Mside
        conversations={conversations}
        activeConversation={activeConversation}
        selectConversation={(id) => {
          const conversation = conversations.find((conv) => conv.id === id);
          if (conversation) {
            setActiveConversation(id);
            setChatHistory(conversation.messages);
            setRepositoryName(conversation.repository);
          }
        }}
        deleteConversation={(id) => {
          setConversations((prev) => prev.filter((conv) => conv.id !== id));
          if (activeConversation === id) {
            setActiveConversation(null);
            setChatHistory([]);
          }
        }}
        startNewChat={() => {
          setShowPopup(true);
          setGithubUrl("");
          setIngestError("");
          setActiveConversation(null);
          setChatHistory([]);
        }}
      />
      <MChat
        activeConversation={activeConversation}
        repositoryName={repositoryName}
        chatHistory={chatHistory}
        currentMessage={currentMessage}
        setCurrentMessage={setCurrentMessage}
        handleSendMessage={handleSendMessage}
        isTyping={isTyping}
      />
    </div>
  );
};

export default Main;
