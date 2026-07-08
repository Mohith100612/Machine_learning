import axios from "axios";

// In dev, Vite proxies /api -> http://localhost:5000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to your deployed backend URL.
const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export const getModels = () => client.get("/api/models").then((r) => r.data);

export const getSample = (modelId) =>
  client.get(`/api/${modelId}/sample`).then((r) => r.data);

export const getInfo = (modelId) =>
  client.get(`/api/${modelId}/info`).then((r) => r.data);

export const predict = (modelId, payload) =>
  client
    .post(`/api/${modelId}/predict`, payload)
    .then((r) => r.data)
    .catch((err) => {
      const msg = err.response?.data?.error || "Prediction failed. Check your inputs.";
      throw new Error(msg);
    });

export default client;
