"use client";

import React, { useRef, useEffect } from "react";
import { ArrowUp, Square, Sparkles } from "lucide-react";

interface ChatInputProps {
  input: string;
  setInput: (value: string) => void;
  onSubmit: () => void;
  onStop?: () => void;
  isLoading: boolean;
  suggestions?: string[];
}

export function ChatInput({
  input,
  setInput,
  onSubmit,
  onStop,
  isLoading,
  suggestions,
}: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && input.trim()) {
        onSubmit();
      }
    }
  };

  return (
    <div className="animate-slide-up">
      {/* Suggestion chips */}
      {/* {suggestions && suggestions.length > 0 && !input && (
        <div className="flex flex-wrap gap-2 mb-4 px-0.5">
          {suggestions.map((suggestion, i) => (
            <button
              key={suggestion}
              onClick={() => {
                setInput(suggestion);
                setTimeout(() => textareaRef.current?.focus(), 0);
              }}
              className="group flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-border/50 bg-card/30 hover:border-primary/25 hover:bg-primary/[0.04] transition-all duration-300 caption-text hover:text-foreground animate-fade-in"
              style={{
                animationDelay: `${0.6 + i * 0.06}s`,
                animationFillMode: "both",
              }}
            >
              <Sparkles className="h-2.5 w-2.5 text-primary/40 group-hover:text-primary/70 transition-colors duration-300" />
              <span>{suggestion}</span>
            </button>
          ))}
        </div>
      )} */}

      {/* Input area */}
      <div className="relative flex items-end gap-2 rounded-2xl border border-border/50 bg-card/40 p-2.5 glass-input surface-elevated focus-within:border-primary/25 focus-within:glow-primary transition-all duration-400">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Start Debate...."
          rows={1}
          className="flex-1 resize-none bg-transparent px-2 py-1.5 body-text text-foreground placeholder:text-muted-foreground/50 focus:outline-none"
          disabled={isLoading}
        />

        {isLoading ? (
          <button
            onClick={onStop}
            className="flex h-9 w-9 items-center justify-center rounded-xl bg-card border border-border/60 text-muted-foreground hover:text-destructive hover:border-destructive/30 transition-all duration-300 flex-shrink-0"
            aria-label="Stop generating"
          >
            <Square className="h-3 w-3 fill-current" />
          </button>
        ) : (
          <button
            onClick={onSubmit}
            disabled={!input.trim()}
            className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-primary-foreground disabled:opacity-15 hover:brightness-110 transition-all duration-300 flex-shrink-0 disabled:cursor-not-allowed glow-primary"
            aria-label="Send message"
          >
            <ArrowUp className="h-4 w-4" strokeWidth={2.5} />
          </button>
        )}
      </div>

      <p className="text-center caption-text mt-3 opacity-50">
        LLM Debate Agent can give Wrong Answer Also 
      </p>
    </div>
  );
}
