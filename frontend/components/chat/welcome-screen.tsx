"use client";

import {
  Hexagon,
  Cloud,
  Search,
  Calculator,
  ImageIcon,
  ArrowRight,
} from "lucide-react";

const capabilities = [
  {
    icon: Cloud,
    label: "Weather",
    desc: "Live conditions worldwide",
    example: "What's the weather in Tokyo?",
    color: "text-sky-400",
    bg: "bg-sky-500/[0.08]",
    border: "border-sky-500/10 hover:border-sky-500/25",
    glow: "group-hover:shadow-[0_0_20px_rgba(56,189,248,0.08)]",
  },
  {
    icon: Search,
    label: "Search",
    desc: "Explore the web instantly",
    example: "Search for latest AI news",
    color: "text-emerald-400",
    bg: "bg-emerald-500/[0.08]",
    border: "border-emerald-500/10 hover:border-emerald-500/25",
    glow: "group-hover:shadow-[0_0_20px_rgba(52,211,153,0.08)]",
  },
  {
    icon: Calculator,
    label: "Calculate",
    desc: "Complex math, simplified",
    example: "Calculate 1024 * 768",
    color: "text-primary",
    bg: "bg-primary/[0.08]",
    border: "border-primary/10 hover:border-primary/25",
    glow: "group-hover:shadow-[0_0_20px_rgba(52,211,153,0.08)]",
  },
  {
    icon: ImageIcon,
    label: "Imagine",
    desc: "Generate vivid images",
    example: "Generate an image of a sunset",
    color: "text-rose-400",
    bg: "bg-rose-500/[0.08]",
    border: "border-rose-500/10 hover:border-rose-500/25",
    glow: "group-hover:shadow-[0_0_20px_rgba(251,113,133,0.08)]",
  },
];

interface WelcomeScreenProps {
  onSuggestionClick: (text: string) => void;
}

export function WelcomeScreen({ onSuggestionClick }: WelcomeScreenProps) {
  return (
    <div className="flex flex-1 items-center justify-center p-6 sm:p-8 min-h-[70vh]">
      <div className="flex flex-col items-center text-center max-w-lg w-full">
        {/* Logo */}
        <div
          className="relative mb-10 animate-fade-in"
          style={{ animationDelay: "0.1s", animationFillMode: "both" }}
        >
          <div className="absolute inset-0 bg-primary/12 rounded-full blur-3xl scale-[2] animate-glow-breathe" />
          <div className="relative flex h-20 w-20 items-center justify-center rounded-2xl bg-card border border-border/60 surface-elevated-lg">
            <Hexagon className="h-9 w-9 text-primary animate-float" />
          </div>
        </div>

        {/* Title */}
        <div
          className="animate-text-reveal"
          style={{ animationDelay: "0.2s", animationFillMode: "both" }}
        >
          <h1 className="heading-display text-foreground text-balance">
            Meet{" "}
            <span className="text-primary font-light">LLM DEBATE AGENT </span>
          </h1>
        </div>

        <p
          className="body-text text-muted-foreground mt-4 max-w-[340px] text-balance animate-text-reveal"
          style={{ animationDelay: "0.35s", animationFillMode: "both" }}
        >
         Where AI Disagress Before User Suffers
        </p>

        {/* Capabilities grid */}
        <div
          className="grid grid-cols-2 gap-2.5 mt-10 w-full max-w-md animate-fade-in"
          style={{ animationDelay: "0.5s", animationFillMode: "both" }}
        >
          {/* {capabilities.map((cap, i) => (
            <button
              key={cap.label}
              onClick={() => onSuggestionClick(cap.example)}
              className={`group relative flex flex-col items-start rounded-xl border ${cap.border} bg-card/40 p-4 text-left transition-all duration-400 hover:bg-card/80 ${cap.glow} animate-fade-in`}
              style={{
                animationDelay: `${0.55 + i * 0.07}s`,
                animationFillMode: "both",
              }}
            >
              <div className="relative w-full">
                <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${cap.bg} mb-3`}>
                  <cap.icon className={`h-4 w-4 ${cap.color}`} />
                </div>
                <p className="heading-xs text-foreground">{cap.label}</p>
                <p className="caption-text mt-1">{cap.desc}</p>
                <div className="flex items-center gap-1 mt-2.5 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-1 group-hover:translate-y-0">
                  <span className="text-[10px] text-primary/70 tracking-wide">Try it</span>
                  <ArrowRight className="h-2.5 w-2.5 text-primary/70" />
                </div>
              </div>
            </button>
          ))} */}
        </div>
      </div>
    </div>
  );
}
