import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import { useChat } from "./hooks/useChat";

function App() {
  const { messages, inputValue, handleSend, handleInputChange, handleKeyDown } =
    useChat();

  return (
    <div style={{ padding: "25px" }}>
      <h1>ByteMentor</h1>
      <ChatWindow messages={messages} />
      <ChatInput
        value={inputValue}
        onChange={handleInputChange}
        onSend={handleSend}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
}

export default App;
