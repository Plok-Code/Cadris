import type { Metadata } from "next";
import { IBM_Plex_Mono, Public_Sans } from "next/font/google";
import "./globals.css";
import SessionWrapper from "./components/SessionWrapper";
import UserMenu from "./components/UserMenu";
import { validateEnv } from "../src/lib/envCheck";

validateEnv();

const publicSans = Public_Sans({
  subsets: ["latin"],
  variable: "--font-sans"
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono"
});

export const metadata: Metadata = {
  title: "Cadris",
  description: "Le chainon manquant du vibe coding. Cadrez votre projet avant de coder."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body className={`${publicSans.variable} ${ibmPlexMono.variable}`}>
        <SessionWrapper>
          <header className="app-header">
            <a href="/" className="app-header__logo" aria-label="Cadris — Accueil">
              <img src="/cadris-favicon.svg" alt="" className="app-header__logo-symbol" width={26} height={26} />
              <span className="app-header__logo-wordmark">CADRIS</span>
            </a>
            <UserMenu />
          </header>
          {children}
        </SessionWrapper>
      </body>
    </html>
  );
}
