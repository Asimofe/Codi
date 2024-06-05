import React, { useState, useEffect } from "react";
import Typing from "react-typing-effect";
import axios from "axios";
import "./App.css"; // import your css

const App = () => {
  const [messages, setMessages] = useState([]);
  const [currentTypingId, setCurrentTypingId] = useState(null);

  const handleSendMessage = async (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: message, isUser: true },
      {
        text: "Processing...",
        isUser: false,
        isTyping: true,
        id: Date.now(),
      },
    ]);

    try {
      const response = await axios.post("http://localhost:8001/generate", {
        code: message,
      });

      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.isTyping ? { ...msg, text: response.data.generated_code, isTyping: false } : msg
        )
      );
    } catch (error) {
      console.error("Error generating code:", error);
      setMessages((prevMessages) =>
        prevMessages.map((msg) =>
          msg.isTyping ? { ...msg, text: "Error processing request", isTyping: false } : msg
        )
      );
    }
  };

  const handleEndTyping = (id) => {
    setMessages((prevMessages) =>
      prevMessages.map((msg) =>
        msg.id === id ? { ...msg, isTyping: false } : msg
      )
    );
    setCurrentTypingId(null);
  };

  useEffect(() => {
    if (currentTypingId === null) {
      const nextTypingMessage = messages.find(
        (msg) => !msg.isUser && msg.isTyping
      );
      if (nextTypingMessage) {
        setCurrentTypingId(nextTypingMessage.id);
      }
    }
  }, [messages, currentTypingId]);

  return (
    <div className="app">
      <div className="chat-box">
        <h1>Codi</h1>
        <MessageList
          messages={messages || []}  // Ensure messages is an array
          currentTypingId={currentTypingId}
          onEndTyping={handleEndTyping}
        />
        <MessageForm onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};

const MessageList = ({ messages, currentTypingId, onEndTyping }) => (
  <div className="messages-list">
    {messages && messages.length > 0 ? (
      messages.map((message, index) => (
        <Message
          key={index}
          {...message}
          onEndTyping={onEndTyping}
          currentTypingId={currentTypingId}
        />
      ))
    ) : (
      <p>No messages</p>
    )}
  </div>
);


const Message = ({
  text,
  isUser,
  isTyping,
  id,
  onEndTyping,
  currentTypingId
}) => {
  return (
    <div className={isUser ? "user-message" : "ai-message"}>
      {isTyping && currentTypingId === id ? (
        <Typing speed={50} onFinishedTyping={() => onEndTyping(id)}>
          <pre>
            <code>
              <b>AI</b>: {text}
            </code>
          </pre>
        </Typing>
      ) : (
        <pre>
          <code>
            <b>{isUser ? "User" : "AI"}</b>: {text}
          </code>
        </pre>
      )}
    </div>
  );
};

const MessageForm = ({ onSendMessage }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onSendMessage(message);
    setMessage("");
  };

  return (
    <form onSubmit={handleSubmit} className="message-form">
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        className="message-input"
        placeholder="Type your code here..."
      />
      <button type="submit" className="send-button">
        Send
      </button>
    </form>
  );
};

export default App;
