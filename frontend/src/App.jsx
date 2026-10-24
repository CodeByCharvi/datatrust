import { useState } from "react";
import ResultChart from "./ResultChart";

import UploadBox from "./UploadBox";

const API_URL = "http://127.0.0.1:8000/api/ask";

export default function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleAsk(e) {
    e.preventDefault();
    if (question.trim().length < 3) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      setResult(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", padding: 16, textAlign: "left" }}>
      <h1>DataTrust</h1>
      <p>Ask a question about your sales data in plain English.</p>
            <UploadBox />

      <form onSubmit={handleAsk} style={{ display: "flex", gap: 8 }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Total revenue by category"
          style={{ flex: 1, padding: 10, fontSize: 16 }}
        />
        <button type="submit" disabled={loading} style={{ padding: "10px 16px" }}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {error && <p style={{ color: "crimson" }}>Error: {error}</p>}

      {result && (
        <div style={{ marginTop: 24 }}>
          <p>
            <b>Status:</b> {result.status}
                      {result.sources && result.sources.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <b>Sources used:</b>
              {result.sources.map((s, i) => (
                <blockquote
                  key={i}
                  style={{ background: "#f4f4f4", margin: "8px 0", padding: 10, whiteSpace: "pre-wrap" }}
                >
                  <small>
                    {s.source} (match {s.score})
                  </small>
                  <br />
                  {s.text}
                </blockquote>
              ))}
            </div>
          )}
            {result.cache?.hit && " (answered from cache)"}
          </p>
          {result.answer && <p style={{ fontSize: 18 }}>{result.answer}</p>}
          {result.message && <p>{result.message}</p>}
          {result.sql && (
            <pre style={{ background: "#f4f4f4", padding: 12, overflowX: "auto" }}>
              {result.sql}
            </pre>
          )}

          <ResultChart chart={result.chart} columns={result.columns} rows={result.rows} />
          
          


          {result.rows && (
            <table border="1" cellPadding="6" style={{ borderCollapse: "collapse" }}>
              <thead>
                <tr>{result.columns.map((c) => <th key={c}>{c}</th>)}</tr>
              </thead>
              <tbody>
                {result.rows.map((row, i) => (
                  <tr key={i}>{row.map((v, j) => <td key={j}>{String(v)}</td>)}</tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}