import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "gdp_per_capita_k", label: "GDP per capita", unit: "k$", step: "0.1", min: 0 },
  { name: "life_expectancy", label: "Life expectancy", unit: "years", step: "0.1", min: 40, max: 95 },
  { name: "internet_users_pct", label: "Internet users", unit: "%", step: "0.1", min: 0, max: 100 },
  { name: "urban_pop_pct", label: "Urban population", unit: "%", step: "0.1", min: 0, max: 100 },
];

const defaultValues = {
  gdp_per_capita_k: 18,
  life_expectancy: 74,
  internet_users_pct: 68,
  urban_pop_pct: 61,
};

export default function HierarchicalClustering() {
  return (
    <ModelPageLayout
      modelId="hierarchical-clustering"
      moduleNumber="07"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
