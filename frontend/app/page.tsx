"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import {
  type ChatMessage,
  type ToolInvocation,
  streamMockResponse,
  loadChatHistory,
  saveChatHistory,
  clearChatHistory,
} from "@/lib/mock-agent";
import { ChatHeader } from "@/components/chat/chat-header";
import { MessageBubble } from "@/components/chat/message-bubble";
import { ChatInput } from "@/components/chat/chat-input";
import { TypingIndicator } from "@/components/chat/typing-indicator";
import { WelcomeScreen } from "@/components/chat/welcome-screen";

const SUGGESTIONS = [
  "What's the weather in Tokyo?",
  "Search for latest AI news",
  "Calculate 1024 * 768",
  "Generate an image of a sunset",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [mounted, setMounted] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Load history on mount
  useEffect(() => {
    const history = loadChatHistory();
    if (history.length > 0) {
      setMessages(history);
    }
    setMounted(true);
  }, []);

  // Save to localStorage whenever messages change
  useEffect(() => {
    if (mounted && messages.length > 0) {
      saveChatHistory(messages);
    }
  }, [messages, mounted]);

  const scrollToBottom = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSubmit = useCallback(async () => {
    if (!input.trim() || isStreaming) return;

    const userMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      role: "user",
      content: input.trim(),
      timestamp: Date.now(),
    };

    const assistantMessage: ChatMessage = {
      id: `msg_${Date.now() + 1}`,
      role: "assistant",
      content: "",
      timestamp: Date.now(),
      toolInvocations: [],
    };

    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setInput("");
    setIsStreaming(true);

    const abort = new AbortController();
    abortRef.current = abort;

    await streamMockResponse(
      userMessage.content,
      {
        onToken: (token) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === "assistant") {
              updated[updated.length - 1] = { ...last, content: last.content + token };
            }
            return updated;
          });
        },
        onToolStart: (tool: ToolInvocation) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === "assistant") {
              updated[updated.length - 1] = {
                ...last,
                toolInvocations: [...(last.toolInvocations || []), tool],
              };
            }
            return updated;
          });
        },
        onToolComplete: (toolId: string, output: Record<string, unknown>) => {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            if (last.role === "assistant" && last.toolInvocations) {
              updated[updated.length - 1] = {
                ...last,
                toolInvocations: last.toolInvocations.map((t) =>
                  t.id === toolId ? { ...t, state: "complete" as const, output } : t,
                ),
              };
            }
            return updated;
          });
        },
        onDone: () => {
          setIsStreaming(false);
          abortRef.current = null;
        },
      },
      abort.signal,
    );
  }, [input, isStreaming]);

  const handleStop = useCallback(() => {
    abortRef.current?.abort();
    setIsStreaming(false);
  }, []);

  const handleClear = useCallback(() => {
    setMessages([]);
    clearChatHistory();
    setShowHistory(false);
  }, []);

  const handleSuggestionClick = useCallback(
    (text: string) => {
      setInput(text);
    },
    [],
  );

  if (!mounted) return null;

  return (
    <div className="flex h-dvh flex-col bg-background noise-overlay relative">
      {/* Ambient glow */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[700px] h-[500px] bg-primary/[0.03] rounded-full blur-[120px]" />
        <div className="absolute bottom-[-5%] right-[-5%] w-[500px] h-[400px] bg-primary/[0.02] rounded-full blur-[100px]" />
      </div>

      <div className="relative flex flex-col h-full z-10">
        <ChatHeader
          messageCount={messages.length}
          onClear={handleClear}
          isStreaming={isStreaming}
          onToggleHistory={() => setShowHistory(!showHistory)}
          showHistory={showHistory}
        />

        {/* Chat messages area */}
        <div className="flex-1 overflow-y-auto chat-scrollbar">
          {messages.length === 0 ? (
            <WelcomeScreen onSuggestionClick={handleSuggestionClick} />
          ) : (
            <div className="mx-auto max-w-2xl px-4 py-8 flex flex-col gap-6">
              {messages
                .filter((m) => m.content || (m.toolInvocations && m.toolInvocations.length > 0))
                .map((message, index) => (
                  <MessageBubble key={message.id} message={message} index={index} />
                ))}
              {isStreaming &&
                messages.length > 0 &&
                messages[messages.length - 1].role === "assistant" &&
                !messages[messages.length - 1].content &&
                (!messages[messages.length - 1].toolInvocations ||
                  messages[messages.length - 1].toolInvocations?.length === 0) && (
                  <TypingIndicator />
                )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="border-t border-border/30 glass-surface bg-background/50">
          <div className="mx-auto max-w-2xl px-4 py-4">
            <ChatInput
              input={input}
              setInput={setInput}
              onSubmit={handleSubmit}
              onStop={handleStop}
              isLoading={isStreaming}
              suggestions={messages.length === 0 ? SUGGESTIONS : undefined}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
