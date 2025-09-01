import React, { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import '../styles/ChatWindow.css';
import '../styles/Markdown.css';

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (question) => {
    setMessages(prev => [...prev, { sender: "user", text: question }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/process-question`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { sender: "bot", text: data.answer || "No answer received." },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: "Error: could not reach server." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            <div className="markdown-body">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  a: ({node, ...props}) => <a {...props} target="_blank" rel="noopener noreferrer" />
                }}
              >
                {msg.text}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-message bot">
            <div className="markdown-body">Typing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSend={handleSend} />
    </div>
  );
}
