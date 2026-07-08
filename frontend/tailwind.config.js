/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B1220",
        panel: "#111A2C",
        panel2: "#16233A",
        edge: "#23355",
        signal: "#3DE2C4",
        signal2: "#7C9CFF",
        warn: "#FFB454",
        danger: "#FF6B6B",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(61,226,196,0.15), 0 8px 30px rgba(61,226,196,0.08)",
      },
    },
  },
  plugins: [],
};
