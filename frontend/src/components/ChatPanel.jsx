
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendChat } from "../api.js";

const GREETING =
  "Hi there! 👋 I'm Nova, your AI assistant. I can answer questions about the company, its services, documents, and more. How can I help you today?";

const SUGGESTIONS = [
  "What services does the company offer?",
  "Tell me about the company",
  "How can I get in touch?",
  "What technologies do you use?",
];

function NovaAvatar() {
  return (
    <div className="nova-avatar" title="Nova">
      🤖
    </div>
  );
}

function ChatPanel() {
  const [messages, setMessages] = useState([
    { role: "assistant", text: GREETING },
  ]);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function submit(text) {
    const question = text.trim();
    if (!question || loading) return;

    setShowSuggestions(false);
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChat(question, sessionId);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "error", text: err.message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit(input);
    }
  }

  return (
    <section className="panel chat">
      <div className="messages">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`message-row ${m.role}-row`}
          >
            {m.role === "assistant" && <NovaAvatar />}

            <div className={`bubble ${m.role}`}>
              {m.role === "assistant" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {m.text}
                </ReactMarkdown>
              ) : (
                m.text
              )}
            </div>
          </div>
        ))}

        {showSuggestions && (
          <div className="suggestions">
            <p className="suggestions-label">Try asking:</p>
            <div className="chips">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  className="chip"
                  onClick={() => submit(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="message-row assistant-row">
            <NovaAvatar />
            <div className="bubble assistant typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="composer">
        <textarea
          rows={1}
          value={input}
          placeholder="Message Nova..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          className="btn"
          onClick={() => submit(input)}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </section>
  );
}

export default ChatPanel;
