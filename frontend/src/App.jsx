import { useState, useEffect } from "react";
import {
  MessageSquare,
  LogIn,
  Loader2,
  AlertCircle,
  Send,
} from "lucide-react";

function App() {
  // =========================
  // Authentication state
  // =========================
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [sessionId, setSessionId] = useState(() => {
  const savedSessionId = localStorage.getItem("session_id");

  if (savedSessionId) {
    return savedSessionId;
  }

  const newSessionId = crypto.randomUUID();
  localStorage.setItem("session_id", newSessionId);

  return newSessionId;
});

  // =========================
  // Chat state
  // =========================
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);

  // =========================
  // Check authentication
  // =========================
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth/status");

        if (!response.ok) {
          throw new Error("Failed to check authentication");
        }

        const data = await response.json();
        setAuthenticated(data.authenticated);
      } catch (err) {
        console.error("Auth check failed:", err);
      }
    };

    checkAuth();
  }, []);


  useEffect(() => {
  const loadHistory = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/agent/history/${sessionId}`
      );

      if (!response.ok) {
        throw new Error("Failed to load conversation history");
      }

      const data = await response.json();

      const restoredMessages = data.messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
      }));

      setMessages(restoredMessages);

    } catch (err) {
      console.error("Failed to load chat history:", err);
    }
  };

  if (authenticated && sessionId) {
    loadHistory();
  }
}, [authenticated, sessionId]);

  // =========================
  // Login
  // =========================
  const login = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/login");

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();

      if (!data.authorization_url) {
        throw new Error("No authorization URL received from server.");
      }

      window.location.href = data.authorization_url;
    } catch (err) {
      console.error("Login failed:", err);
      setError(
        err.message === "Failed to fetch"
          ? "Couldn't reach the server. Is the backend running?"
          : err.message
      );
      setLoading(false);
    }
  };

  const newChat = () => {
  const newSessionId = crypto.randomUUID();

  localStorage.setItem("session_id", newSessionId);

  setSessionId(newSessionId);
  setMessages([]);
  setMessage("");
  setError(null);
};

  // =========================
  // Send message to Agent
  // =========================
  const sendMessage = async () => {
    if (!message.trim() || sending) {
      return;
    }

    const userMessage = message.trim();

    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    // Clear input
    setMessage("");

    // Start loading
    setSending(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/agent?message=${encodeURIComponent(userMessage)}&session_id=${encodeURIComponent(sessionId)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error(
          `Agent request failed with status ${response.status}`
        );
      }

      const data = await response.json();

      // Show agent response
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (err) {
      console.error("Agent error:", err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong while contacting the Teams agent.",
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  // =========================
  // Handle Enter key
  // =========================
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className={`w-full ${authenticated ? "max-w-2xl" : "max-w-sm"}`}>
        <div className="bg-slate-800/60 backdrop-blur-xl border border-slate-700/50 rounded-2xl shadow-2xl p-8">
          {/* =========================
              Header
          ========================= */}
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <MessageSquare className="w-8 h-8 text-white" />
            </div>
          </div>

          <h1 className="text-2xl font-semibold text-white text-center mb-2">
            Goku's Graph Assistant
          </h1>

          <p className="text-slate-400 text-center text-sm mb-8">
            {authenticated
              ? "Connected to Microsoft Teams"
              : "Sign in with your Microsoft account to get started"}
          </p>

          {/* =========================
              Error
          ========================= */}
          {error && (
            <div className="mb-5 flex items-start gap-2 bg-red-500/10 border border-red-500/30 rounded-lg px-3 py-2.5">
              <AlertCircle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {/* =================================================
              AUTHENTICATED → CHAT
          ================================================= */}
          {authenticated ? (
            <div>
              {/* Chat status */}
              <div className="flex items-center gap-2 mb-5">
                <div className="w-2.5 h-2.5 bg-green-400 rounded-full"></div>
                <span className="text-sm text-slate-300">Teams Assistant</span>
              </div>

              {/* New Chat */}
            <button
              onClick={newChat}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-3 py-2 rounded-lg transition-all"
            >
              <MessageSquare className="w-4 h-4" />
              New Chat
            </button>

              {/* =========================
                  Messages
              ========================= */}
              <div className="h-96 overflow-y-auto space-y-3 mb-5 pr-2">
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full text-center">
                    <MessageSquare className="w-10 h-10 text-slate-600 mb-3" />
                    <p className="text-slate-400 text-sm">
                      Ask me something about your Teams chats.
                    </p>
                    <p className="text-slate-600 text-xs mt-2">
                      Example: Get the latest messages from Pragadheeswaran
                    </p>
                  </div>
                )}

                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${
                      msg.role === "user" ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
                        msg.role === "user"
                          ? "bg-indigo-600 text-white rounded-br-md"
                          : "bg-slate-700 text-slate-200 rounded-bl-md"
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}

                {/* Agent loading */}
                {sending && (
                  <div className="flex justify-start">
                    <div className="bg-slate-700 text-slate-300 px-4 py-3 rounded-2xl rounded-bl-md flex items-center gap-2 text-sm">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Thinking...
                    </div>
                  </div>
                )}
              </div>

              {/* =========================
                  Input
              ========================= */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask something about Teams..."
                  disabled={sending}
                  className="flex-1 bg-slate-700/70 border border-slate-600 text-white placeholder-slate-500 rounded-xl px-4 py-3 outline-none focus:border-indigo-500 transition-colors disabled:opacity-50"
                />

                <button
                  onClick={sendMessage}
                  disabled={sending || !message.trim()}
                  className="flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white px-5 py-3 rounded-xl transition-all"
                >
                  {sending ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          ) : (
            /* =================================================
               NOT AUTHENTICATED → LOGIN
            ================================================= */
            <button
              onClick={login}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2.5 bg-white hover:bg-slate-100 disabled:bg-slate-300 disabled:cursor-not-allowed text-slate-900 font-medium py-3 px-4 rounded-xl transition-all duration-200 shadow-lg active:scale-[0.98]"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Redirecting...
                </>
              ) : (
                <>
                  <LogIn className="w-4 h-4" />
                  Login with Microsoft
                </>
              )}
            </button>
          )}

          {/* =========================
              Footer
          ========================= */}
          <p className="text-slate-500 text-xs text-center mt-6">
            {authenticated
              ? "Powered by Microsoft Graph & Agent Framework"
              : "You'll be redirected to Microsoft to sign in securely."}
          </p>
        </div>

        {!authenticated && (
          <p className="text-slate-600 text-xs text-center mt-4">
            Powered by Microsoft Graph &amp; Agent Framework
          </p>
        )}
      </div>
    </div>
  );
}

export default App;