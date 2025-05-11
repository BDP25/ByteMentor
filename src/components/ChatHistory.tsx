import { Message } from "../types/messages";
import "../static/css/chathistory.css";

export interface ChatSession {
  id: number;
  title: string;
  messages: Message[];
}

interface ChatHistoryProps {
  chats: ChatSession[];
  onSelectChat: (chat: ChatSession) => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ chats, onSelectChat }) => {
  return (
    <div className="chat-history">
      <h3>Chat History</h3>
      <ul className="chat-history-list">
        {chats.map((chat) => (
          <li
            key={chat.id}
            className="chat-history-item"
            onClick={() => onSelectChat(chat)}
          >
            {chat.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatHistory;
