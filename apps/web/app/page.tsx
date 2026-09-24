"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  allPages,
  api,
  type Job,
  type ImportBatch,
  type Patient,
  type Session,
  type Snapshot,
  type Source,
  type SourceRevision,
} from "@/lib/api";

import { ImportPanel } from "./import-panel";
import { ClinicalPanel } from "./clinical-panel";

const message = (error: unknown) =>
  error instanceof Error ? error.message : "Something went wrong.";

export default function Workspace() {
  const [view, setView] = useState<
    "sources" | "abstraction" | "ask" | "documents"
  >("sources");
  const [session, setSession] = useState<Session | null>(null);
  const [starting, setStarting] = useState(true);
  const [patients, setPatients] = useState<Patient[]>([]);
  const [patient, setPatient] = useState<Patient | null>(null);
  const [documents, setDocuments] = useState<SourceRevision[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [snapshotId, setSnapshotId] = useState("");
  const [source, setSource] = useState<Source | null>(null);
  const [spanId, setSpanId] = useState("");
  const [query, setQuery] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [busy, setBusy] = useState(false);
  const [loadingSource, setLoadingSource] = useState(false);
  const [error, setError] = useState("");
  const [batches, setBatches] = useState<ImportBatch[]>([]);
  const [importNotice, setImportNotice] = useState("");
  const [removing, setRemoving] = useState(false);
  const [removeReason, setRemoveReason] = useState("");
  const patientRef = useRef<string | null>(null);
  const sourceRequest = useRef(0);
  const retryImport = useRef<{ signature: string; key: string } | null>(null);

  const loadPatients = useCallback(async () => {
    const [values, imports] = await Promise.all([
      allPages<Patient>("/patients"),
      allPages<ImportBatch>("/imports"),
    ]);
    setBatches(imports);
    setPatients(values);
    const requestedId = new URL(window.location.href).searchParams.get(
      "patient",
    );
    // Never silently switch a bookmarked patient to a different chart.
    setPatient(
      (current) =>
        current ??
        (requestedId
          ? (values.find((value) => value.id === requestedId) ?? null)
          : values.length === 1
            ? values[0]
            : null),
    );
    return values;
  }, []);

  useEffect(() => {
    api<Session>("/session")
      .then(async (value) => {
        setSession(value);
        await loadPatients();
      })
      .catch((error) => {
        if (!message(error).startsWith("401")) setError(message(error));
      })
      .finally(() => setStarting(false));
  }, [loadPatients]);

  const refresh = useCallback(async (id: string) => {
    const [docs, imports, versions] = await Promise.all([
      allPages<SourceRevision>(`/patients/${id}/documents`),
      allPages<Job>(`/patients/${id}/jobs`),
      api<Snapshot[]>(`/patients/${id}/snapshots`),
    ]);
    if (patientRef.current !== id) return;
    setDocuments(docs);
    setJobs(imports);
    setSnapshots(versions);
  }, []);

  useEffect(() => {
    patientRef.current = patient?.id ?? null;
    sourceRequest.current += 1;
    setSource(null);
    setDocuments([]);
    setJobs([]);
    setSnapshots([]);
    setSnapshotId("");
    setLoadingSource(false);
    setSpanId("");
    if (!patient) return;
    const url = new URL(window.location.href);
    url.searchParams.set("patient", patient.id);
    window.history.replaceState(null, "", url);
    let disposed = false;
    let timer: ReturnType<typeof setTimeout>;
    const poll = async () => {
      try {
        await refresh(patient.id);
      } catch (error) {
        if (!disposed) setError(message(error));
      }
      if (!disposed) timer = setTimeout(poll, 2000);
    };
    void poll();
    return () => {
      disposed = true;
      clearTimeout(timer);
    };
  }, [patient, refresh]);

  async function signIn() {
    setBusy(true);
    setError("");
    try {
      setSession(await api<Session>("/dev-session", { method: "POST" }));
      await loadPatients();
    } catch (error) {
      setError(message(error));
    } finally {
      setBusy(false);
    }
  }

  async function upload() {
    if (!session || !files.length) return;
    setBusy(true);
    setError("");
    const form = new FormData();
    files.forEach((file) => form.append("files", file));
    const signature = JSON.stringify([
      files.map((file) => [file.name, file.size, file.lastModified]),
    ]);
    if (retryImport.current?.signature !== signature)
      retryImport.current = { signature, key: crypto.randomUUID() };
    try {
      const result = await api<ImportBatch>("/imports", {
        method: "POST",
        headers: {
          "X-CSRF-Token": session.csrf_token,
          "Idempotency-Key": retryImport.current.key,
        },
        body: form,
      });
      retryImport.current = null;
      setFiles([]);
      const values = await loadPatients();
      const ids = new Set(result.jobs.map((job) => job.patient_id));
      if (ids.size === 1) {
        const next = values.find((value) => ids.has(value.id)) ?? null;
        setPatient(next);
        if (next && patientRef.current === next.id) await refresh(next.id);
      } else if (ids.size > 1) {
        setPatient(null);
        const url = new URL(window.location.href);
        url.searchParams.delete("patient");
        window.history.replaceState(null, "", url);
      }
      setImportNotice(
        ids.size > 1
          ? `${ids.size} patients detected. Records were grouped separately; choose a patient to inspect their sources.`
          : ids.size === 1
            ? "Patient detected. Your records are being processed in the matching case."
            : "These files need identity review before they can be attached to a patient.",
      );
    } catch (error) {
      setError(message(error));
    } finally {
      setBusy(false);
    }
  }

  async function openSource(id: string, targetSpan = "") {
    const request = ++sourceRequest.current;
    setLoadingSource(true);
    setError("");
    try {
      const next = await api<Source>(`/source-revisions/${id}`);
      if (sourceRequest.current === request) {
        setSource(next);
        setSpanId(targetSpan);
      }
    } catch (error) {
      if (sourceRequest.current === request) setError(message(error));
    } finally {
      if (sourceRequest.current === request) setLoadingSource(false);
    }
  }

  async function changeDocument(
    id: string,
    action: "withdraw" | "restore",
    reason?: string,
  ) {
    if (!session || !patient) return;
    setBusy(true);
    setError("");
    try {
      await api(`/patients/${patient.id}/documents/${id}/${action}`, {
        method: "POST",
        headers: {
          "X-CSRF-Token": session.csrf_token,
          "Content-Type": "application/json",
        },
        body: action === "withdraw" ? JSON.stringify({ reason }) : undefined,
      });
      setRemoving(false);
      setRemoveReason("");
      setSnapshotId("");
      if (action === "withdraw") setSource(null);
      await refresh(patient.id);
    } catch (error) {
      setError(message(error));
    } finally {
      setBusy(false);
    }
  }

  const selectedSnapshot =
    snapshots.find((value) => value.id === snapshotId) ?? snapshots[0];
  const included = new Set(
    selectedSnapshot?.manifest.map((value) => value.revision_id),
  );
  const visibleDocs = documents.filter(
    (doc) =>
      (!selectedSnapshot || included.has(doc.id)) &&
      `${doc.filename} ${doc.declared_id ?? ""}`
        .toLowerCase()
        .includes(query.toLowerCase()),
  );
  const withdrawnDocs = documents.filter((doc) => doc.withdrawn);
  const viewingLatest = !snapshotId || snapshotId === snapshots[0]?.id;
  const sourceWithdrawn = documents.some(
    (doc) => doc.id === source?.id && doc.withdrawn,
  );
  const activeJobs = jobs.filter((job) =>
    ["queued", "running"].includes(job.status),
  );
  const issues = jobs.flatMap((job) =>
    job.uploads.filter((upload) =>
      ["quarantined", "failed"].includes(upload.status),
    ),
  );
  const highlighted = source?.spans.find((span) => span.id === spanId);
  const lines = source?.text.split(/\r\n|[\n\r\v\f\x85\u2028\u2029]/) ?? [];
  if (lines.at(-1) === "") lines.pop();

  return (
    <div className="shell">
      <aside className="sidebar">
        <a className="brand" href="/">
          <span className="brand-icon">e</span>
          <span>
            Evidence<span className="brand-sub">CLINICAL WORKSPACE</span>
          </span>
        </a>
        <div className="nav-label">WORKSPACE</div>
        <button
          className={`nav-item ${view === "sources" ? "active" : ""}`}
          onClick={() => setView("sources")}
          aria-label="Source library"
        >
          <span>▤</span> Source library
        </button>
        <button
          className={`nav-item ${view === "abstraction" ? "active" : ""}`}
          onClick={() => setView("abstraction")}
          aria-label="Clinical record"
        >
          <span>◷</span> Clinical record
        </button>
        <button
          className={`nav-item ${view === "documents" ? "active" : ""}`}
          onClick={() => setView("documents")}
          aria-label="Documents"
        >
          <span>≡</span> Documents
        </button>
        <button
          className={`nav-item ${view === "ask" ? "active" : ""}`}
          onClick={() => setView("ask")}
          aria-label="Ask a question"
        >
          <span>◇</span> Ask a question
        </button>
        <div className="sidebar-bottom">
          Development workspace
          <p>Synthetic records only.</p>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <span>
            Records <span className="slash">/</span>{" "}
            <strong>
              {view === "sources"
                ? "Source library"
                : view === "abstraction"
                  ? "Clinical record"
                  : view === "documents"
                    ? "Documents"
                    : "Ask a question"}
            </strong>
          </span>
          <span className="development">LOCAL DEVELOPMENT</span>
        </header>
        <div className="content">
          <div className="page-heading">
            <h1>
              {view === "sources"
                ? "Every source. In context."
                : view === "abstraction"
                  ? "From records to a clear picture."
                  : view === "documents"
                    ? "The history behind the record."
                    : "Answers with evidence."}
            </h1>
            <p>Import records, inspect sources, and ask questions.</p>
          </div>
          {error && (
            <div role="alert" className="alert error">
              {error}
            </div>
          )}
          {starting ? (
            <div role="status" className="empty">
              Opening your workspace…
            </div>
          ) : !session ? (
            <section className="welcome panel">
              <div className="empty-icon">▤</div>
              <h2>A clear view of your source records</h2>
              <p>
                Upload fictional patient records. We identify the patient and
                group their documents, with exact, stable source citations.
              </p>
              <button className="primary" disabled={busy} onClick={signIn}>
                {busy ? "Opening…" : "Enter development workspace →"}
              </button>
              <small>
                Development sign-in is shared. Production authentication is not
                enabled.
              </small>
            </section>
          ) : (
            <>
              {view === "sources" && (
                <ImportPanel
                  files={files}
                  busy={busy}
                  onFiles={(values) => {
                    setFiles(values);
                    retryImport.current = null;
                    setImportNotice("");
                  }}
                  onImport={() => void upload()}
                />
              )}
              {importNotice && (
                <div className="alert" role="status">
                  {importNotice}
                </div>
              )}
              {batches.some((batch) => batch.issues.length > 0) && (
                <details className="alert warning" open>
                  <summary>Files awaiting identity review</summary>
                  <p>
                    These files are saved separately and have not been attached
                    to a patient.
                  </p>
                  {batches
                    .flatMap((batch) => batch.issues)
                    .map((issue) => (
                      <p key={issue.id}>
                        <strong>{issue.filename}</strong>:{" "}
                        {issue.error_code === "conflicting_identifiers"
                          ? "Conflicting MRN or birth-date information. Review the source header before importing a corrected record."
                          : issue.error_code === "identity_unconfirmed"
                            ? "The record needs an explicit MRN and date of birth."
                            : issue.error_code.replaceAll("_", " ")}
                      </p>
                    ))}
                </details>
              )}
              {(patient || patients.length > 1) && (
                <section className="patient-bar panel">
                  <div className="patient-avatar">
                    {patient?.name
                      .split(" ")
                      .map((part) => part[0])
                      .slice(0, 2)
                      .join("") || "▤"}
                  </div>
                  <div className="patient-picker">
                    {patients.length > 1 ? (
                      <>
                        <label htmlFor="patient">PATIENT</label>
                        <select
                          id="patient"
                          value={patient?.id ?? ""}
                          disabled={busy}
                          onChange={(event) =>
                            setPatient(
                              patients.find(
                                (value) => value.id === event.target.value,
                              ) ?? null,
                            )
                          }
                        >
                          <option value="" disabled>
                            Select a patient
                          </option>
                          {patients.map((value) => (
                            <option key={value.id} value={value.id}>
                              {value.name} · {value.mrn}
                            </option>
                          ))}
                        </select>
                      </>
                    ) : (
                      <>
                        <span className="eyebrow">PATIENT DETECTED</span>
                        <strong>{patient?.name}</strong>
                      </>
                    )}
                    {patient && (
                      <small>
                        MRN {patient.mrn} <span>·</span> DOB{" "}
                        {patient.birth_date}
                      </small>
                    )}
                  </div>
                </section>
              )}
              {patient && view !== "sources" && (
                <ClinicalPanel
                  key={patient.id}
                  patientId={patient.id}
                  csrf={session.csrf_token}
                  snapshot={selectedSnapshot}
                  snapshots={snapshots}
                  onSnapshot={setSnapshotId}
                  view={view}
                  onSource={(revision, span) => {
                    setView("sources");
                    void openSource(revision, span);
                  }}
                />
              )}
              {!patient && view !== "sources" && (
                <div className="empty">
                  Select a patient with imported records to view their record
                  and ask questions.
                </div>
              )}
              {patient && view === "sources" && (
                <>
                  <div className="summary-grid">
                    <div className="panel summary">
                      <span>Source documents</span>
                      <strong>{selectedSnapshot?.manifest.length ?? 0}</strong>
                      <small>Immutable text revisions</small>
                    </div>
                    <div className="panel summary">
                      <span>Import activity</span>
                      <strong>
                        {activeJobs.length
                          ? `${activeJobs.length} active`
                          : "Up to date"}
                      </strong>
                      <small>
                        {jobs.length} import{jobs.length !== 1 ? "s" : ""} in
                        this workspace
                      </small>
                    </div>
                    <div className="panel summary">
                      <span>Clinical record</span>
                      <button
                        className="text-action"
                        onClick={() => setView("abstraction")}
                      >
                        Open record →
                      </button>
                      <small>Facts decided by code from quoted sources</small>
                    </div>
                  </div>
                  {activeJobs.length > 0 && (
                    <div className="alert" role="status">
                      Processing source records. You can close this page and
                      return later.
                    </div>
                  )}
                  {issues.length > 0 && (
                    <details className="alert warning">
                      <summary>
                        {issues.length} file
                        {issues.length !== 1 ? "s need" : " needs"} attention ·
                        source coverage is incomplete
                      </summary>
                      {issues.map((issue) => (
                        <p key={issue.id}>
                          {issue.filename}:{" "}
                          {issue.error_code === "identity_mismatch"
                            ? `The file’s MRN or date of birth does not match ${patient.name} (${patient.mrn}, ${patient.birth_date}). Choose the matching patient workspace and import it there.`
                            : (issue.error_code ?? issue.status).replaceAll(
                                "_",
                                " ",
                              )}
                        </p>
                      ))}
                    </details>
                  )}
                  <section className="panel library">
                    <div className="library-heading">
                      <div>
                        <h2>
                          Source library{" "}
                          <span className="count">{visibleDocs.length}</span>
                        </h2>
                        <p>Original records, preserved exactly as uploaded.</p>
                      </div>
                      <label className="snapshot-picker">
                        Source snapshot
                        <select
                          aria-label="Source snapshot"
                          value={snapshotId}
                          onChange={(event) => {
                            setSnapshotId(event.target.value);
                            setSource(null);
                            sourceRequest.current += 1;
                          }}
                        >
                          <option value="">
                            Latest
                            {snapshots[0] ? ` · v${snapshots[0].sequence}` : ""}
                          </option>
                          {snapshots.map((value) => (
                            <option value={value.id} key={value.id}>
                              v{value.sequence} · {value.manifest.length}{" "}
                              sources
                            </option>
                          ))}
                        </select>
                      </label>
                    </div>
                    {snapshotId && snapshotId !== snapshots[0]?.id && (
                      <div className="historical">
                        Viewing an older source snapshot. Newer imports are not
                        included.
                      </div>
                    )}
                    <div className="evidence-grid">
                      <div className="document-list">
                        <label className="search">
                          <span>⌕</span>
                          <input
                            aria-label="Filter sources"
                            value={query}
                            onChange={(event) => setQuery(event.target.value)}
                            placeholder="Find a source…"
                          />
                        </label>
                        <div className="document-scroll">
                          {visibleDocs.map((doc) => (
                            <button
                              className={`document ${source?.id === doc.id ? "selected" : ""}`}
                              key={doc.id}
                              onClick={() => void openSource(doc.id)}
                            >
                              <span className="doc-icon">TXT</span>
                              <span>
                                <strong>
                                  {doc.declared_id ?? "Text record"}
                                </strong>
                                <span className="filename">{doc.filename}</span>
                                <small>
                                  {doc.line_count} lines <span>·</span>{" "}
                                  {(doc.byte_count / 1024).toFixed(1)} KiB
                                </small>
                              </span>
                              <span className="chevron">›</span>
                            </button>
                          ))}
                          {!visibleDocs.length && (
                            <div className="empty small">
                              {query
                                ? "No sources match your search."
                                : "Your source records will appear here after import."}
                            </div>
                          )}
                        </div>
                        {viewingLatest && withdrawnDocs.length > 0 && (
                          <details className="withdrawn">
                            <summary>
                              Removed from case ({withdrawnDocs.length})
                            </summary>
                            {withdrawnDocs.map((doc) => (
                              <div className="withdrawn-row" key={doc.id}>
                                <button
                                  className="text-action"
                                  onClick={() => void openSource(doc.id)}
                                >
                                  {doc.declared_id ?? doc.filename}
                                </button>
                                <button
                                  className="text-action"
                                  disabled={busy}
                                  onClick={() =>
                                    void changeDocument(doc.id, "restore")
                                  }
                                >
                                  Restore
                                </button>
                              </div>
                            ))}
                          </details>
                        )}
                      </div>
                      <div className="source-viewer" aria-busy={loadingSource}>
                        {loadingSource ? (
                          <div className="empty" role="status">
                            Opening source…
                          </div>
                        ) : source ? (
                          <>
                            <div className="source-heading">
                              <div>
                                <span className="eyebrow">ORIGINAL SOURCE</span>
                                <h3>{source.declared_id ?? source.filename}</h3>
                                <p>{source.filename}</p>
                              </div>
                              <span className="verified">
                                {sourceWithdrawn
                                  ? "● Removed from case"
                                  : "● Preserved"}
                              </span>
                            </div>
                            {viewingLatest && !sourceWithdrawn && (
                              <div className="remove-source">
                                {removing ? (
                                  <form
                                    onSubmit={(event) => {
                                      event.preventDefault();
                                      void changeDocument(
                                        source.id,
                                        "withdraw",
                                        removeReason.trim(),
                                      );
                                    }}
                                  >
                                    <input
                                      aria-label="Reason for removal"
                                      placeholder="Reason (for example, filed to the wrong chart)"
                                      value={removeReason}
                                      maxLength={500}
                                      onChange={(event) =>
                                        setRemoveReason(event.target.value)
                                      }
                                    />
                                    <button
                                      disabled={busy || !removeReason.trim()}
                                    >
                                      Remove
                                    </button>
                                    <button
                                      type="button"
                                      className="text-action"
                                      onClick={() => setRemoving(false)}
                                    >
                                      Cancel
                                    </button>
                                  </form>
                                ) : (
                                  <button
                                    className="text-action"
                                    onClick={() => setRemoving(true)}
                                  >
                                    Remove from case…
                                  </button>
                                )}
                                <small>
                                  The original stays preserved for audit. A new
                                  source snapshot without it is published and
                                  its record rebuilt automatically; it can be
                                  restored later.
                                </small>
                              </div>
                            )}
                            <div className="source-meta">
                              <span>
                                SHA-256{" "}
                                <code title={source.sha256}>
                                  {source.sha256.slice(0, 16)}…
                                </code>
                              </span>
                              <span>{source.line_count} lines</span>
                            </div>
                            <label className="span-picker">
                              Inspect a source block
                              <select
                                aria-label="Source block"
                                value={spanId}
                                onChange={(event) =>
                                  setSpanId(event.target.value)
                                }
                              >
                                <option value="">All source lines</option>
                                {source.spans.map((span) => (
                                  <option key={span.id} value={span.id}>
                                    Lines {span.start_line}–{span.end_line}:{" "}
                                    {span.quote.slice(0, 70)}
                                  </option>
                                ))}
                              </select>
                            </label>
                            <div
                              className="source-lines"
                              tabIndex={0}
                              aria-label="Original source text"
                            >
                              {lines.map((line, i) => (
                                <div
                                  id={`line-${i + 1}`}
                                  key={i}
                                  className={`source-line ${highlighted && i + 1 >= highlighted.start_line && i + 1 <= highlighted.end_line ? "highlighted" : ""}`}
                                >
                                  <span
                                    className="line-number"
                                    aria-hidden="true"
                                  >
                                    {i + 1}
                                  </span>
                                  <span>{line || " "}</span>
                                </div>
                              ))}
                            </div>
                            {highlighted && (
                              <div className="citation-detail">
                                <strong>
                                  Stable citation · lines{" "}
                                  {highlighted.start_line}–
                                  {highlighted.end_line}
                                </strong>
                                <span>
                                  Character offsets [{highlighted.start_char},{" "}
                                  {highlighted.end_char})
                                </span>
                                <a
                                  href={`/api/v1/source-revisions/${source.id}/spans/${highlighted.id}`}
                                  target="_blank"
                                  rel="noreferrer"
                                >
                                  Open citation data ↗
                                </a>
                              </div>
                            )}
                            <div className="source-footer">
                              Blocks are structural text sections. Use the
                              Clinical record view to inspect the facts drawn
                              from them.
                            </div>
                          </>
                        ) : (
                          <div className="empty source-empty">
                            <div className="empty-icon">▤</div>
                            <h3>Follow the evidence</h3>
                            <p>
                              Select a record to inspect its original text,
                              <br />
                              line numbers, and exact source spans.
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  </section>
                  {jobs.length > 0 && (
                    <details className="panel import-history">
                      <summary>
                        Import history{" "}
                        <span className="count">{jobs.length}</span>
                      </summary>
                      {[...jobs]
                        .sort((a, b) =>
                          b.created_at.localeCompare(a.created_at),
                        )
                        .map((job) => (
                          <div key={job.id} className="job">
                            <div>
                              <strong>
                                {new Date(job.created_at).toLocaleString()}
                              </strong>
                              <span className="job-status">
                                {job.status === "succeeded"
                                  ? "Processing complete"
                                  : job.status}
                              </span>
                              {job.error_code && (
                                <span>
                                  {job.error_code.replaceAll("_", " ")}
                                </span>
                              )}
                            </div>
                            {job.uploads.map((file) => (
                              <div className="upload-row" key={file.id}>
                                <span>{file.filename}</span>
                                <span
                                  className={`upload-status ${file.status}`}
                                >
                                  {file.status}
                                </span>
                              </div>
                            ))}
                          </div>
                        ))}
                    </details>
                  )}
                </>
              )}
              <footer>
                Source-grounded by design <span>·</span> Extracted by Claude,
                reconciled by code; review before clinical use{" "}
                <button
                  onClick={async () => {
                    if (!session) return;
                    try {
                      await api<void>("/session", {
                        method: "DELETE",
                        headers: { "X-CSRF-Token": session.csrf_token },
                      });
                      setSession(null);
                      setPatient(null);
                      setPatients([]);
                    } catch (error) {
                      setError(message(error));
                    }
                  }}
                >
                  Sign out
                </button>
              </footer>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
