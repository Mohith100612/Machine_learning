import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "age", label: "Age", unit: "years", step: "1", min: 18, max: 75 },
  { name: "annual_income_k", label: "Annual income", unit: "k$", step: "0.1", min: 0 },
  { name: "spending_score", label: "Spending score", unit: "1-100", step: "1", min: 1, max: 100 },
];

const defaultValues = {
  age: 28,
  annual_income_k: 42,
  spending_score: 76,
};

export default function KMeans() {
  return (
    <ModelPageLayout
      modelId="kmeans"
      moduleNumber="06"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
