import { test, expect } from "@playwright/test";

test("upload detects patients, routes independently of the open case, retains review issues and citations", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await page
    .getByRole("button", { name: "Enter development workspace" })
    .click();
  await expect(
    page.getByRole("button", { name: "Create workspace" }),
  ).toHaveCount(0);
  await expect(
    page.getByRole("combobox", { name: "PATIENT", exact: true }),
  ).toHaveCount(0);
  const mrn = `BROWSER-${Date.now()}`;
  const file = {
    name: "original.txt",
    mimeType: "text/plain",
    buffer: Buffer.from(
      `Document ID: BROWSER-SOURCE\r\nPatient: Example Patient | MRN: ${mrn} | DOB: 1985-03-04\r\n\r\nOriginal quotation 🧪.\r\n`,
    ),
  };
  async function importFile(value: typeof file) {
    await page.getByLabel("Choose source files").setInputFiles(value);
    await page
      .getByRole("button", { name: "Import 1 file", exact: true })
      .click();
  }
  await importFile(file);
  await expect(page.getByText(`MRN ${mrn}`, { exact: false })).toBeVisible();
  await expect(
    page.getByRole("combobox", { name: "PATIENT", exact: true }),
  ).toHaveCount(0);
  const patientId = new URL(page.url()).searchParams.get("patient")!;
  await page.getByRole("button", { name: /TXT BROWSER-SOURCE/ }).click();
  await expect(page.getByLabel("Original source text")).toContainText(
    "Original quotation 🧪.",
  );
  await page.getByLabel("Source block").selectOption({ index: 2 });
  const citationUrl = await page
    .getByRole("link", { name: "Open citation data" })
    .getAttribute("href");
  const citation = await page.request.get(citationUrl!);
  expect((await citation.json()).quote).toBe("Original quotation 🧪.");
  await importFile(file);
  await page.getByText("Import history", { exact: false }).click();
  await expect(page.getByText("duplicate", { exact: true })).toBeVisible();
  const other = {
    name: "other.txt",
    mimeType: "text/plain",
    buffer: Buffer.from(
      `Document ID: SECOND-SOURCE\nPatient: Another Patient | MRN: ${mrn}-OTHER | DOB: 1970-01-01\n\nSecond source.`,
    ),
  };
  await importFile(other);
  await expect(
    page.getByText(`MRN ${mrn}-OTHER`, { exact: false }),
  ).toBeVisible();
  await expect(
    page.getByRole("combobox", { name: "PATIENT", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: /TXT SECOND-SOURCE/ }).click();
  await importFile(file);
  await expect(
    page.getByRole("combobox", { name: "PATIENT", exact: true }),
  ).toHaveValue(patientId);
  await page.reload();
  await expect(
    page.getByRole("combobox", { name: "PATIENT", exact: true }),
  ).toHaveValue(patientId);
  await expect(
    page.getByRole("button", { name: /TXT BROWSER-SOURCE/ }),
  ).toHaveCount(1);
  const conflict = {
    ...file,
    name: "conflict.txt",
    buffer: Buffer.from(
      file.buffer.toString().replace("1985-03-04", "1986-03-04"),
    ),
  };
  await importFile(conflict);
  await expect(page.getByText("Files awaiting identity review")).toBeVisible();
  await expect(
    page.getByText(/Conflicting MRN or birth-date information/),
  ).toBeVisible();
  await page.reload();
  await expect(page.getByText("Files awaiting identity review")).toBeVisible();
  await page
    .getByRole("button", { name: "Clinical record", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Clinical record", exact: true }),
  ).toBeVisible();
  await expect(page.getByText(/Claude is not configured/)).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Build record" }),
  ).toBeDisabled();
  await page
    .getByRole("button", { name: "Ask a question", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Ask the record" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Source library", exact: true })
    .click();
  await page.getByRole("button", { name: /TXT BROWSER-SOURCE/ }).click();
  await page.screenshot({
    path: ".local/screenshots/automatic-import.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await page
    .getByRole("button", { name: "Clinical record", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Clinical record", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Ask a question", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Ask the record", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  expect(errors).toEqual([]);
});
