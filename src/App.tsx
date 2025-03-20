import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import ChatHistory from "./components/ChatHistory";
import { useChat } from "./hooks/useChat";
import { useState } from "react";
import { ChatSession } from "./components/ChatHistory";
import "./static/css/App.css";

function App() {
  const {
    messages,
    inputValue,
    handleSend,
    handleInputChange,
    handleKeyDown,
    resetChat,
    setMessages,
  } = useChat();
  const [chatHistory, setChatHistory] = useState<ChatSession[]>([]);
  const [chatIdCounter, setChatIdCounter] = useState<number>(1);

  const handleSaveChat = () => {
    const title = messages.length > 0 ? messages[0].text : "Neuer Chat";
    const newChat: ChatSession = {
      id: chatIdCounter,
      title: title,
      messages: messages,
    };
    setChatHistory([...chatHistory, newChat]);
    setChatIdCounter(chatIdCounter + 1);
    resetChat();
  };

  const handleSelectChat = (chat: ChatSession) => {
    console.log("Ausgewählter Chat:", chat);
    setMessages(chat.messages);
  };

  return (
    <div className="app-container">
      <div className="chat-history-container">
        <h1>ByteMentor</h1>
        <ChatHistory chats={chatHistory} onSelectChat={handleSelectChat} />
      </div>
      <div className="active-chat-container">
        <ChatWindow messages={messages} />
        <ChatInput
          value={inputValue}
          onChange={handleInputChange}
          onSend={handleSend}
          onKeyDown={handleKeyDown}
        />
        <div className="button-group">
          <button className="save-chat-button" onClick={handleSaveChat}>
            Chat Speichern
          </button>
          <button className="reset-chat-button" onClick={resetChat}>
            Chat Reset
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
