"use client";
import type { components } from "@/lib/api-schema";

export type Citation = components["schemas"]["CitationOut"];
export type OnSource = (revision: string, span: string) => void;

const MESSAGES: Record<string, string> = {
  engine_record_required: "Build the record before asking questions.",
  record_outdated:
    "The record was built by an earlier engine version. It is being rebuilt; ask again when it is ready.",
  run_already_active: "Another run for this patient is still in progress.",
};

export const human = (value: string) =>
  MESSAGES[value] ?? value.replaceAll("_", " ");

// "DOC-7_primary_record_2026-01-26.txt" -> "DOC-7 primary record 2026-01-26"
export const sourceLabel = (filename: string) => {
  const label = filename.replace(/\.[a-z]+$/i, "").replaceAll("_", " ");
  return label.length > 48 ? `${label.slice(0, 47)}…` : label;
};

// A value with conflicting sources carries every scenario: "40 or 50".
export const either = (values: unknown[], unit = "") =>
  values.length
    ? values.map((value) => `${display(value)}`).join(" or ") + unit
    : "Unknown";

export const display = (value: unknown): string =>
  value === null || value === undefined
    ? "—"
    : Array.isArray(value)
      ? value.map(display).join(", ")
      : typeof value === "object"
        ? JSON.stringify(value)
        : String(value);

export function Sources({
  citations,
  onSource,
}: {
  citations: Citation[];
  onSource: OnSource;
}) {
  if (!citations.length) return null;
  return (
    <div className="evidence-links">
      {citations.map((citation) => (
        <button
          key={citation.span_id}
          title={citation.quote}
          onClick={() => onSource(citation.revision_id, citation.span_id)}
        >
          {sourceLabel(citation.filename)} · L{citation.start_line}
          {citation.end_line !== citation.start_line
            ? `–${citation.end_line}`
            : ""}{" "}
          ↗
        </button>
      ))}
    </div>
  );
}

export function Status({ value }: { value: string | null | undefined }) {
  if (!value) return null;
  return (
    <span className={`status-badge ${value}`}>
      {value.replaceAll("_", " ")}
    </span>
  );
}
