import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getModels } from "../api.js";

const SUPERVISED = [
  {
    id: "linear-regression",
    path: "/linear-regression",
    number: "01",
    title: "Linear Regression",
    useCase: "Stock Price Prediction",
    desc: "Fits a straight-line relationship between market signals and next-day closing price.",
    task: "regression",
  },
  {
    id: "logistic-regression",
    path: "/logistic-regression",
    number: "02",
    title: "Logistic Regression",
    useCase: "Student Pass / Fail Prediction",
    desc: "Estimates the probability of passing from study habits and prior performance.",
    task: "classification",
  },
  {
    id: "decision-tree",
    path: "/decision-tree",
    number: "03",
    title: "Decision Tree",
    useCase: "Play Tennis Prediction",
    desc: "Splits weather conditions into simple yes/no rules to decide play or no play.",
    task: "classification",
  },
  {
    id: "random-forest",
    path: "/random-forest",
    number: "04",
    title: "Random Forest",
    useCase: "Fruit Classification",
    desc: "An ensemble of trees votes on fruit type from weight, size and color.",
    task: "classification",
  },
  {
    id: "gradient-boosting",
    path: "/gradient-boosting",
    number: "05",
    title: "Gradient Boosting",
    useCase: "House Price Prediction",
    desc: "Sequentially corrected trees combine to estimate market value from property features.",
    task: "regression",
  },
];

const UNSUPERVISED = [
  {
    id: "kmeans",
    path: "/kmeans",
    number: "06",
    title: "K-Means",
    useCase: "Customer Segmentation",
    desc: "Groups customers into segments by age, income and spending — no labels needed.",
    task: "clustering",
  },
  {
    id: "hierarchical-clustering",
    path: "/hierarchical-clustering",
    number: "07",
    title: "Hierarchical Clustering",
    useCase: "Country Development Grouping",
    desc: "Merges countries bottom-up into development tiers from socio-economic indicators.",
    task: "clustering",
  },
  {
    id: "pca",
    path: "/pca",
    number: "08",
    title: "PCA",
    useCase: "Wine Chemical Profile Compression",
    desc: "Compresses 6 chemical measurements into 2 components that keep most of the variance.",
    task: "dimensionality reduction",
  },
  {
    id: "dbscan",
    path: "/dbscan",
    number: "09",
    title: "DBSCAN",
    useCase: "Taxi Pickup Hotspot Detection",
    desc: "Finds dense pickup hotspots of any shape and flags isolated pickups as noise.",
    task: "clustering",
  },
  {
    id: "autoencoder",
    path: "/autoencoder",
    number: "10",
    title: "Autoencoder",
    useCase: "Machine Sensor Anomaly Detection",
    desc: "A neural net learns to reconstruct normal readings — what it can't rebuild is an anomaly.",
    task: "anomaly detection",
  },
];

function taskBadgeClass(task) {
  if (task === "regression") return "border-signal2/30 !text-signal2";
  if (task === "classification") return "border-signal/30 !text-signal";
  return "border-warn/30 !text-warn";
}

function ModuleCard({ m, metrics }) {
  return (
    <Link
      to={m.path}
      className="group panel p-6 relative overflow-hidden hover:border-signal/30 transition"
    >
      <div className="absolute -right-6 -top-6 font-display text-8xl font-bold text-white/[0.03] group-hover:text-signal/[0.06] transition select-none">
        {m.number}
      </div>
      <div className="relative">
        <div className="flex items-center gap-2 mb-3">
          <span className="mono-tag">module {m.number}</span>
          <span
            className={`mono-tag !text-[10px] px-2 py-0.5 rounded-full border ${taskBadgeClass(
              m.task
            )}`}
          >
            {m.task}
          </span>
        </div>
        <h3 className="font-display text-xl font-semibold text-slate-50 group-hover:text-signal transition">
          {m.title}
        </h3>
        <p className="text-sm text-slate-500 mb-3">{m.useCase}</p>
        <p className="text-sm text-slate-400 leading-relaxed">{m.desc}</p>

        <div className="mt-5 flex items-center justify-between">
          <span className="text-signal text-sm font-medium flex items-center gap-1.5 group-hover:gap-2.5 transition-all">
            Open module →
          </span>
          {metrics && (
            <span className="mono-tag !text-slate-500">
              {Object.entries(metrics)
                .slice(0, 2)
                .map(([k, v]) => `${k}: ${v}`)
                .join(" · ")}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

export default function Home() {
  const [metrics, setMetrics] = useState({});
  const [apiDown, setApiDown] = useState(false);

  useEffect(() => {
    getModels()
      .then((list) => {
        const map = {};
        list.forEach((m) => (map[m.id] = m.metrics));
        setMetrics(map);
      })
      .catch(() => setApiDown(true));
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 py-14">
      <div className="mb-14 max-w-2xl">
        <p className="mono-tag mb-3">10 trained models · live inference</p>
        <h1 className="font-display text-4xl md:text-5xl font-bold text-slate-50 leading-tight">
          Machine Learning, <span className="text-signal">signal by signal.</span>
        </h1>
        <p className="text-slate-400 mt-4 leading-relaxed">
          Five supervised and five unsupervised algorithms, each with its own
          dataset. Pick a module to inspect the training data, enter your own
          values, and run a live prediction against a model trained just now on
          the backend.
        </p>
        {apiDown && (
          <p className="mt-4 text-sm text-danger bg-danger/10 border border-danger/30 rounded-lg px-3 py-2 inline-block">
            Backend not reachable — start the Flask API on port 5000 to see live metrics.
          </p>
        )}
      </div>

      <div className="flex items-center gap-3 mb-6">
        <h2 className="font-display text-2xl font-semibold text-slate-50">
          Supervised Learning
        </h2>
        <span className="mono-tag !text-slate-500">learns from labelled examples</span>
      </div>
      <div className="grid md:grid-cols-2 gap-5 mb-14">
        {SUPERVISED.map((m) => (
          <ModuleCard key={m.id} m={m} metrics={metrics[m.id]} />
        ))}
      </div>

      <div className="flex items-center gap-3 mb-6">
        <h2 className="font-display text-2xl font-semibold text-slate-50">
          Unsupervised Learning
        </h2>
        <span className="mono-tag !text-slate-500">finds structure without labels</span>
      </div>
      <div className="grid md:grid-cols-2 gap-5">
        {UNSUPERVISED.map((m) => (
          <ModuleCard key={m.id} m={m} metrics={metrics[m.id]} />
        ))}
      </div>
    </div>
  );
}
