"use client";

import { Hexagon } from "lucide-react";

export function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 animate-message-in">
      <div className="flex-shrink-0 h-8 w-8 rounded-full flex items-center justify-center bg-primary/[0.06] border border-primary/15">
        <Hexagon className="h-3.5 w-3.5 text-primary animate-spin-slow" />
      </div>
      <div className="flex items-center gap-2.5 px-4 py-3 rounded-2xl rounded-bl-md glass-card surface-elevated animate-border-glow">
        <div className="flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="block h-[5px] w-[5px] rounded-full bg-primary"
              style={{
                animation: `pulse-dot 1.4s ease-in-out ${i * 0.2}s infinite`,
              }}
            />
          ))}
        </div>
        <span className="caption-text ml-0.5">
          Debate In Progress ..
        </span>
        <span className="inline-block w-[2px] h-3.5 bg-primary/60 animate-cursor-blink" />
      </div>
    </div>
  );
}
