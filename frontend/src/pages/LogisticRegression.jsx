import ModelPageLayout from "../components/ModelPageLayout.jsx";

const fields = [
  { name: "hours_studied", label: "Hours studied / week", unit: "hrs", step: "0.5", min: 0, max: 24 },
  { name: "attendance_percentage", label: "Attendance", unit: "%", step: "1", min: 0, max: 100 },
  { name: "previous_score", label: "Previous exam score", unit: "%", step: "1", min: 0, max: 100 },
];

const defaultValues = {
  hours_studied: 6,
  attendance_percentage: 85,
  previous_score: 70,
};

export default function LogisticRegression() {
  return (
    <ModelPageLayout
      modelId="logistic-regression"
      moduleNumber="02"
      fields={fields}
      defaultValues={defaultValues}
    />
  );
}
