import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "weight_g", label: "Weight", unit: "g", step: "0.1", min: 0 },
  { name: "diameter_cm", label: "Diameter", unit: "cm", step: "0.1", min: 0 },
  { name: "red", label: "Red channel", unit: "0-255", step: "1", min: 0, max: 255 },
  { name: "green", label: "Green channel", unit: "0-255", step: "1", min: 0, max: 255 },
  { name: "blue", label: "Blue channel", unit: "0-255", step: "1", min: 0, max: 255 },
];

const defaultValues = {
  weight_g: 150,
  diameter_cm: 7.5,
  red: 190,
  green: 40,
  blue: 40,
};

export default function RandomForest() {
  return (
    <ModelPageLayout
      modelId="random-forest"
      moduleNumber="04"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
