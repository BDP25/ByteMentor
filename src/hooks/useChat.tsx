import { useState } from "react";
import { Message } from "../types/messages";

// Input-Feld Logik
export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hallo, wie geht es dir?", sender: "user" },
    { text: "Mir geht es gut, danke!", sender: "bot" },
    { text: "Was kann ich für dich tun?", sender: "bot" },
    { text: "Ich brauche Hilfe mit meinem Projekt", sender: "user" },
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

  return { messages, inputValue, handleSend,  handleInputChange, handleKeyDown}
}
