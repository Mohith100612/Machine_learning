import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "alcohol", label: "Alcohol", unit: "% vol", step: "0.01", min: 8, max: 16 },
  { name: "malic_acid", label: "Malic acid", unit: "g/L", step: "0.01", min: 0 },
  { name: "flavanoids", label: "Flavanoids", unit: "g/L", step: "0.01", min: 0 },
  { name: "color_intensity", label: "Color intensity", step: "0.01", min: 0 },
  { name: "hue", label: "Hue", step: "0.01", min: 0 },
  { name: "proline", label: "Proline", unit: "mg/L", step: "1", min: 0 },
];

const defaultValues = {
  alcohol: 13.2,
  malic_acid: 2.1,
  flavanoids: 2.4,
  color_intensity: 4.8,
  hue: 0.98,
  proline: 850,
};

export default function PCAPage() {
  return (
    <ModelPageLayout
      modelId="pca"
      moduleNumber="08"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
