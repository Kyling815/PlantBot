"use client";
import ChatBox from "@/components/ChatBox";

export default function ChatPage() {
  return (
    <main style={{ fontFamily: "sans-serif", maxWidth: 560, margin: "0 auto", padding: 32 }}>
      <h1 style={{ color: "#2e7d32" }}>💬 Chat with PlantBot</h1>
      <p style={{ color: "#555" }}>Ask PlantBot anything about plant diseases, treatments, or prevention.</p>
      <ChatBox initialMessage="Hello! I'm PlantBot 🌿 How can I help you today?" />
    </main>
  );
}
