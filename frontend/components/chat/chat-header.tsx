"use client";

import { Trash2, Hexagon, History, X } from "lucide-react";
import { useState } from "react";

interface ChatHeaderProps {
  messageCount: number;
  onClear: () => void;
  isStreaming: boolean;
  onToggleHistory?: () => void;
  showHistory?: boolean;
}

export function ChatHeader({
  messageCount,
  onClear,
  isStreaming,
  onToggleHistory,
  showHistory,
}: ChatHeaderProps) {
  const [confirmClear, setConfirmClear] = useState(false);

  return (
    <header className="flex items-center justify-between px-5 py-3 border-b border-border/40 glass-surface bg-card/50 sticky top-0 z-20">
      <div className="flex items-center gap-3">
        {/* Animated logo */}
        <div className="relative">
          <div
            className={`absolute inset-0 rounded-xl bg-primary/20 blur-lg transition-all duration-700 ${isStreaming ? "opacity-100 animate-glow-breathe scale-125" : "opacity-0 scale-100"}`}
          />
          <div className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-primary/[0.08] border border-primary/20 glow-primary-ring">
            <Hexagon
              className={`h-4 w-4 text-primary transition-all duration-500 ${isStreaming ? "scale-110 animate-spin-slow" : ""}`}
            />
            {isStreaming && (
              <span className="absolute -top-0.5 -right-0.5 flex h-2.5 w-2.5">
                <span className="absolute inline-flex h-full w-full rounded-full bg-primary opacity-60 animate-ping" />
                <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-primary" />
              </span>
            )}
          </div>
        </div>
        <div>
          <h1 className="heading-sm text-foreground flex items-center gap-2">
            LLM Debate 
            <span className="label-text text-primary/60 font-normal">v1</span>
          </h1>
          <p className="caption-text mt-0.5">
            {isStreaming
              ? "Thinking..."
              : messageCount > 0
                ? `${messageCount} message${messageCount !== 1 ? "s" : ""}`
                : "Ready to assist"}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-1.5">
        {onToggleHistory && (
          <button
            onClick={onToggleHistory}
            className={`flex h-8 items-center gap-1.5 px-2.5 rounded-lg transition-all duration-300 label-text ${
              showHistory
                ? "text-primary bg-primary/10"
                : "text-muted-foreground hover:text-foreground hover:bg-secondary/60"
            }`}
            aria-label="Toggle history"
          >
            {showHistory ? <X className="h-3.5 w-3.5" /> : <History className="h-3.5 w-3.5" />}
          </button>
        )}

        {messageCount > 0 && (
          <>
            {confirmClear ? (
              <div className="flex items-center gap-1 animate-scale-in">
                <button
                  onClick={() => {
                    onClear();
                    setConfirmClear(false);
                  }}
                  className="flex h-7 items-center px-2.5 rounded-lg text-destructive bg-destructive/10 border border-destructive/20 label-text transition-all duration-200 hover:bg-destructive/20"
                >
                  Confirm
                </button>
                <button
                  onClick={() => setConfirmClear(false)}
                  className="flex h-7 items-center px-2.5 rounded-lg text-muted-foreground hover:text-foreground label-text transition-all duration-200"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button
                onClick={() => setConfirmClear(true)}
                className="flex h-8 items-center gap-1.5 px-2.5 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/[0.08] transition-all duration-300 label-text"
                aria-label="Clear chat"
              >
                <Trash2 className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">Clear</span>
              </button>
            )}
          </>
        )}
      </div>
    </header>
  );
}
