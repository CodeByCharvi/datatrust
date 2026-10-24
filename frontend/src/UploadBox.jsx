import { useState } from "react";

const UPLOAD_URL = "http://127.0.0.1:8000/api/upload";

export default function UploadBox() {
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleFile(e) {
    const file = e.target.files[0];
    if (!file) return;
    setBusy(true);
    setMessage("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(UPLOAD_URL, { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || `Server returned ${res.status}`);
      setMessage(`Added ${data.filename} (${data.chunks_added} passages). You can now ask about it.`);
    } catch (err) {
      setMessage(`Upload failed: ${err.message}`);
    } finally {
      setBusy(false);
      e.target.value = "";
    }
  }

  return (
    <div style={{ margin: "16px 0", padding: 12, border: "1px dashed #999" }}>
      <b>Add a document</b> (.txt or .md, max 1 MB){" "}
      <input type="file" accept=".txt,.md" onChange={handleFile} disabled={busy} />
      {busy && <p>Uploading...</p>}
      {message && <p>{message}</p>}
    </div>
  );
}