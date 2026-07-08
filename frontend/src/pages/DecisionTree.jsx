import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "outlook", label: "Outlook", type: "select", options: ["Sunny", "Overcast", "Rain"] },
  { name: "temperature", label: "Temperature", type: "select", options: ["Hot", "Mild", "Cool"] },
  { name: "humidity", label: "Humidity", type: "select", options: ["High", "Normal"] },
  { name: "wind", label: "Wind", type: "select", options: ["Weak", "Strong"] },
];

const defaultValues = {
  outlook: "Sunny",
  temperature: "Mild",
  humidity: "Normal",
  wind: "Weak",
};

export default function DecisionTree() {
  return (
    <ModelPageLayout
      modelId="decision-tree"
      moduleNumber="03"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
