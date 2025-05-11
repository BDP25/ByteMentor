import logo from "../assets/logo.png";

// Das Chat Feld
import { Message } from "../types/messages";
import ChatMessage from "./ChatMessage";

interface ChatWindowProps {
  messages: Message[];
}

const ChatWindow: React.FC<ChatWindowProps> = ({ messages }) => {
  const showIntro = messages.length === 1;
  
  return (
    <div
      className="chat-window"
      style={{
        border: "1px solid rgb(238, 191, 133)",
        padding: "10px 25px",
        height: "800px",
        overflow: "scroll",
        background: "rgb(255, 255, 255)",
        borderRadius: "10px",
      }}
    >
      {showIntro ? (
        <div className="intro-logo">
          <img src={logo} alt="ByteMentor Logo" />
          <p>Welcome to <strong>ByteMentor</strong> – your Data Science guide!</p>
        </div>
      ) : (
        messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))
      )}
    </div>
  );
};

export default ChatWindow;

