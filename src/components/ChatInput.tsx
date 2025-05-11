// Input Feld für den User
interface ChatInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSend: () => void;
  onKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChange,
  onSend,
  onKeyDown,
}) => {
  return (
    <div
      className="input-container"
      style={{ marginTop: "10px", display: "flex" }}
    >
      <input
        type="text"
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        style={{
          flex: 1,
          padding: "12px 20px",
          border: "2px solid #FFB366",
          borderRadius: "12px",
          fontSize: '18px',
          outline: "none",
        }}
        placeholder="Type what you want to know about Data Science..."
      />
      <button onClick={onSend} style={{ marginLeft: '15px', padding: '10px 25px', border: "1px solid rgb(238, 191, 133)", background: "rgb(238, 176, 100)", borderRadius: "10px", fontSize: '25px'}}>
        Send
      </button>
    </div>
  );
};

export default ChatInput;
