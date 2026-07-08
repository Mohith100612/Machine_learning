import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "temperature_c", label: "Temperature", unit: "°C", step: "0.1" },
  { name: "vibration_mm_s", label: "Vibration", unit: "mm/s", step: "0.01", min: 0 },
  { name: "pressure_kpa", label: "Pressure", unit: "kPa", step: "0.1", min: 0 },
  { name: "rpm", label: "Rotation speed", unit: "rpm", step: "1", min: 0 },
  { name: "voltage_v", label: "Voltage", unit: "V", step: "0.1", min: 0 },
];

const defaultValues = {
  temperature_c: 65.0,
  vibration_mm_s: 2.0,
  pressure_kpa: 101.0,
  rpm: 1500,
  voltage_v: 230.0,
};

export default function Autoencoder() {
  return (
    <ModelPageLayout
      modelId="autoencoder"
      moduleNumber="10"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
