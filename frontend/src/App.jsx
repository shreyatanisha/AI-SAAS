import { useEffect, useState } from "react";
import ChatPanel from "./components/ChatPanel.jsx";
import WebsitePanel from "./components/WebsitePanel.jsx";
import DocumentPanel from "./components/DocumentPanel.jsx";
import { checkHealth } from "./api.js";

const TABS = [
  { id: "chat", label: "Chat", icon: "💬" },
  { id: "website", label: "Website", icon: "🌐" },
  { id: "document", label: "Documents", icon: "📄" },
];

function App() {
  const [tab, setTab] = useState("chat");
  const [online, setOnline] = useState(null); // null = checking

  useEffect(() => {
    checkHealth()
      .then(() => setOnline(true))
      .catch(() => setOnline(false));
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <span className="logo">◆</span>
          <h1>Knowledge Assistant</h1>
        </div>
        <span className={`status ${online === null ? "" : online ? "up" : "down"}`}>
          {online === null ? "Checking…" : online ? "API online" : "API offline"}
        </span>
      </header>

      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`tab ${tab === t.id ? "active" : ""}`}
            onClick={() => setTab(t.id)}
          >
            {t.icon} {t.label}
          </button>
        ))}
      </nav> 

      <main className="content">
        {tab === "chat" && <ChatPanel />}
        {tab === "website" && <WebsitePanel />}
        {tab === "document" && <DocumentPanel />}
      </main> 
    </div>
  );
}

export default App;
