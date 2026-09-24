import type { NextConfig } from "next";

const config: NextConfig = {
  distDir:
    process.env.EHR_BROWSER_TEST === "1" ? ".next-browser-test" : ".next",
  poweredByHeader: false,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.EHR_BROWSER_TEST === "1"
            ? "http://127.0.0.1:8009/api/:path*"
            : "http://127.0.0.1:8008/api/:path*",
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "same-origin" },
          { key: "X-Frame-Options", value: "DENY" },
        ],
      },
    ];
  },
};
export default config;
