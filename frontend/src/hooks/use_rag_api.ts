const API_BASE = import.meta.env.VITE_API_URL || "/api";

interface ChatResponse {
  question: string;
  answer: string;
  sources: Array<{
    source: string;
    page: string | null;
    chunk_id: string | null;
    reference: string;
  }>;
  source_count: number;
}

interface EvalResults {
  last_run: string;
  overall_score: number;
  retrieval: Record<string, number>;
  generation: Record<string, number>;
  latency: Record<string, number>;
}

export async function askQuestion(
  question: string,
  token: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/query/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ question, stream: false }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to get answer");
  }

  return res.json();
}

export async function uploadDocument(
  file: File,
  token: string
): Promise<{ message: string; chunks_created: number }> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/ingest/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to upload document");
  }

  return res.json();
}

export async function getEvalResults(token: string): Promise<EvalResults> {
  const res = await fetch(`${API_BASE}/evaluate/results`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch evaluation results");
  }

  return res.json();
}

export async function login(
  username: string,
  password: string
): Promise<{ access_token: string; refresh_token: string }> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Login failed");
  }

  return res.json();
}
