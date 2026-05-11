"use client";
import { useState } from "react";
import ImageUploader from "@/components/ImageUploader";
import DiagnosisCard from "@/components/DiagnosisCard";
import ChatBox from "@/components/ChatBox";
import { PredictionResult } from "@/lib/types";

export default function HomePage() {
  const [result, setResult] = useState<PredictionResult | null>(null);

  return (
    <main style={{ fontFamily: "sans-serif", maxWidth: 560, margin: "0 auto", padding: 32 }}>
      <h1 style={{ color: "#2e7d32" }}>🌿 PlantBot</h1>
      <p style={{ color: "#555" }}>Upload a leaf photo to detect plant diseases instantly.</p>

      <ImageUploader onResult={setResult} />

      {result && (
        <div style={{ marginTop: 32, display: "flex", flexDirection: "column", gap: 24 }}>
          <DiagnosisCard result={result} />
          <ChatBox
            initialMessage={
              result.status === "Healthy"
                ? `Your ${result.label} plant looks healthy! 🎉 How can I help you?`
                : `I detected **${result.label}** with ${result.confidence.toFixed(1)}% confidence. Would you like treatment and prevention advice?`
            }
          />
        </div>
      )}
    </main>
  );
}
