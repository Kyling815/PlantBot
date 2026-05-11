"use client";
import { predictDisease } from "@/lib/api";
import { PredictionResult } from "@/lib/types";
import { useState, useRef } from "react";

interface Props {
  onResult: (result: PredictionResult) => void;
}

export default function ImageUploader({ onResult }: Props) {
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    setError(null);
    setPreview(URL.createObjectURL(file));
    setLoading(true);
    try {
      const response = await predictDisease(file);
      if (response.success) {
        onResult(response.data);
      } else {
        setError(response.error ?? "Prediction failed");
      }
    } catch (e: any) {
      setError(e.message ?? "Network error");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onClick={() => inputRef.current?.click()}
      style={{
        border: "2px dashed #4caf50",
        borderRadius: 12,
        padding: 32,
        textAlign: "center",
        cursor: "pointer",
        background: preview ? "transparent" : "#f1f8e9",
        minHeight: 200,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 12,
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={handleChange}
      />
      {preview ? (
        <img src={preview} alt="Leaf preview" style={{ maxHeight: 240, borderRadius: 8 }} />
      ) : (
        <p style={{ color: "#555" }}>📷 Drop a leaf image here or click to upload</p>
      )}
      {loading && <p style={{ color: "#4caf50" }}>🔍 Analysing...</p>}
      {error && <p style={{ color: "red" }}>⚠️ {error}</p>}
    </div>
  );
}
