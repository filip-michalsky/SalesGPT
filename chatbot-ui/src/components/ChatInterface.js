import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css'; // Import CSS for styling
import { v4 as uuidv4 } from 'uuid';
import maskot from '../assets/maskot.png';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(''); // Add state for sessionId

  // Generate a new sessionId when the component mounts
  useEffect(() => {
    setSessionId(uuidv4());
  }, []);

  const sendMessage = async () => {
    if (input.trim()) {
      const userMessage = { author: 'user', text: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput('');

      try {
        const response = await axios.post('http://localhost:8000/chat', {
          session_id: sessionId, // Include the sessionId in the request
          conversation_history: messages.filter(msg => msg.author === 'bot').map(msg => msg.text),
          human_say: input
        });
        const botMessage = { author: 'bot', text: response.data.say };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };
  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Chat with SalesGPT</h2>
      </div>
      <div className="chat-body">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.author}`}>
            {msg.author === 'user' ? 
              <span className="avatar">🧑</span> : 
              <img className="avatar" src={maskot} alt="maskot" />
            }
            <p className="text">{msg.text}</p>
          </div>
        ))}
      </div>
      <div className="chat-footer">
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
      <a href="https://github.com/yourusername/yourrepository" target="_blank" rel="noopener noreferrer" className="github-link">
          View on GitHub
        </a>
    </div>
  );
  
};


export default ChatInterface;