import { PredictionResult } from "@/lib/types";

interface Props {
  result: PredictionResult;
}

const severityColor: Record<string, string> = {
  healthy: "#4caf50",
  mild: "#ff9800",
  moderate: "#f44336",
  severe: "#b71c1c",
};

export default function DiagnosisCard({ result }: Props) {
  const isHealthy = result.status === "Healthy";
  const color = isHealthy ? "#4caf50" : "#f44336";

  return (
    <div
      style={{
        background: "#fff",
        borderRadius: 12,
        boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
        padding: 24,
        maxWidth: 480,
      }}
    >
      <h2 style={{ color, margin: 0 }}>
        {isHealthy ? "✅ Healthy Plant" : "🚨 Disease Detected"}
      </h2>
      <p style={{ fontSize: 18, fontWeight: 600, marginTop: 8 }}>{result.label}</p>
      <p style={{ color: "#666" }}>Confidence: {result.confidence.toFixed(1)}%</p>

      <div style={{ marginTop: 16 }}>
        <h4 style={{ marginBottom: 8 }}>Top Predictions</h4>
        {result.top5.map((p, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
            <span style={{ fontSize: 14 }}>{p.label}</span>
            <span style={{ fontSize: 14, color: "#888" }}>{p.confidence.toFixed(1)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
