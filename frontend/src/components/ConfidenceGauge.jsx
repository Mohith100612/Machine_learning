export default function ConfidenceGauge({ value = 0, label = "Confidence" }) {
  // value: 0-100
  const radius = 70;
  const stroke = 12;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const clamped = Math.max(0, Math.min(100, value));
  const offset = circumference - (clamped / 100) * circumference;

  const color =
    clamped >= 75 ? "#3DE2C4" : clamped >= 45 ? "#FFB454" : "#FF6B6B";

  return (
    <div className="flex flex-col items-center justify-center gap-1">
      <svg height={radius * 2} width={radius * 2} className="-rotate-90">
        <circle
          stroke="#1c2a42"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference + " " + circumference}
          style={{ strokeDashoffset: offset, transition: "stroke-dashoffset 0.6s ease" }}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <div className="-mt-24 flex flex-col items-center">
        <span className="font-display text-3xl font-bold text-slate-50">
          {clamped.toFixed(1)}%
        </span>
        <span className="mono-tag mt-1">{label}</span>
      </div>
      <div className="h-8" />
    </div>
  );
}
