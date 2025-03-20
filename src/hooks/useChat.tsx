import { useState } from "react";
import { Message } from "../types/messages";

// Input-Feld Logik
export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Wie kann ich dir behilflich sein?", sender: "bot" },
  ]);

  const [inputValue, setInputValue] = useState<string>("");

  const handleSend = () => {
    if (inputValue.trim() === "") return;

    // Nutzer Nachricht
    const newMessage: Message = { text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, newMessage]);

    // Bot Nachricht
    setTimeout(() => {
      const botResponse: Message = {
        text: `Antwort: ${inputValue}`,
        sender: "bot",
      };
      setMessages((prev) => [...prev, botResponse]);
    }, 1000);

    setInputValue("");
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const resetChat = () => {
    setMessages([{ text: "Wie kann ich dir behilflich sein?", sender: "bot" }]);
  };

  return {
    messages,
    inputValue,
    handleSend,
    handleInputChange,
    handleKeyDown,
    resetChat,
    setMessages,
  };
}
