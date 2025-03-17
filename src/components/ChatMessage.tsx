// Für die Nachrichten
import { Message } from "../types/messages";
import "../static/css/chatbox.css";

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const containerClass =
    message.sender === "user"
      ? "chat-message-container user"
      : "chat-message-container bot";

  return (
    <div className={containerClass}>
      <span className="chat-message-text">{message.text}</span>
    </div>
  );
};

export default ChatMessage;
