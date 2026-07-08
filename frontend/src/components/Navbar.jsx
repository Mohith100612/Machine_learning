import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();
  const onHome = pathname === "/";

  return (
    <header className="sticky top-0 z-30 backdrop-blur bg-ink/80 border-b border-white/5">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <span className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-signal/10 border border-signal/30">
            <span className="h-2.5 w-2.5 rounded-full bg-signal shadow-[0_0_12px_2px_rgba(61,226,196,0.7)] group-hover:scale-110 transition" />
          </span>
          <div className="leading-tight">
            <p className="font-display font-semibold text-slate-50 tracking-tight">
              Signal Lab
            </p>
            <p className="mono-tag !text-slate-500">supervised learning console</p>
          </div>
        </Link>
        {!onHome && (
          <Link
            to="/"
            className="mono-tag !text-slate-400 hover:!text-signal transition flex items-center gap-2"
          >
            ← all modules
          </Link>
        )}
      </div>
    </header>
  );
}
