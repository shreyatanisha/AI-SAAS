import { useState } from "react";
import { ingestWebsite } from "../api.js";

function PageCard({ page }) {
  const [open, setOpen] = useState(false);
  const preview = page.content.slice(0, 280);

  return (
    <article className="card">
      <h3>{page.title}</h3>
      <a href={page.url} target="_blank" rel="noreferrer" className="link">
        {page.url}
      </a>
      <p className="muted">
        {open ? page.content : preview}
        {!open && page.content.length > 280 && "…"}
      </p>
      <div className="card-footer">
        <span className="tag">{page.content.length.toLocaleString()} chars</span>
        {page.content.length > 280 && (
          <button className="linkbtn" onClick={() => setOpen(!open)}>
            {open ? "Show less" : "Show full text"}
          </button>
        )}
      </div>
    </article>
  );
}

function WebsitePanel() {
  const [url, setUrl] = useState("");
  const [maxPages, setMaxPages] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      setResult(await ingestWebsite(url.trim(), Number(maxPages)));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <form className="form" onSubmit={handleSubmit}>
        <label>
          Website URL
          <input
            type="url"
            required
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </label>

        <label>
          Max pages: <strong>{maxPages}</strong>
          <input
            type="range"
            min="1"
            max="100"
            value={maxPages}
            onChange={(e) => setMaxPages(e.target.value)}
          />
        </label>

        <button className="btn" disabled={loading || !url}>
          {loading ? "Crawling…" : "Ingest website"}
        </button>
      </form>

      {loading && <p className="notice">Crawling pages, this can take a little while…</p>}
      {error && <p className="notice error">{error}</p>}

      {result && (
        <div className="results">
          <p className="notice success">
            {result.message} <strong>{result.total_pages}</strong> page(s) collected.
          </p>
          <div className="grid">
            {result.pages.map((p) => (
              <PageCard key={p.url} page={p} />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

export default WebsitePanel;
