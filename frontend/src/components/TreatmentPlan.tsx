interface Props {
  plan: string;
}

export default function TreatmentPlan({ plan }: Props) {
  if (!plan) return null;
  return (
    <div style={{ background: "#fff8e1", borderRadius: 12, padding: 20, maxWidth: 480 }}>
      <h3 style={{ color: "#f57c00", marginTop: 0 }}>💊 Treatment Plan</h3>
      <pre style={{ whiteSpace: "pre-wrap", fontSize: 14, lineHeight: 1.6 }}>{plan}</pre>
    </div>
  );
}
