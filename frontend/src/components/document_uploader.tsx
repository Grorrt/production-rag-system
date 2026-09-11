import { useState, useRef } from "react";

interface DocumentUploaderProps { token: string }

const ALLOWED_TYPES = [".pdf", ".html", ".htm", ".md", ".mdx", ".txt"];

function DocumentUploader({ token }: DocumentUploaderProps) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<{ message: string; chunks_created: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File) {
    const ext = "." + file.name.split(".").pop()?.toLowerCase();
    if (!ALLOWED_TYPES.includes(ext)) {
      setError(`Unsupported file type: ${ext}`);
      return;
    }

    setFileName(file.name);
    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/api/ingest/upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Upload failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }

  return (
    <div className="p-4 space-y-3">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200 ${
          dragging
            ? "border-primary-400 bg-primary-50/50 dark:bg-primary-900/20 scale-[1.02]"
            : "border-surface-300 dark:border-surface-600 hover:border-surface-400 dark:hover:border-surface-500 hover:bg-surface-50/50 dark:hover:bg-surface-800/50"
        }`}>
        <input ref={inputRef} type="file" accept=".pdf,.html,.htm,.md,.mdx,.txt" onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }} className="hidden" />

        {uploading ? (
          <div className="flex flex-col items-center gap-3">
            <span className="w-10 h-10 border-3 border-primary-300 border-t-primary-600 rounded-full animate-spin" />
            <div>
              <p className="text-sm font-medium text-surface-700 dark:text-surface-300">Processing...</p>
              <p className="text-xs text-surface-400 mt-0.5">{fileName}</p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
              <UploadIcon />
            </div>
            <div>
              <p className="text-sm font-medium text-surface-700 dark:text-surface-300">Drop files here or click to browse</p>
              <p className="text-xs text-surface-400 mt-0.5">PDF, HTML, Markdown, TXT (max 10MB)</p>
            </div>
          </div>
        )}
      </div>

      {error && (
        <div className="flex items-center gap-2 px-4 py-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
          <ErrorIcon /> {error}
        </div>
      )}

      {result && (
        <div className="flex items-center gap-2 px-4 py-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
          <CheckIcon /> {result.chunks_created} chunks created successfully
        </div>
      )}
    </div>
  );
}

function UploadIcon() { return <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>; }
function ErrorIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>; }
function CheckIcon() { return <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>; }

export default DocumentUploader;
