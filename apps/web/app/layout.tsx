import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Clinical Evidence | Source workspace",
  description: "An inspectable workspace for source-grounded clinical records.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
