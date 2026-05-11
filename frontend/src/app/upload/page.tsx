"use client";
import ImageUploader from "@/components/ImageUploader";
import DiagnosisCard from "@/components/DiagnosisCard";
import { useState } from "react";
import { PredictionResult } from "@/lib/types";

export default function UploadPage() {
  const [result, setResult] = useState<PredictionResult | null>(null);

  return (
    <main style={{ fontFamily: "sans-serif", maxWidth: 560, margin: "0 auto", padding: 32 }}>
      <h1 style={{ color: "#2e7d32" }}>📷 Upload Leaf Image</h1>
      <ImageUploader onResult={setResult} />
      {result && <div style={{ marginTop: 24 }}><DiagnosisCard result={result} /></div>}
    </main>
  );
}
