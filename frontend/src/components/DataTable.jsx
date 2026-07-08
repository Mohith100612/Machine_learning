export default function DataTable({ columns, rows, highlightCol }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="text-sm text-slate-400 py-6 text-center">
        No sample rows available.
      </div>
    );
  }

  return (
    <div className="overflow-auto max-h-80 rounded-xl border border-white/5">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th
                key={col}
                className={col === highlightCol ? "text-signal" : ""}
              >
                {col.replaceAll("_", " ")}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {columns.map((col) => (
                <td
                  key={col}
                  className={col === highlightCol ? "text-signal font-semibold" : ""}
                >
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
