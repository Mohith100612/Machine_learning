import { useEffect, useState } from "react";
import DataTable from "./DataTable.jsx";
import ConfidenceGauge from "./ConfidenceGauge.jsx";
import { getSample, getInfo, predict } from "../api.js";

/**
 * fields: [{ name, label, type: 'number'|'select', options?, step, min, max, placeholder, unit }]
 */
function formatMetric(k, v) {
  if (typeof v !== "number") return v;
  if (k === "r2_score" || k === "accuracy") return (v * 100).toFixed(1) + "%";
  if (k.includes("variance")) return v.toFixed(1) + "%";
  if (k.includes("mae")) return v.toLocaleString();
  if (Number.isInteger(v)) return v.toLocaleString();
  return v.toFixed(2);
}

export default function ModelPageLayout({
  modelId,
  moduleNumber,
  fields,
  defaultValues,
  accent = "signal",
}) {
  const [sample, setSample] = useState(null);
  const [info, setInfo] = useState(null);
  const [form, setForm] = useState(defaultValues);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState(null);

  useEffect(() => {
    let mounted = true;
    Promise.all([getSample(modelId), getInfo(modelId)])
      .then(([s, i]) => {
        if (!mounted) return;
        setSample(s);
        setInfo(i);
      })
      .catch(() =>
        setLoadError(
          "Could not reach the backend API. Make sure the Flask server is running on port 5000."
        )
      );
    return () => (mounted = false);
  }, [modelId]);

  const handleChange = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const payload = {};
      fields.forEach((f) => {
        payload[f.name] =
          f.type === "select" ? form[f.name] : Number(form[f.name]);
      });
      const data = await predict(modelId, payload);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loadError) {
    return (
      <div className="max-w-2xl mx-auto mt-24 panel p-8 text-center">
        <p className="text-danger font-display font-semibold mb-2">
          Connection error
        </p>
        <p className="text-slate-400 text-sm">{loadError}</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4 mb-8">
        <div>
          <p className="mono-tag mb-2">Module {moduleNumber} / 10</p>
          <h1 className="font-display text-3xl font-bold text-slate-50">
            {info?.name || "…"}
          </h1>
          <p className="text-slate-400 mt-1">{info?.use_case}</p>
        </div>
        {info && (
          <div className="panel px-4 py-3 flex gap-6">
            {Object.entries(info.metrics).map(([k, v]) => (
              <div key={k} className="text-right">
                <p className="mono-tag !text-slate-500">{k.replaceAll("_", " ")}</p>
                <p className="font-display text-xl font-semibold text-signal">
                  {formatMetric(k, v)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="grid lg:grid-cols-5 gap-6">
        {/* Left: dataset + explanation */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          <section className="panel p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-display font-semibold text-slate-100">
                Sample dataset
              </h2>
              {sample && (
                <span className="mono-tag !text-slate-500">
                  {sample.total_rows} rows total · showing {sample.rows.length}
                </span>
              )}
            </div>
            {sample ? (
              <DataTable
                columns={sample.columns}
                rows={sample.rows}
                highlightCol={info?.target}
              />
            ) : (
              <TableSkeleton />
            )}
          </section>

          <section className="panel p-6">
            <h2 className="font-display font-semibold text-slate-100 mb-3">
              How this model works
            </h2>
            <p className="text-sm leading-relaxed text-slate-400">
              {info?.explanation || "Loading explanation…"}
            </p>
            {info?.features && (
              <div className="mt-4 flex flex-wrap gap-2">
                {info.features.map((f) => (
                  <span
                    key={f}
                    className="mono-tag !text-slate-300 bg-white/5 border border-white/10 rounded-full px-3 py-1"
                  >
                    {f.replaceAll("_", " ")}
                  </span>
                ))}
              </div>
            )}
          </section>
        </div>

        {/* Right: form + result */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <section className="panel p-6">
            <h2 className="font-display font-semibold text-slate-100 mb-4">
              Enter values
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              {fields.map((f) => (
                <div key={f.name}>
                  <label className="mono-tag !text-slate-400 block mb-1.5">
                    {f.label}
                    {f.unit ? ` (${f.unit})` : ""}
                  </label>
                  {f.type === "select" ? (
                    <select
                      className="field-input focus-ring"
                      value={form[f.name]}
                      onChange={(e) => handleChange(f.name, e.target.value)}
                    >
                      {f.options.map((opt) => (
                        <option key={opt} value={opt}>
                          {opt}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type="number"
                      step={f.step || "any"}
                      min={f.min}
                      max={f.max}
                      required
                      placeholder={f.placeholder}
                      className="field-input focus-ring"
                      value={form[f.name]}
                      onChange={(e) => handleChange(f.name, e.target.value)}
                    />
                  )}
                </div>
              ))}
              <button type="submit" disabled={loading} className="btn-primary mt-2">
                {loading ? "Predicting…" : "Predict"}
              </button>
              {error && (
                <p className="text-danger text-sm bg-danger/10 border border-danger/30 rounded-lg px-3 py-2">
                  {error}
                </p>
              )}
            </form>
          </section>

          {result && (
            <section className="panel-raised p-6 shadow-glow animate-[fadeIn_0.4s_ease]">
              <h2 className="font-display font-semibold text-slate-100 mb-4">
                Prediction result
              </h2>
              {result.task === "regression" ? (
                <div className="text-center py-4">
                  <p className="mono-tag mb-2">{info?.target?.replaceAll("_", " ")}</p>
                  <p className="font-display text-4xl font-bold text-signal">
                    {result.prediction.toLocaleString(undefined, {
                      maximumFractionDigits: 2,
                    })}
                  </p>
                  <p className="text-xs text-slate-500 mt-3">
                    Model R² on held-out test data: {(result.metrics.r2_score * 100).toFixed(1)}%
                  </p>
                </div>
              ) : result.task === "dimensionality-reduction" ? (
                <div className="py-2">
                  <p className="mono-tag mb-4 text-center">projected coordinates</p>
                  <div className="flex justify-center gap-10">
                    {Object.entries(result.projection).map(([pc, val]) => (
                      <div key={pc} className="text-center">
                        <p className="font-display text-3xl font-bold text-signal">
                          {val}
                        </p>
                        <p className="mono-tag mt-1">{pc}</p>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 flex flex-col gap-2">
                    {Object.entries(result.explained_variance).map(([pc, v]) => (
                      <div key={pc}>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-slate-400">
                            {pc} · variance explained
                          </span>
                          <span className="font-mono text-slate-300">{v}%</span>
                        </div>
                        <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                          <div
                            className="h-full rounded-full bg-signal"
                            style={{ width: `${v}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-center justify-center">
                    <ConfidenceGauge value={result.confidence} label="Confidence" />
                  </div>
                  <p className="text-center -mt-2 font-display text-2xl font-bold text-slate-50">
                    {result.prediction}
                  </p>
                  <div className="mt-4 flex flex-col gap-2">
                    {Object.entries(result.probabilities).map(([cls, p]) => (
                      <div key={cls}>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-slate-400">{cls}</span>
                          <span className="font-mono text-slate-300">{p}%</span>
                        </div>
                        <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                          <div
                            className="h-full rounded-full bg-signal"
                            style={{ width: `${p}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {result.note && (
                <p className="text-xs text-slate-500 mt-4 border-t border-white/5 pt-3 leading-relaxed">
                  {result.note}
                </p>
              )}
            </section>
          )}
        </div>
      </div>
    </div>
  );
}

function TableSkeleton() {
  return (
    <div className="animate-pulse space-y-2">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="h-6 bg-white/5 rounded" />
      ))}
    </div>
  );
}
