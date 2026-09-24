import type { components } from "./api-schema";

export type Patient = components["schemas"]["PatientOut"];
export type Session = components["schemas"]["SessionOut"];
export type SourceRevision = components["schemas"]["RevisionOut"];
export type Source = components["schemas"]["SourceOut"];
export type Job = components["schemas"]["JobOut"];
export type ImportBatch = components["schemas"]["ImportBatchOut"];
export type Snapshot = components["schemas"]["SnapshotOut"];

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api/v1${path}`, {
    ...init,
    cache: "no-store",
  });
  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "request_failed" }));
    const code =
      typeof error.detail === "string" ? error.detail : "request_failed";
    throw new Error(`${response.status}: ${code.replaceAll("_", " ")}`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export async function allPages<T extends { id: string }>(
  path: string,
): Promise<T[]> {
  const rows: T[] = [];
  let cursor = "";
  for (;;) {
    const page = await api<T[]>(`${path}${cursor ? `?after=${cursor}` : ""}`);
    rows.push(...page);
    if (page.length < 100) return rows;
    cursor = page[page.length - 1].id;
  }
}
