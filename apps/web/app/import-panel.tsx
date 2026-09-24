"use client";

export function ImportPanel({
  files,
  busy,
  onFiles,
  onImport,
}: {
  files: File[];
  busy: boolean;
  onFiles: (files: File[]) => void;
  onImport: () => void;
}) {
  return (
    <>
      <section className="panel import-panel">
        <div className="import-icon">↥</div>
        <div>
          <h2>Upload your records</h2>
          <p>We detect the patient and group matching records automatically.</p>
          <p>UTF-8 TXT · 10 MiB per file · 25 MiB per import · 100 files</p>
        </div>
        <label className="secondary file-button">
          Choose files
          <input
            aria-label="Choose source files"
            type="file"
            accept=".txt,text/plain"
            multiple
            disabled={busy}
            onChange={(event) => {
              onFiles(Array.from(event.target.files ?? []));
              event.target.value = "";
            }}
          />
        </label>
        <button
          className="primary"
          disabled={!files.length || busy}
          onClick={onImport}
        >
          {busy
            ? "Importing…"
            : files.length
              ? `Import ${files.length} file${files.length > 1 ? "s" : ""}`
              : "Import records"}
        </button>
      </section>
      {files.length > 0 && (
        <div className="file-preview">
          Ready to import: {files.map((file) => file.name).join(", ")}
        </div>
      )}
    </>
  );
}
