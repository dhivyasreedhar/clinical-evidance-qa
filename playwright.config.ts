import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/browser",
  timeout: 60_000,
  expect: { timeout: 20_000 },
  workers: 1,
  webServer: {
    command: ".venv/bin/python scripts/dev.py --browser-test",
    url: "http://localhost:3001/api/v1/ready",
    reuseExistingServer: false,
    timeout: 60_000,
    gracefulShutdown: { signal: "SIGTERM", timeout: 15_000 },
  },
  use: {
    baseURL: "http://localhost:3001",
    browserName: "chromium",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  reporter: "list",
});
