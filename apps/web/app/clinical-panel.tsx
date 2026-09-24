"use client";

import { useEffect, useRef, useState } from "react";
import { api, type Snapshot } from "@/lib/api";
import type { components } from "@/lib/api-schema";
import { DocumentList, RecordSummary } from "./record-view";
import { Sources, human, type OnSource } from "./evidence-views";

type Run = components["schemas"]["RunOut"];
type RunDetail = components["schemas"]["RunDetail"];
type ModelStatus = components["schemas"]["ModelStatusOut"];
type View = "abstraction" | "ask" | "documents";

// Only statements the reader must weigh differently are labelled.
const LABELS: Record<string, string> = {
  conflict: "Sources disagree",
  missing: "Not documented",
  inference: "Inference",
};

const active = (run: Run) => ["queued", "running"].includes(run.status);

export function ClinicalPanel({
  patientId,
  csrf,
  snapshot,
  snapshots,
  onSnapshot,
  view,
  onSource,
}: {
  patientId: string;
  csrf: string;
  snapshot: Snapshot | undefined;
  snapshots: Snapshot[];
  onSnapshot: (id: string) => void;
  view: View;
  onSource: OnSource;
}) {
  const [runs, setRuns] = useState<Run[]>([]);
  const [details, setDetails] = useState<Record<string, RunDetail>>({});
  const [model, setModel] = useState<ModelStatus | null>(null);
  const [question, setQuestion] = useState("");
  const [error, setError] = useState("");
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  const retry = useRef<{ signature: string; key: string } | null>(null);
  const loadedVersion = useRef("");

  useEffect(() => {
    let disposed = false;
    let timer: ReturnType<typeof setTimeout>;
    loadedVersion.current = "";
    const poll = async () => {
      try {
        // Poll a small change marker; download runs only when something changed.
        const { version } = await api<{ version: string }>(
          `/patients/${patientId}/runs/version`,
        );
        if (version !== loadedVersion.current) {
          const [values, status] = await Promise.all([
            api<Run[]>(`/patients/${patientId}/runs`),
            api<ModelStatus>("/model-status"),
          ]);
          if (!disposed) {
            loadedVersion.current = version;
            setRuns(values);
            setModel(status);
          }
        }
        if (!disposed) setLoading(false);
      } catch (e) {
        if (!disposed) {
          setError(e instanceof Error ? e.message : "Unable to load runs");
          setLoading(false);
        }
      }
      if (!disposed) timer = setTimeout(poll, 2500);
    };
    void poll();
    return () => {
      disposed = true;
      clearTimeout(timer);
    };
  }, [patientId]);

  const matching = runs.filter((run) => run.snapshot_id === snapshot?.id);
  const built = matching.filter(
    (run) => run.kind === "engine_record" && run.status === "succeeded",
  );
  // a record built by the current engine version; an older one is shown only until it is rebuilt
  const record =
    built.find((run) => run.prompt_version === model?.engine_version) ??
    built[0];
  const outdated =
    !!record && !!model && record.prompt_version !== model.engine_version;
  const latestBuild = matching.find((run) => run.kind === "engine_record");
  const answers = matching.filter(
    (run) => run.kind === "engine_answer" && run.record_id === record?.id,
  );
  const running = runs.find(active);

  // Download each finished run's result once; results never change.
  useEffect(() => {
    const wanted = [record, ...answers].filter(
      (run): run is Run =>
        !!run && run.status === "succeeded" && !details[run.id],
    );
    for (const run of wanted) {
      void api<RunDetail>(`/patients/${patientId}/runs/${run.id}`)
        .then((detail) =>
          setDetails((current) => ({ ...current, [run.id]: detail })),
        )
        .catch((e) =>
          setError(e instanceof Error ? e.message : "Unable to load result"),
        );
    }
  }, [runs, snapshot?.id]);

  async function submit(kind: "records" | "answers") {
    if (!snapshot || (kind === "answers" && (!question.trim() || !record)))
      return;
    setSending(true);
    setError("");
    const payload =
      kind === "records"
        ? { snapshot_id: snapshot.id }
        : { record_id: record!.id, question: question.trim() };
    const signature = JSON.stringify(payload);
    if (retry.current?.signature !== signature)
      retry.current = { signature, key: crypto.randomUUID() };
    try {
      const run = await api<Run>(`/patients/${patientId}/${kind}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrf,
          "Idempotency-Key": retry.current.key,
        },
        body: signature,
      });
      setRuns((current) => [
        run,
        ...current.filter((value) => value.id !== run.id),
      ]);
      retry.current = null;
      if (kind === "answers") setQuestion("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to start");
    } finally {
      setSending(false);
    }
  }

  const view_ = record ? details[record.id]?.record : undefined;

  return (
    <section className="panel clinical-panel">
      <div className="clinical-heading">
        <div>
          <span className="eyebrow">RECORD ENGINE · SOURCE-LINKED</span>
          <h2>
            {view === "documents"
              ? "Documents"
              : view === "abstraction"
                ? "Clinical record"
                : "Ask the record"}
          </h2>
          <p>
            {view === "documents"
              ? "What each document is, who issued it, the service dates it supports, and whether it is a copy or was set aside."
              : view === "abstraction"
                ? "Encounters, weekly goal results and every fact, decided by code from quoted source observations."
                : "Ask a question about this patient's record. Every figure comes from a query over the record."}
          </p>
        </div>
        <label className="snapshot-picker">
          Source snapshot
          <select
            aria-label="Source snapshot"
            value={snapshot?.id ?? ""}
            onChange={(event) => onSnapshot(event.target.value)}
          >
            {snapshots.map((value) => (
              <option key={value.id} value={value.id}>
                v{value.sequence} · {value.manifest.length} sources
              </option>
            ))}
          </select>
        </label>
      </div>
      {error && (
        <div className="alert error" role="alert">
          {error}
        </div>
      )}
      {snapshot && snapshot.id !== snapshots[0]?.id && (
        <div className="alert warning">
          Historical snapshot. Newer imports are not included.
        </div>
      )}
      {model && !model.configured && (
        <div className="alert warning">
          Claude is not configured. Add EHR_ANTHROPIC_API_KEY to the server’s
          .env file and restart the services.
        </div>
      )}
      {view !== "ask" && (
        <div className="analysis-actions">
          <span>{model?.model ?? "Checking Claude configuration…"}</span>
          {record && (
            <>
              <a
                className="button"
                href={`/api/v1/patients/${patientId}/records/${record.id}/export`}
              >
                Download record (JSON)
              </a>
              <a
                className="button"
                href={`/api/v1/patients/${patientId}/records/${record.id}/export?format=markdown`}
              >
                Download abstraction
              </a>
            </>
          )}
          <button
            className="primary"
            disabled={
              loading || !model?.configured || !snapshot || !!running || sending
            }
            onClick={() => void submit("records")}
          >
            {sending ? "Starting…" : record ? "Rebuild record" : "Build record"}
          </button>
        </div>
      )}
      {running && (
        <div className="alert" role="status">
          {running.kind === "engine_record"
            ? "Extracting observations and reconciling the record"
            : "Preparing a cited answer"}{" "}
          · {running.status}.
          {running.kind === "engine_record" &&
            " Unchanged documents reuse their cached extraction."}{" "}
          You can leave this page and return later.
        </div>
      )}
      {outdated && (
        <div className="alert warning">
          This record was built by an earlier engine version, so questions are
          not answered over it.{" "}
          {running
            ? "It is being rebuilt now."
            : "Rebuild it to use the current engine."}
        </div>
      )}
      {latestBuild?.status === "failed" && (
        <div className="alert warning">
          The record build failed: {human(latestBuild.error_code ?? "failed")}.
          Correct the issue, then build again.
        </div>
      )}
      {!record ? (
        <div className="empty">
          <h3>
            {loading
              ? "Loading…"
              : running
                ? "The record is being built"
                : "Sources are ready"}
          </h3>
          <p>
            Build the record to review encounters and facts and to ask
            questions. This sends the selected fictional records to Anthropic.
          </p>
        </div>
      ) : !view_ ? (
        <div className="empty">
          <h3>Loading the record…</h3>
        </div>
      ) : view === "abstraction" ? (
        <RecordSummary view={view_} onSource={onSource} />
      ) : view === "documents" ? (
        <DocumentList view={view_} onSource={(id) => onSource(id, "")} />
      ) : (
        <>
          <form
            className="question-form"
            onSubmit={(event) => {
              event.preventDefault();
              void submit("answers");
            }}
          >
            <label htmlFor="clinical-question">Your question</label>
            <textarea
              id="clinical-question"
              rows={3}
              maxLength={2000}
              placeholder="What changed over the review period? Which treatment time is uncertain?"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
            />
            <div className="question-examples">
              {[
                "How many sessions, days, and minutes of care are documented?",
                "Were the documented weekly treatment goals met?",
                "Summarize changes in symptoms and functioning.",
              ].map((value) => (
                <button
                  type="button"
                  key={value}
                  onClick={() => setQuestion(value)}
                >
                  {value}
                </button>
              ))}
            </div>
            <button
              className="primary"
              disabled={
                !question.trim() || !!running || sending || !model?.configured
              }
            >
              Ask
            </button>
          </form>
          <div className="answer-history">
            {answers.map((run) => {
              const answer = details[run.id]?.answer;
              return (
                <article className="answer-card" key={run.id}>
                  <span className="eyebrow">
                    {new Date(run.created_at).toLocaleString()} ·{" "}
                    {answer?.status ?? run.status}
                  </span>
                  <h3>{run.question}</h3>
                  {run.error_code && (
                    <p className="alert warning">{human(run.error_code)}</p>
                  )}
                  {active(run) && <p role="status">Preparing answer…</p>}
                  {answer?.status === "withheld" && (
                    <div className="alert warning">
                      The answer did not pass its checks, so it was not
                      published.
                      <ul>
                        {answer.reasons.map((reason, index) => (
                          <li key={index}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {answer?.status === "partial" && (
                    <p className="alert warning">
                      Partial answer: some parts of the question are not
                      covered.
                    </p>
                  )}
                  {answer?.statements.map((statement, index) => (
                    <div className="finding" key={index}>
                      {LABELS[statement.kind] && (
                        <span className="eyebrow">
                          {LABELS[statement.kind]}
                        </span>
                      )}
                      <p>{statement.text}</p>
                      <Sources
                        citations={statement.citations}
                        onSource={onSource}
                      />
                    </div>
                  ))}
                  {!!answer?.omitted?.length && (
                    <details className="answer-more">
                      <summary>
                        Other details from the record ({answer.omitted.length})
                      </summary>
                      {answer.omitted.map((statement, index) => (
                        <div className="finding" key={index}>
                          <p>{statement.text}</p>
                          <Sources
                            citations={statement.citations}
                            onSource={onSource}
                          />
                        </div>
                      ))}
                    </details>
                  )}
                </article>
              );
            })}
          </div>
        </>
      )}
      {record && (
        <div className="analysis-provenance">
          {record.model} · {record.prompt_version} · {record.schema_version} ·{" "}
          {new Date(record.created_at).toLocaleString()}
          {record.usage &&
            ` · ${record.usage.calls} model calls (${record.usage.cached_calls} cached) · $${record.usage.cost_usd.toFixed(2)}`}
        </div>
      )}
    </section>
  );
}
