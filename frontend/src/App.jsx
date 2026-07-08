import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import LinearRegression from "./pages/LinearRegression.jsx";
import LogisticRegression from "./pages/LogisticRegression.jsx";
import DecisionTree from "./pages/DecisionTree.jsx";
import RandomForest from "./pages/RandomForest.jsx";
import GradientBoosting from "./pages/GradientBoosting.jsx";

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/linear-regression" element={<LinearRegression />} />
        <Route path="/logistic-regression" element={<LogisticRegression />} />
        <Route path="/decision-tree" element={<DecisionTree />} />
        <Route path="/random-forest" element={<RandomForest />} />
        <Route path="/gradient-boosting" element={<GradientBoosting />} />
        <Route
          path="*"
          element={
            <div className="max-w-xl mx-auto mt-24 text-center panel p-10">
              <p className="font-display text-2xl font-semibold text-slate-50">
                404
              </p>
              <p className="text-slate-400 mt-2">
                This module doesn't exist. Head back to the dashboard.
              </p>
            </div>
          }
        />
      </Routes>
    </div>
  );
}
