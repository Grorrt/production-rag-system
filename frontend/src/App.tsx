import { useState, useEffect, createContext, useContext } from "react";
import Sidebar from "./components/sidebar";
import ChatInterface from "./components/chat_interface";
import Dashboard from "./components/dashboard";

type Page = "chat" | "dashboard";

interface ThemeCtx { dark: boolean; toggle: () => void }
const ThemeContext = createContext<ThemeCtx>({ dark: false, toggle: () => {} });
export const useTheme = () => useContext(ThemeContext);

function App() {
  const [currentPage, setCurrentPage] = useState<Page>("chat");
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));
  const [username, setUsername] = useState<string>("");
  const [dark, setDark] = useState(() => localStorage.getItem("theme") === "dark");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  function handleLogin(newToken: string, user: string) {
    setToken(newToken);
    setUsername(user);
  }

  function handleLogout() {
    setToken(null);
    setUsername("");
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
  }

  if (!token) {
    return <ThemeContext.Provider value={{ dark, toggle: () => setDark(d => !d) }}>
      <LoginForm onLogin={handleLogin} />
    </ThemeContext.Provider>;
  }

  return (
    <ThemeContext.Provider value={{ dark, toggle: () => setDark(d => !d) }}>
      <div className="flex h-screen bg-surface-50 dark:bg-surface-900 transition-colors duration-200">
        <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} username={username} onLogout={handleLogout} />
        <main className="flex-1 flex flex-col min-w-0">
          {currentPage === "chat" && <ChatInterface token={token} />}
          {currentPage === "dashboard" && <Dashboard token={token} />}
        </main>
      </div>
    </ThemeContext.Provider>
  );
}

function LoginForm({ onLogin }: { onLogin: (token: string, user: string) => void }) {
  const { dark, toggle } = useTheme();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const endpoint = isRegister ? "/api/auth/register" : "/api/auth/login";
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || (isRegister ? "Registration failed" : "Login failed"));
      }

      if (isRegister) {
        setIsRegister(false);
        setError("Registration successful! Please sign in.");
        setLoading(false);
        return;
      }

      const data = await res.json();
      onLogin(data.access_token, username);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-surface-50 dark:bg-surface-900">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary-400/20 dark:bg-primary-600/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-400/20 dark:bg-purple-600/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary-500/5 dark:bg-primary-400/5 rounded-full blur-3xl" />
      </div>

      <div className="relative w-full max-w-md mx-4 animate-fade-in">
        <div className="glass-card p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 gradient-bg rounded-2xl mb-4 shadow-lg shadow-primary-500/25">
              <span className="text-2xl font-bold text-white">R</span>
            </div>
            <h1 className="text-2xl font-bold">RAG System</h1>
            <p className="text-surface-500 dark:text-surface-400 mt-1 text-sm">
              {isRegister ? "Create your account" : "Knowledge Assistant Login"}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">Username</label>
              <input type="text" value={username} onChange={(e) => setUsername(e.target.value)}
                className="input-field" placeholder="Enter your username" required />
            </div>

            <div>
              <label className="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1.5">Password</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                className="input-field" placeholder="Enter your password" required />
            </div>

            {error && (
              <p className={`text-sm p-3 rounded-xl ${error.includes("successful") ? "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400" : "bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400"}`}>
                {error}
              </p>
            )}

            <button type="submit" disabled={loading}
              className="btn-primary w-full flex items-center justify-center gap-2">
              {loading ? (
                <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> Please wait...</>
              ) : isRegister ? "Create Account" : "Sign In"}
            </button>
          </form>

          <div className="flex items-center justify-between mt-6">
            <p className="text-sm text-surface-500 dark:text-surface-400">
              {isRegister ? "Already have an account?" : "Don't have an account?"}
              <button onClick={() => { setIsRegister(!isRegister); setError(""); }}
                className="ml-1 text-primary-600 dark:text-primary-400 hover:underline font-medium">
                {isRegister ? "Sign In" : "Register"}
              </button>
            </p>
            <button onClick={toggle} className="p-2 rounded-xl hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors" title="Toggle theme">
              {dark ? <SunIcon /> : <MoonIcon />}
            </button>
          </div>
        </div>
        <p className="text-center mt-6 text-xs text-surface-400">RAG System v2.0 — Powered by LangChain + Groq</p>
      </div>
    </div>
  );
}

function SunIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>; }
function MoonIcon() { return <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>; }

export default App;
