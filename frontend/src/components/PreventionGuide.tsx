interface Props {
  tips: string;
}

export default function PreventionGuide({ tips }: Props) {
  if (!tips) return null;
  return (
    <div style={{ background: "#e8f5e9", borderRadius: 12, padding: 20, maxWidth: 480 }}>
      <h3 style={{ color: "#388e3c", marginTop: 0 }}>🛡️ Prevention Guide</h3>
      <pre style={{ whiteSpace: "pre-wrap", fontSize: 14, lineHeight: 1.6 }}>{tips}</pre>
    </div>
  );
}
