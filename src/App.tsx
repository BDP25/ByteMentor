import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import ChatHistory from "./components/ChatHistory";
import { useChat } from "./hooks/useChat";
import { useState, useEffect } from "react";
import { ChatSession } from "./components/ChatHistory";
import { Message } from "./types/messages";
import "./static/css/App.css";
import ChatMessage from "./components/ChatMessage";

const STORAGE_KEY = "chatHistory";

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

  useEffect(() => {
    const storedChats = localStorage.getItem(STORAGE_KEY);
    if (storedChats) {
      const parsedChats: ChatSession[] = JSON.parse(storedChats);
      setChatHistory(parsedChats);
      const maxId = parsedChats.reduce((max, chat) => Math.max(max, chat.id), 0);
      setChatIdCounter(maxId + 1);

      const lastChatId = localStorage.getItem("lastChatId");
      if (lastChatId) {
        const lastChat = parsedChats.find(chat => chat.id === Number(lastChatId));
        if (lastChat) {
          setMessages(lastChat.messages);
        }
      }
    } else {
      const defaultChat: ChatSession = {
        id: 1,
        title: "Welcome",
        messages: [],
    };
    setChatHistory([defaultChat]);
    setMessages(defaultChat.messages);
    setChatIdCounter(2); 
    localStorage.setItem(STORAGE_KEY, JSON.stringify([defaultChat]));
    localStorage.setItem("lastChatId", "1");
    localStorage.setItem("chat_id_counter", "2");
  }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chatHistory));
  }, [chatHistory]);

  useEffect(() => {
    const storedCounter = localStorage.getItem("chat_id_counter");
    if (storedCounter) {
      setChatIdCounter(Number(storedCounter));
    }
  }, []);
  
  useEffect(() => {
    localStorage.setItem("chat_id_counter", String(chatIdCounter));
  }, [chatIdCounter]);  

  const handleSaveChat = () => {
    const title = messages.length > 0 ? messages[0].text : "New Chat";
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
    localStorage.setItem("chatMessages", JSON.stringify(chat.messages));
    localStorage.setItem("lastChatId", String(chat.id));
  };

  return (
    <div className="app-container">
      <div className="chat-history-container">
        <div className="header-title">
          <h1>ByteMentor</h1>
        </div>
        <ChatHistory chats={chatHistory} onSelectChat={handleSelectChat} />
      </div>
      <div className="active-chat-container">
        <ChatWindow messages={messages.length > 0 ? messages : [{ text: "Welcome", sender: "bot" }]} />
        <ChatInput
          value={inputValue}
          onChange={handleInputChange}
          onSend={handleSend}
          onKeyDown={handleKeyDown}
        />
        <div className="button-group">
          <button className="save-chat-button" onClick={handleSaveChat}>
            Save Chat
          </button>
          <button className="reset-chat-button" onClick={resetChat}>
            Reset Chat
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
