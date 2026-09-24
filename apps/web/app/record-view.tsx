"use client";
import { useState } from "react";
import type { components } from "@/lib/api-schema";
import {
  Sources,
  Status,
  display,
  either,
  type OnSource,
} from "./evidence-views";

type RecordView = components["schemas"]["RecordView"];
type Week = components["schemas"]["WeekRow"];

const week = (value: Week) => {
  const [start, end] = value.week.split("..");
  return end ? `${start} – ${end}` : value.week;
};

export function RecordSummary({
  view,
  onSource,
}: {
  view: RecordView;
  onSource: OnSource;
}) {
  const totals = view.totals;
  return (
    <>
      <section className="calculation">
        <div className="section-title">
          <h3>Care delivered</h3>
          <span className="verified">Computed by code</span>
        </div>
        <p className="muted-text">
          Included encounters of the services the documented care goal counts.
          Where sources disagree, every possibility is kept.
        </p>
        <div className="summary-grid">
          <div className="summary">
            <span>Sessions</span>
            <strong>{totals?.sessions ?? "—"}</strong>
          </div>
          <div className="summary">
            <span>Distinct treatment days</span>
            <strong>{totals?.days ?? "—"}</strong>
          </div>
          <div className="summary">
            <span>Treatment time</span>
            <strong>{totals ? either(totals.minutes, " min") : "—"}</strong>
          </div>
        </div>
        {view.weeks.length > 0 && (
          <table className="breakdown">
            <caption>Weekly goal</caption>
            <thead>
              <tr>
                <th>Week</th>
                <th>Sessions</th>
                <th>Days</th>
                <th>Minutes</th>
                <th>Goal</th>
              </tr>
            </thead>
            <tbody>
              {view.weeks.map((row) => (
                <tr key={row.week}>
                  <td>
                    {week(row)}
                    {row.partial && (
                      <span className="muted-text"> · partial week</span>
                    )}
                  </td>
                  <td>{row.sessions ?? "—"}</td>
                  <td>{row.days ?? "—"}</td>
                  <td>{either(row.minutes)}</td>
                  <td>
                    <Status value={row.goal} />
                    {(row.thresholds ?? []).map((t) => (
                      <div key={t.threshold} className="muted-text">
                        {t.threshold}: {either(t.measured)} (
                        {t.outcome.replaceAll("_", " ")})
                      </div>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section>
        <div className="section-title">
          <h3>Encounters</h3>
        </div>
        <table className="breakdown">
          <thead>
            <tr>
              <th>Encounter</th>
              <th>Date</th>
              <th>Service</th>
              <th>Counted</th>
              <th>Minutes</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {view.encounters.map((row) => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>
                  {row.date ?? "—"}
                  {row.weekday && (
                    <div className="muted-text">{row.weekday}</div>
                  )}
                </td>
                <td>
                  {row.service ?? "—"}
                  {row.attendance && (
                    <div className="muted-text">{row.attendance}</div>
                  )}
                </td>
                <td>
                  {row.disposition?.replaceAll("_", " ") ?? "—"}
                  {row.reason && <div className="muted-text">{row.reason}</div>}
                </td>
                <td>{either(row.minutes)}</td>
                <td>
                  <Status value={row.status} />
                  <Sources citations={row.citations} onSource={onSource} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {view.open_items.length > 0 && (
        <section>
          <div className="section-title">
            <h3>Needs review ({view.open_items.length})</h3>
          </div>
          <div className="clinical-findings">
            {view.open_items.map((item, index) => (
              <article key={index} className="finding">
                <span className="eyebrow">
                  {item.kind.replaceAll("_", " ")}
                  {item.subject ? ` · ${item.subject}` : ""}
                </span>
                <p>{item.text}</p>
                <Sources citations={item.citations} onSource={onSource} />
              </article>
            ))}
          </div>
        </section>
      )}

      <details className="encounter-ledger">
        <summary>
          Every fact ({view.events.length} events shown, {view.facts_total}{" "}
          facts in the record)
        </summary>
        {view.events.map((event) => (
          <table className="breakdown" key={event.id}>
            <caption>
              {event.id} · {event.kind}
            </caption>
            <tbody>
              {event.facts.map((fact) => (
                <tr key={fact.field}>
                  <th>{fact.field.replaceAll("_", " ")}</th>
                  <td>
                    {either(fact.values)}
                    {fact.reason && (
                      <div className="muted-text">{fact.reason}</div>
                    )}
                  </td>
                  <td>
                    <Status value={fact.status} />
                    <Sources citations={fact.citations} onSource={onSource} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ))}
      </details>

      <Findings view={view} onSource={onSource} />
    </>
  );
}

function Findings({
  view,
  onSource,
}: {
  view: RecordView;
  onSource: OnSource;
}) {
  const [filter, setFilter] = useState("");
  const shown = view.findings.filter((finding) =>
    `${display(finding.text)} ${finding.type ?? ""} ${finding.date ?? ""}`
      .toLowerCase()
      .includes(filter.trim().toLowerCase()),
  );
  return (
    <details className="encounter-ledger">
      <summary>Clinical findings by date ({view.findings.length})</summary>
      <input
        className="ledger-search"
        aria-label="Filter findings"
        placeholder="Filter by word, type or date"
        value={filter}
        onChange={(event) => setFilter(event.target.value)}
      />
      <div className="clinical-findings">
        {shown.map((finding) => (
          <article key={finding.id} className="finding">
            <span className="eyebrow">
              {finding.date ?? "Undated"}
              {finding.type ? ` · ${finding.type}` : ""}
              {finding.reporter ? ` · ${finding.reporter}` : ""}
            </span>
            <p>{display(finding.text)}</p>
            <Sources citations={finding.citations} onSource={onSource} />
          </article>
        ))}
      </div>
    </details>
  );
}

export function DocumentList({
  view,
  onSource,
}: {
  view: RecordView;
  onSource: (revision: string) => void;
}) {
  return (
    <table className="breakdown">
      <thead>
        <tr>
          <th>Document</th>
          <th>Issuer</th>
          <th>Service dates</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        {view.documents.map((document) => (
          <tr key={document.key}>
            <td>
              {document.revision_id ? (
                <button
                  className="link-button"
                  onClick={() => onSource(document.revision_id!)}
                >
                  {document.title ?? document.filename}
                </button>
              ) : (
                (document.title ?? document.filename)
              )}
              <div className="muted-text">{document.filename}</div>
            </td>
            <td>{document.issuer ?? "—"}</td>
            <td>{document.service_dates.join(", ") || "—"}</td>
            <td>
              {document.set_aside
                ? `Set aside: ${document.set_aside}`
                : document.copy_of
                  ? `Copy of ${document.copy_of}`
                  : "Source"}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
