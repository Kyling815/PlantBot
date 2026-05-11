"use client";
import { useState } from "react";
import { sendChatMessage } from "@/lib/api";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "bot";
  text: string;
}

interface Props {
  initialMessage?: string;
}

export default function ChatBox({ initialMessage }: Props) {
  const [messages, setMessages] = useState<Message[]>(
    initialMessage ? [{ role: "bot", text: initialMessage }] : []
  );
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    const newMessages: Message[] = [...messages, { role: "user", text: userMessage }];
    setMessages(newMessages);

    try {
      const response = await sendChatMessage(
        userMessage,
        messages.map((m) => ({ role: m.role, text: m.text }))
      );
      
      if (response.success) {
        setMessages([...newMessages, { role: "bot", text: response.reply }]);
      } else {
        setMessages([...newMessages, { role: "bot", text: response.reply || "Error connecting to LLM." }]);
      }
    } catch (error) {
      setMessages([...newMessages, { role: "bot", text: "Network error trying to reach PlantBot." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 12,
        display: "flex",
        flexDirection: "column",
        maxWidth: 480,
        height: 400,
        overflow: "hidden",
      }}
    >
      <div style={{ flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 8 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              alignSelf: m.role === "user" ? "flex-end" : "flex-start",
              background: m.role === "user" ? "#4caf50" : "#f5f5f5",
              color: m.role === "user" ? "#fff" : "#333",
              padding: "8px 14px",
              borderRadius: 16,
              maxWidth: "80%",
              fontSize: 14,
            }}
          >
            <ReactMarkdown
              components={{
                p: ({ node, ...props }) => <p style={{ margin: "4px 0" }} {...props} />,
                ul: ({ node, ...props }) => <ul style={{ margin: "4px 0", paddingLeft: "20px" }} {...props} />,
                ol: ({ node, ...props }) => <ol style={{ margin: "4px 0", paddingLeft: "20px" }} {...props} />,
              }}
            >
              {m.text}
            </ReactMarkdown>
          </div>
        ))}
      </div>
      <div style={{ borderTop: "1px solid #eee", padding: "8px 12px", display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask PlantBot..."
          style={{ flex: 1, border: "none", outline: "none", fontSize: 14 }}
        />
        <button onClick={sendMessage} style={{ background: "#4caf50", color: "#fff", border: "none", borderRadius: 8, padding: "6px 16px", cursor: "pointer" }}>
          Send
        </button>
      </div>
    </div>
  );
}
