import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8001";

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 30_000,
});

/**
 * Upload a leaf image and receive a disease prediction.
 */
export async function predictDisease(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post("/api/predict", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function sendChatMessage(message: string, history: { role: string; text: string }[]) {
  const response = await api.post("/api/chat", { message, history });
  return response.data;
}
