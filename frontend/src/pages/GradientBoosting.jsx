import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "area_sqft", label: "Area", unit: "sqft", step: "1", min: 0 },
  { name: "bedrooms", label: "Bedrooms", step: "1", min: 0, max: 10 },
  { name: "bathrooms", label: "Bathrooms", step: "1", min: 0, max: 10 },
  { name: "age_years", label: "Age of property", unit: "yrs", step: "1", min: 0 },
  { name: "location_score", label: "Location score", unit: "1-10", step: "0.1", min: 1, max: 10 },
];

const defaultValues = {
  area_sqft: 2000,
  bedrooms: 3,
  bathrooms: 2,
  age_years: 5,
  location_score: 7.5,
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
