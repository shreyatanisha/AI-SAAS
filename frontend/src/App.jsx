import { useEffect, useState } from "react";
import ChatPanel from "./components/ChatPanel.jsx";
import WebsitePanel from "./components/WebsitePanel.jsx";
import DocumentPanel from "./components/DocumentPanel.jsx";
import { checkHealth, adminLogin } from "./api.js";

const ADMIN_TABS = [
  { id: "chat", label: "Chat", icon: "💬" },
  { id: "website", label: "Website", icon: "🌐" },
  { id: "document", label: "Documents", icon: "📄" },
];

function App() {
  const [tab, setTab] = useState("chat");
  const [online, setOnline] = useState(null);
  const [isAdmin, setIsAdmin] = useState(() => sessionStorage.getItem("isAdmin") === "true");
  const [showLogin, setShowLogin] = useState(false);
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [loggingIn, setLoggingIn] = useState(false);

  useEffect(() => {
    checkHealth()
      .then(() => setOnline(true))
      .catch(() => setOnline(false));
  }, []);

  async function handleAdminLogin(e) {
    e.preventDefault();
    setLoginError("");
    setLoggingIn(true);
    try {
      await adminLogin(password);
      setIsAdmin(true);
      sessionStorage.setItem("isAdmin", "true");
      setShowLogin(false);
      setPassword("");
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoggingIn(false);
    }
  }

  function handleLogout() {
    setIsAdmin(false);
    setTab("chat");
    sessionStorage.removeItem("isAdmin");
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <span className="logo">🤖</span>
         <div className="brand-text">
          <h1>Nova</h1>
          <span>Your Intelligent AI Assistant</span>
         </div>
        </div>
        <div className="header-right">
          <span className={`status ${online === null ? "" : online ? "up" : "down"}`}>
            {online === null ? "Checking…" : online ? "API online" : "API offline"}
          </span>
          {isAdmin ? (
            <button className="admin-btn active" onClick={handleLogout} title="Logout admin">
              🔓
            </button>
          ) : (
            <button className="admin-btn" onClick={() => setShowLogin(true)} title="Admin login">
              🔒
            </button>
          )}
        </div>
      </header>

      {isAdmin && (
        <nav className="tabs">
          {ADMIN_TABS.map((t) => (
            <button
              key={t.id}
              className={`tab ${tab === t.id ? "active" : ""}`}
              onClick={() => setTab(t.id)}
            >
              {t.icon} {t.label}
            </button>
          ))}
        </nav>
      )}

      <main className="content">
        {tab === "chat" && <ChatPanel />}
        {isAdmin && tab === "website" && <WebsitePanel />}
        {isAdmin && tab === "document" && <DocumentPanel />}
      </main>

      {showLogin && (
        <div className="modal-overlay" onClick={() => setShowLogin(false)}>
          <form className="modal" onClick={(e) => e.stopPropagation()} onSubmit={handleAdminLogin}>
            <h2>Admin Login</h2>
            <p className="muted">Enter the admin password to manage knowledge sources.</p>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoFocus
            />
            {loginError && <p className="notice error">{loginError}</p>}
            <div className="modal-actions">
              <button type="button" className="btn btn-secondary" onClick={() => setShowLogin(false)}>
                Cancel
              </button>
              <button type="submit" className="btn" disabled={loggingIn || !password}>
                {loggingIn ? "Verifying…" : "Login"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;
