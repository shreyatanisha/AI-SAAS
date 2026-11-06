// All backend calls live here. "/api" is proxied to FastAPI by vite.config.js.
// For production, set VITE_API_URL (e.g. https://my-api.com) and enable CORS on FastAPI.
const BASE = import.meta.env.VITE_API_URL || "/api";

async function handle(response) {
  let data = null;
  try {
    data = await response.json();
  } catch {
    // non-JSON body
  }
  if (!response.ok) {
    // FastAPI errors look like { detail: "..." } or { detail: [{msg: "..."}] }
    let message = `Request failed (${response.status})`;
    if (typeof data?.detail === "string") message = data.detail;
    else if (Array.isArray(data?.detail)) message = data.detail.map((d) => d.msg).join(", ");
    throw new Error(message);
  }
  return data;
}

export async function checkHealth() {
  return handle(await fetch(`${BASE}/`));
}

export async function sendChat(question) {
  return handle(
    await fetch(`${BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    })
  );
}

export async function ingestWebsite(url, maxPages) {
  return handle(
    await fetch(`${BASE}/ingest-website`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, max_pages: maxPages }),
    })
  );
}

export async function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  return handle(await fetch(`${BASE}/upload-document`, { method: "POST", body: form }));
}
