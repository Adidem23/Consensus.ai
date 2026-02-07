"use client";

import React, { useState } from "react";
import { Hexagon, User, Copy, Check, Clock } from "lucide-react";
import type { ChatMessage, ToolInvocation } from "@/lib/mock-agent";
import {
  WeatherCard,
  SearchCard,
  CalculateCard,
  ImageGenCard,
} from "./tool-card";

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="opacity-0 group-hover:opacity-100 transition-all duration-300 p-1 rounded-md hover:bg-secondary/50 text-muted-foreground hover:text-foreground"
      aria-label="Copy message"
    >
      {copied ? (
        <Check className="h-3 w-3 text-primary" />
      ) : (
        <Copy className="h-3 w-3" />
      )}
    </button>
  );
}

function formatTime(ts: number) {
  return new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function renderMarkdown(text: string) {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];
  let inCodeBlock = false;
  let codeContent = "";
  let codeLang = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith("```")) {
      if (inCodeBlock) {
        elements.push(
          <div key={`code-${i}`} className="my-2.5 rounded-lg overflow-hidden border border-border/40 surface-elevated">
            {codeLang && (
              <div className="bg-secondary/40 px-3.5 py-1.5 border-b border-border/30">
                <span className="label-text text-muted-foreground">{codeLang}</span>
              </div>
            )}
            <pre className="bg-secondary/15 p-3.5 overflow-x-auto">
              <code className="mono-text text-foreground">{codeContent.trim()}</code>
            </pre>
          </div>,
        );
        inCodeBlock = false;
        codeContent = "";
        codeLang = "";
      } else {
        inCodeBlock = true;
        codeLang = line.slice(3).trim();
      }
      continue;
    }

    if (inCodeBlock) {
      codeContent += `${line}\n`;
      continue;
    }

    if (line.startsWith("### ")) {
      elements.push(<h3 key={i} className="heading-sm text-foreground mt-3 mb-1">{line.slice(4)}</h3>);
    } else if (line.startsWith("## ")) {
      elements.push(<h2 key={i} className="heading-md text-foreground mt-3 mb-1">{line.slice(3)}</h2>);
    } else if (line.startsWith("# ")) {
      elements.push(<h1 key={i} className="heading-lg text-foreground mt-3 mb-1">{line.slice(2)}</h1>);
    } else if (line.startsWith("- ") || line.startsWith("* ")) {
      elements.push(
        <li key={i} className="body-sm text-foreground ml-4 list-disc marker:text-primary/30">
          {renderInline(line.slice(2))}
        </li>,
      );
    } else if (/^\d+\. /.test(line)) {
      elements.push(
        <li key={i} className="body-sm text-foreground ml-4 list-decimal marker:text-primary/30">
          {renderInline(line.replace(/^\d+\.\s/, ""))}
        </li>,
      );
    } else if (line.trim() === "") {
      elements.push(<div key={i} className="h-1.5" />);
    } else {
      elements.push(<p key={i} className="body-sm text-foreground">{renderInline(line)}</p>);
    }
  }

  return elements;
}

function renderInline(text: string): React.ReactNode {
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*(.+?)\*\*)|(`(.+?)`)|(--.+?--)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) parts.push(text.slice(lastIndex, match.index));
    if (match[2]) {
      parts.push(<strong key={match.index} className="font-semibold text-foreground">{match[2]}</strong>);
    } else if (match[4]) {
      parts.push(
        <code key={match.index} className="px-1.5 py-0.5 rounded bg-secondary/40 text-primary mono-text border border-border/30">
          {match[4]}
        </code>,
      );
    }
    lastIndex = match.index + match[0].length;
  }

  if (lastIndex < text.length) parts.push(text.slice(lastIndex));
  return parts.length > 0 ? parts : text;
}

function ToolRenderer({ tool }: { tool: ToolInvocation }) {
  const data = tool.state === "complete" && tool.output ? tool.output : { status: "pending", ...tool.input };

  switch (tool.toolName) {
    case "getWeather":
      return <WeatherCard data={data} />;
    case "searchWeb":
      return <SearchCard data={data} />;
    case "calculate":
      return <CalculateCard data={data} />;
    case "generateImage":
      return <ImageGenCard data={data} />;
    default:
      return null;
  }
}

export function MessageBubble({
  message,
  index,
}: {
  message: ChatMessage;
  index: number;
}) {
  const isUser = message.role === "user";

  return (
    <div
      className="animate-message-in group"
      style={{
        animationDelay: `${Math.min(index * 0.03, 0.15)}s`,
        animationFillMode: "both",
      }}
    >
      <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}>
        {/* Avatar */}
        <div
          className={`flex-shrink-0 h-7 w-7 rounded-full flex items-center justify-center transition-all duration-300 ${
            isUser
              ? "bg-foreground/[0.06] text-foreground/70 border border-border/40"
              : "bg-primary/[0.06] text-primary border border-primary/15"
          }`}
        >
          {isUser ? <User className="h-3 w-3" /> : <Hexagon className="h-3 w-3" />}
        </div>

        {/* Content */}
        <div className={`flex flex-col max-w-[82%] ${isUser ? "items-end" : "items-start"}`}>
          <div className="flex items-center gap-2 mb-1 px-0.5">
            <span className="heading-xs text-muted-foreground">{isUser ? "You" : "Aether"}</span>
            <span className="flex items-center gap-1 caption-text opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <Clock className="h-2.5 w-2.5" />
              {formatTime(message.timestamp)}
            </span>
          </div>

          {/* Text */}
          {message.content && (
            <div
              className={`relative rounded-2xl px-4 py-3 ${
                isUser
                  ? "bg-foreground/[0.05] border border-border/30 rounded-br-sm"
                  : "glass-card rounded-bl-sm surface-elevated"
              }`}
            >
              <div className="flex flex-col gap-0.5">
                {isUser ? (
                  <p className="body-sm text-foreground">{message.content}</p>
                ) : (
                  renderMarkdown(message.content)
                )}
              </div>
              {!isUser && message.content && (
                <div className="flex items-center gap-1 mt-2 pt-2 border-t border-border/20">
                  <CopyButton text={message.content} />
                </div>
              )}
            </div>
          )}

          {/* Tool invocations */}
          {message.toolInvocations?.map((tool) => (
            <ToolRenderer key={tool.id} tool={tool} />
          ))}
        </div>
      </div>
    </div>
  );
}
