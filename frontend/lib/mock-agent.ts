export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  toolInvocations?: ToolInvocation[];
}

export interface ToolInvocation {
  id: string;
  toolName: string;
  input: Record<string, unknown>;
  output?: Record<string, unknown>;
  state: "pending" | "complete";
}

export interface StreamCallbacks {
  onToken: (token: string) => void;
  onToolStart: (tool: ToolInvocation) => void;
  onToolComplete: (toolId: string, output: Record<string, unknown>) => void;
  onDone: () => void;
}

/**
 * Backend returns STREAMED PLAIN TEXT
 */
export async function streamMockResponse(
  userMessage: string,
  callbacks: StreamCallbacks,
  signal?: AbortSignal
) {
  const res = await fetch("http://localhost:8000/userquery/process", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userQuery: userMessage }),
    signal,
  });

  console.log("response: "+res)

  if (!res.ok) {
    throw new Error(`Chat API error: ${res.status}`);
  }

  if (!res.body) {
    throw new Error("No response body from chat API");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder("utf-8");

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      // Decode streamed chunk
      const textChunk = decoder.decode(value, { stream: true });

      if (textChunk) {
        callbacks.onToken(textChunk);
      }
    }
  } catch (err) {
    if ((err as any)?.name !== "AbortError") {
      console.error("Streaming error:", err);
    }
  } finally {
    callbacks.onDone();
  }
}

// =======================
// Chat History Persistence
// =======================

const STORAGE_KEY = "aether-chat-history";

export function loadChatHistory(): ChatMessage[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

export function saveChatHistory(messages: ChatMessage[]) {
  if (typeof window === "undefined") return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  } catch {
    // Storage quota exceeded or unavailable
  }
}

export function clearChatHistory() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(STORAGE_KEY);
}