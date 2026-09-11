import { useState, useRef, useEffect } from "react";
import MessageBubble from "./message_bubble";
import DocumentUploader from "./document_uploader";
import { askQuestion } from "../hooks/use_rag_api";

interface Message {
  text: string;
  isUser: boolean;
  sources?: Array<{ source: string; page: string | null; chunk_id: string | null; reference: string }>;
}

interface ChatInterfaceProps { token: string }

const suggestions = [
  "What documents are available?",
  "Summarize the main topics",
  "List key findings",
  "Explain the methodology",
];

function ChatInterface({ token }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I'm your knowledge assistant. Upload documents and ask me anything about them.", isUser: false },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showUpload, setShowUpload] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (!loading) inputRef.current?.focus();
  }, [loading]);

  async function handleSend(question?: string) {
    const q = question || input.trim();
    if (!q || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { text: q, isUser: true }]);
    setLoading(true);

    try {
      const result = await askQuestion(q, token);
      setMessages((prev) => [...prev, { text: result.answer, isUser: false, sources: result.sources }]);
    } catch (err: any) {
      setMessages((prev) => [...prev, { text: `Error: ${err.message}`, isUser: false }]);
    } finally {
      setLoading(false);
    }
  }

  const isEmpty = messages.length === 1;

  return (
    <div className="flex-1 flex flex-col h-full">
      <div className="flex items-center justify-between px-6 py-3 border-b border-surface-200 dark:border-surface-700/50 glass shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center">
            <ChatIcon />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-surface-900 dark:text-surface-50">Chat</h2>
            <p className="text-[10px] text-surface-400">Ask questions about your documents</p>
          </div>
        </div>
        <button onClick={() => setShowUpload(!showUpload)}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-xl transition-all duration-200 bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 hover:bg-primary-100 dark:hover:bg-primary-900/50 active:scale-[0.97]">
          <UploadIcon />
          {showUpload ? "Close" : "Upload"}
        </button>
      </div>

      {showUpload && (
        <div className="border-b border-surface-200 dark:border-surface-700/50 bg-surface-50/50 dark:bg-surface-800/50">
          <DocumentUploader token={token} />
        </div>
      )}

      <div className="flex-1 overflow-y-auto px-4 lg:px-8 py-4 space-y-4">
        {isEmpty && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center animate-fade-in -mt-8">
            <div className="w-20 h-20 gradient-bg rounded-3xl flex items-center justify-center mb-5 shadow-xl shadow-primary-500/20">
              <RocketIcon />
            </div>
            <h3 className="text-xl font-bold text-surface-900 dark:text-surface-50 mb-2">How can I help you?</h3>
            <p className="text-sm text-surface-400 max-w-md mb-6">Upload documents and ask questions — I'll find answers with citations.</p>
            <div className="grid grid-cols-2 gap-2 w-full max-w-md">
              {suggestions.map((s) => (
                <button key={s} onClick={() => handleSend(s)}
                  className="text-left px-4 py-2.5 text-sm bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-xl hover:border-primary-300 dark:hover:border-primary-600 hover:bg-primary-50/50 dark:hover:bg-primary-900/20 transition-all duration-200 text-surface-600 dark:text-surface-400">
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <MessageBubble key={idx} text={msg.text} isUser={msg.isUser} sources={msg.sources} />
        ))}

        {loading && (
          <div className="flex justify-start message-enter">
            <div className="bg-white dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-2xl rounded-bl-md px-5 py-4 shadow-sm">
              <div className="flex gap-1.5">
                <span className="typing-dot w-2.5 h-2.5" />
                <span className="typing-dot w-2.5 h-2.5" />
                <span className="typing-dot w-2.5 h-2.5" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="px-4 lg:px-8 py-4 border-t border-surface-200 dark:border-surface-700/50 glass shrink-0">
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex gap-3">
          <div className="relative flex-1">
            <input ref={inputRef} type="text" value={input} onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..." disabled={loading}
              className="input-field pr-12" />
            <button type="submit" disabled={loading || !input.trim()}
              className="absolute right-1.5 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-primary-600 hover:bg-primary-700 text-white disabled:opacity-40 transition-all duration-200 disabled:cursor-not-allowed">
              <SendIcon />
            </button>
          </div>
        </form>
        <p className="text-[10px] text-surface-400 mt-2 text-center">Responses are generated from your uploaded documents and general knowledge</p>
      </div>
    </div>
  );
}

function ChatIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>; }
function UploadIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>; }
function SendIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>; }
function RocketIcon() { return <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>; }

export default ChatInterface;
