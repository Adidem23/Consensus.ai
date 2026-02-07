"use client";

import {
  Cloud,
  Sun,
  CloudRain,
  CloudLightning,
  Search,
  Calculator,
  ImageIcon,
  Loader2,
  ExternalLink,
  Wind,
  Droplets,
  Thermometer,
} from "lucide-react";

function WeatherIcon({ condition }: { condition: string }) {
  const lower = condition.toLowerCase();
  if (lower.includes("sunny") || lower.includes("clear"))
    return <Sun className="h-8 w-8 text-amber-400 drop-shadow-[0_0_10px_rgba(251,191,36,0.25)]" />;
  if (lower.includes("rain"))
    return <CloudRain className="h-8 w-8 text-sky-400 drop-shadow-[0_0_10px_rgba(56,189,248,0.25)]" />;
  if (lower.includes("storm"))
    return <CloudLightning className="h-8 w-8 text-yellow-400 drop-shadow-[0_0_10px_rgba(250,204,21,0.25)]" />;
  return <Cloud className="h-8 w-8 text-muted-foreground" />;
}

export function WeatherCard({
  data,
}: {
  data: Record<string, unknown>;
}) {
  if (data.status === "loading" || data.status === "pending") {
    return (
      <div className="animate-tool-pulse rounded-xl glass-card p-4 mt-2.5 w-full max-w-xs surface-elevated">
        <div className="flex items-center gap-3">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
          <div>
            <p className="heading-xs text-foreground">Fetching weather</p>
            <p className="caption-text mt-0.5">{data.city as string}</p>
          </div>
        </div>
        <div className="mt-3 h-20 rounded-lg animate-shimmer" />
      </div>
    );
  }

  return (
    <div className="animate-scale-in rounded-xl glass-card p-5 mt-2.5 w-full max-w-xs overflow-hidden surface-elevated">
      <div className="flex items-start justify-between">
        <div>
          <p className="label-text text-primary">Weather</p>
          <p className="heading-md text-foreground mt-1">{data.city as string}</p>
        </div>
        <WeatherIcon condition={(data.condition as string) || ""} />
      </div>
      <div className="mt-3 flex items-end gap-1">
        <span className="text-5xl font-extralight text-foreground tracking-tighter font-mono">
          {data.temperature as number}
        </span>
        <span className="text-lg text-muted-foreground mb-1.5 font-light">
          {"°"}{data.unit as string}
        </span>
      </div>
      <p className="body-sm text-primary font-medium mt-1">{data.condition as string}</p>
      <div className="mt-4 flex gap-4 border-t border-border/30 pt-3">
        <div className="flex items-center gap-1.5">
          <Droplets className="h-3 w-3 text-sky-400/60" />
          <span className="caption-text">{data.humidity as number}%</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Wind className="h-3 w-3 text-sky-300/60" />
          <span className="caption-text">{data.windSpeed as number} km/h</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Thermometer className="h-3 w-3 text-primary/60" />
          <span className="caption-text">
            Feels {((data.temperature as number) ?? 0) + 2}{"°"}
          </span>
        </div>
      </div>
    </div>
  );
}

export function SearchCard({
  data,
}: {
  data: Record<string, unknown>;
}) {
  if (data.status === "searching" || data.status === "pending") {
    return (
      <div className="animate-tool-pulse rounded-xl glass-card p-4 mt-2.5 w-full max-w-md surface-elevated">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/[0.08] border border-emerald-500/15">
            <Search className="h-4 w-4 animate-pulse text-emerald-400" />
          </div>
          <div>
            <p className="heading-xs text-foreground">Searching</p>
            <p className="caption-text mt-0.5">{'"'}{data.query as string}{'"'}</p>
          </div>
        </div>
        <div className="mt-3 flex flex-col gap-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 rounded-lg animate-shimmer" />
          ))}
        </div>
      </div>
    );
  }

  const results = (data.results || []) as Array<{ title: string; snippet: string; url: string }>;

  return (
    <div className="animate-scale-in rounded-xl glass-card p-4 mt-2.5 w-full max-w-md surface-elevated">
      <div className="flex items-center gap-2.5 mb-3">
        <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-emerald-500/[0.08] border border-emerald-500/15">
          <Search className="h-3 w-3 text-emerald-400" />
        </div>
        <p className="caption-text">Results for {'"'}{data.query as string}{'"'}</p>
      </div>
      <div className="flex flex-col gap-1.5">
        {results.map((result, i) => (
          <a
            key={i}
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group rounded-lg border border-border/30 bg-card/20 p-3 hover:border-emerald-500/25 hover:bg-emerald-500/[0.03] transition-all duration-300"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1 min-w-0">
                <p className="heading-xs text-foreground group-hover:text-emerald-400 transition-colors truncate">
                  {result.title}
                </p>
                <p className="caption-text mt-1 line-clamp-2 leading-relaxed">
                  {result.snippet}
                </p>
              </div>
              <ExternalLink className="h-3 w-3 text-muted-foreground flex-shrink-0 mt-0.5 opacity-0 group-hover:opacity-100 transition-all duration-300" />
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}

export function CalculateCard({
  data,
}: {
  data: Record<string, unknown>;
}) {
  if (data.status === "calculating" || data.status === "pending") {
    return (
      <div className="animate-tool-pulse rounded-xl glass-card p-4 mt-2.5 w-full max-w-xs surface-elevated">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/[0.08] border border-primary/15">
            <Calculator className="h-4 w-4 animate-pulse text-primary" />
          </div>
          <div>
            <p className="heading-xs text-foreground">Calculating</p>
            <p className="mono-text text-muted-foreground">{data.expression as string}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-scale-in rounded-xl glass-card p-4 mt-2.5 w-full max-w-xs surface-elevated">
      <div className="flex items-center gap-2 mb-3">
        <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-primary/[0.08] border border-primary/15">
          <Calculator className="h-3 w-3 text-primary" />
        </div>
        <p className="label-text text-primary">Calculator</p>
      </div>
      <div className="rounded-lg bg-secondary/20 border border-border/20 p-4 surface-inset">
        <p className="mono-text text-muted-foreground">{data.expression as string}</p>
        <div className="flex items-baseline gap-1.5 mt-2">
          <span className="text-xs text-primary/50">=</span>
          <span className="text-3xl font-extralight text-foreground tracking-tight font-mono">
            {data.result as number}
          </span>
        </div>
      </div>
    </div>
  );
}

export function ImageGenCard({
  data,
}: {
  data: Record<string, unknown>;
}) {
  if (data.status === "generating" || data.status === "pending") {
    return (
      <div className="animate-tool-pulse rounded-xl glass-card p-4 mt-2.5 w-full max-w-sm surface-elevated">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-rose-500/[0.08] border border-rose-500/15">
            <ImageIcon className="h-4 w-4 animate-pulse text-rose-400" />
          </div>
          <div>
            <p className="heading-xs text-foreground">Generating image</p>
            <p className="caption-text truncate max-w-[200px] mt-0.5">{data.prompt as string}</p>
          </div>
        </div>
        <div className="mt-3 h-48 rounded-lg animate-shimmer" />
      </div>
    );
  }

  return (
    <div className="animate-scale-in rounded-xl glass-card overflow-hidden mt-2.5 w-full max-w-sm surface-elevated">
      {data.imageUrl && (
        <div className="relative h-52 bg-secondary/20">
          <img
            src={(data.imageUrl as string) || "/placeholder.svg"}
            alt={(data.description as string) || "Generated image"}
            className="h-full w-full object-cover"
            crossOrigin="anonymous"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-card/70 to-transparent" />
        </div>
      )}
      <div className="p-4">
        <div className="flex items-center gap-1.5 mb-1">
          <ImageIcon className="h-3 w-3 text-rose-400" />
          <p className="label-text text-rose-400">Generated</p>
        </div>
        <p className="caption-text leading-relaxed">{data.prompt as string}</p>
      </div>
    </div>
  );
}
