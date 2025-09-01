import React, { useState } from 'react';
import '../styles/ChatInput.css';

export default function ChatInput({ onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    onSend(input);
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <div className="input-group chat-input-group">
        <input
          type="text"
          className="form-control chat-input-field"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="btn btn-primary chat-input-button" type="submit">
          Send
        </button>
      </div>
    </form>
  );
}
