import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "pickup_x_km", label: "Pickup location X", unit: "km", step: "0.01", min: 0, max: 10 },
  { name: "pickup_y_km", label: "Pickup location Y", unit: "km", step: "0.01", min: 0, max: 10 },
];

const defaultValues = {
  pickup_x_km: 2.2,
  pickup_y_km: 3.1,
};

export default function DBSCANPage() {
  return (
    <ModelPageLayout
      modelId="dbscan"
      moduleNumber="09"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
