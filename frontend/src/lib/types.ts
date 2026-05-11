// PlantBot shared TypeScript types

export interface TopPrediction {
  label: string;
  confidence: number;
}

export interface PredictionResult {
  raw_label: string;
  label: string;
  confidence: number;
  status: "Healthy" | "Disease detected";
  top5: TopPrediction[];
}

export interface PredictionResponse {
  success: boolean;
  data: PredictionResult | null;
  error: string | null;
}

export interface DiagnosisState {
  prediction: PredictionResult;
  plant: string;
  disease: string;
  severity: "healthy" | "mild" | "moderate" | "severe";
  agentResponse: string | null;
}
