import { useState, useEffect } from "react";
import { Message } from "../types/messages";

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>("");

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
  }, [messages]);

  const handleSend = async () => {
    if (inputValue.trim() === "") return;

    try {
      // Text vor dem Anzeigen korrigieren
      const response = await fetch("http://localhost:5000/correct", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputValue }),
      });

      const data = await response.json();
      const correctedText = data.corrected;

      const correctedMessage: Message = {
        text: correctedText,
        sender: "user",
      };

      setMessages((prev) => [...prev, correctedMessage]);

      setTimeout(() => {
        const botMessage: Message = {
          text: `I understood: "${correctedText}"`,
          sender: "bot",
        };
        setMessages((prev) => [...prev, botMessage]);
      }, 1000);
    } catch (error) {
      // Falls der Server nicht erreichbar ist
      const fallbackMessage: Message = {
        text: inputValue,
        sender: "user",
      };
      const errorMsg: Message = {
        text: "Correction service not available.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, fallbackMessage, errorMsg]);
    }

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
    setMessages([]);
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
