import React, { useState, ChangeEvent, KeyboardEvent } from 'react';
import './App.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState<string>('');

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async (): Promise<void> => {
    if (!userInput.trim()) return;

    // Show user message immediately
    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);
    setUserInput('');

    try {
      const response = await fetch('http://localhost:8000/', {
        // add trailing slash to match FastAPI route
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json() as { response?: string };
      console.log('Server Response:', data);

      // Add bot reply to chat
      const botMessage = data.response
        ? { sender: 'bot', text: data.response }
        : { sender: 'bot', text: 'Sorry, something went wrong.' };

      setMessages([...newMessages, botMessage]);
      setUserInput('');
    } catch (error) {
      console.error('Upload failed:', error);
      setMessages([
        ...newMessages,
        { sender: 'bot', text: 'Error connecting to the server.' },
      ]);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSendMessage();
  };

  return (
    <>
      <h1 id='title'>Chat with bainiAi</h1>
      <div className="chatbot-container">
        <div className="chatbot-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className="chatbot-input-area">
          <input
            type="text"
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </>
  );
}

export default App;
