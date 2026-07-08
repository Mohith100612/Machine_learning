import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "prev_close", label: "Previous close", unit: "$", step: "0.01" },
  { name: "open", label: "Open price", unit: "$", step: "0.01" },
  { name: "high", label: "Day high", unit: "$", step: "0.01" },
  { name: "low", label: "Day low", unit: "$", step: "0.01" },
  { name: "volume", label: "Volume", unit: "shares", step: "1" },
];

const defaultValues = {
  prev_close: 101.25,
  open: 101.8,
  high: 103.4,
  low: 100.6,
  volume: 245000,
};

export default function GradientBoosting() {
  return (
    <ModelPageLayout
      modelId="gradient-boosting"
      moduleNumber="05"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
