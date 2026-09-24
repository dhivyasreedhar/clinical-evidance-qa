import { test, expect } from "@playwright/test";

test("record view shows code-computed results with source links, documents and cited answers", async ({
  page,
}) => {
  const text = "Individual session 09:00–09:50. Signed by A. Example.";
  const source = {
    id: "revision",
    filename: "contact.txt",
    declared_id: "TEST-DOC",
    sha256: "hash",
    line_count: 1,
    byte_count: text.length,
    created_at: "2026-09-23T01:00:00Z",
    text,
    spans: [
      {
        id: "span",
        start_char: 0,
        end_char: text.length,
        start_line: 1,
        end_line: 1,
        quote: text,
      },
    ],
  };
  const citation = {
    span_id: "span",
    revision_id: "revision",
    filename: source.filename,
    start_line: 1,
    end_line: 1,
    quote: text,
  };
  const base = {
    snapshot_id: "snapshot",
    status: "succeeded",
    error_code: null,
    model: "fixture",
    prompt_version: "engine",
    schema_version: "policy",
    created_at: source.created_at,
    usage: {
      model: "fixture",
      input_tokens: 10,
      output_tokens: 5,
      cost_usd: 0.01,
      calls: 2,
      cached_calls: 1,
    },
  };
  const record = {
    ...base,
    id: "record",
    kind: "engine_record",
    record_id: null,
    question: null,
  };
  const answer = {
    ...base,
    id: "answer",
    kind: "engine_answer",
    record_id: "record",
    question: "How long was the session?",
  };
  const week = {
    week: "2026-01-05..2026-01-11",
    partial: false,
    sessions: 1,
    days: 1,
    minutes: [40, 50],
  };
  const view = {
    events_total: 2,
    facts_total: 3,
    encounters: [
      {
        id: "E1",
        date: "2026-01-05",
        weekday: "Monday",
        service: "individual",
        attendance: "attended",
        disposition: "included",
        minutes: [40, 50],
        status: "conflicting",
        reason: null,
        citations: [citation],
      },
    ],
    weeks: [
      {
        ...week,
        goal: "cannot_determine",
        thresholds: [
          {
            threshold: "at least 45 minutes",
            measured: null,
            outcome: "cannot_determine",
          },
        ],
      },
    ],
    totals: week,
    events: [
      {
        id: "E1",
        kind: "encounter",
        facts: [
          {
            field: "minutes",
            values: [40, 50],
            status: "conflicting",
            reason: "Sources of equal standing disagree.",
            citations: [citation],
          },
        ],
      },
    ],
    findings: [
      {
        id: "F1",
        date: "2026-01-05",
        type: "symptom",
        reporter: "clinician",
        text: "Sleep improved.",
        status: "documented",
        citations: [citation],
      },
    ],
    documents: [
      {
        key: "contact",
        revision_id: "revision",
        filename: source.filename,
        title: "Individual therapy note",
        issuer: "Example clinic",
        copy_of: null,
        set_aside: null,
        service_dates: ["2026-01-05"],
      },
    ],
    open_items: [
      {
        kind: "conflict",
        subject: "E1",
        text: "E1 minutes: 40 or 50.",
        citations: [citation],
      },
    ],
  };
  await page.route("**/api/v1/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let json: unknown = [];
    if (path.endsWith("/session"))
      json = {
        actor_id: "actor",
        csrf_token: "fixture",
        mode: "synthetic_development",
      };
    else if (path.endsWith("/patients"))
      json = [
        {
          id: "patient",
          name: "Fictional Example",
          mrn: "TEST",
          birth_date: "1980-01-01",
        },
      ];
    else if (path.endsWith("/snapshots"))
      json = [
        {
          id: "snapshot",
          sequence: 1,
          manifest: [{ revision_id: "revision", sha256: "hash" }],
          created_at: source.created_at,
          manifest_hash: "hash",
        },
      ];
    else if (path.endsWith("/documents")) json = [source];
    else if (path.endsWith("/runs/version")) json = { version: "fixture" };
    else if (path.endsWith("/runs")) json = [answer, record];
    else if (path.endsWith("/runs/record"))
      json = { ...record, record: view, answer: null };
    else if (path.endsWith("/runs/answer"))
      json = {
        ...answer,
        record: null,
        answer: {
          status: "answered",
          statements: [
            {
              text: "The session lasted 40 or 50 minutes; the sources disagree.",
              kind: "conflict",
              citations: [citation],
            },
          ],
          reasons: [],
        },
      };
    else if (path.endsWith("/model-status"))
      json = { configured: false, model: "fixture", engine_version: "engine" };
    else if (path.endsWith("/source-revisions/revision")) json = source;
    await route.fulfill({ json });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Clinical record", exact: true })
    .click();
  const panel = page.locator(".clinical-panel");
  await expect(panel).toContainText("40 or 50 min");
  await expect(panel).toContainText("cannot determine");
  await expect(panel).toContainText("E1 minutes: 40 or 50.");
  await expect(
    panel.getByRole("link", { name: "Download record (JSON)" }),
  ).toHaveAttribute("href", /records\/record\/export$/);
  await panel.getByText("Clinical findings by date (1)").click();
  await expect(panel).toContainText("Sleep improved.");
  await page.getByRole("button", { name: "Documents", exact: true }).click();
  await expect(panel).toContainText("Individual therapy note");
  await expect(panel).toContainText("Example clinic");
  await page
    .getByRole("button", { name: "Ask a question", exact: true })
    .click();
  await expect(panel).toContainText("How long was the session?");
  await expect(panel).toContainText("the sources disagree");
  await panel.getByRole("button", { name: /contact · L1/ }).click();
  await expect(page.getByText(text).first()).toBeVisible();
  await page.setViewportSize({ width: 390, height: 844 });
  await page
    .getByRole("button", { name: "Clinical record", exact: true })
    .click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});
