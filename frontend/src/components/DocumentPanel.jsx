import { useRef, useState } from "react";
import { uploadDocument } from "../api.js";

const ALLOWED = [".pdf", ".txt"];

function DocumentPanel() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  function pickFile(f) {
    setError("");
    setResult(null);
    if (!f) return;
    const ext = f.name.slice(f.name.lastIndexOf(".")).toLowerCase();
    if (!ALLOWED.includes(ext)) {
      setFile(null);
      setError("Only PDF and TXT files are supported.");
      return;
    }
    setFile(f);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragging(false);
    pickFile(e.dataTransfer.files[0]);
  }

  async function handleUpload() {
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      setResult(await uploadDocument(file));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <div
        className={`dropzone ${dragging ? "dragging" : ""}`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt"
          hidden
          onChange={(e) => pickFile(e.target.files[0])}
        />
        <div className="drop-icon">⬆</div>
        {file ? (
          <p>
            <strong>{file.name}</strong>
            <br />
            <span className="muted">{(file.size / 1024).toFixed(1)} KB</span>
          </p>
        ) : (
          <p>
            <strong>Drag & drop</strong> a PDF or TXT file here, or click to browse
          </p>
        )}
      </div>

      <button className="btn" onClick={handleUpload} disabled={!file || loading}>
        {loading ? "Extracting…" : "Upload & extract text"}
      </button>

      {error && <p className="notice error">{error}</p>}

      {result && (
        <div className="results">
          <p className="notice success">{result.message}</p>
          <article className="card">
            <h3>{result.document.filename}</h3>
            <div className="card-footer">
              <span className="tag">{result.document.source_type.toUpperCase()}</span>
              <span className="tag">{result.document.content.length.toLocaleString()} chars</span>
            </div>
            <pre className="preview">{result.document.content}</pre>
          </article>
        </div>
      )}
    </section>
  );
}

export default DocumentPanel;
