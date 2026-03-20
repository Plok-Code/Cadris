"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface AppShellProps {
  heading: string;
  description: string;
  eyebrow: string;
  breadcrumbs?: BreadcrumbItem[];
  children: ReactNode;
}

export function AppShell({ heading, description, eyebrow, breadcrumbs, children }: AppShellProps) {
  const pathname = usePathname();

  return (
    <div className="app-shell">
      <div className="app-shell__inner">
        <nav className="top-nav">
          <div className="top-nav__brand">
            <div className="top-nav__symbol">C</div>
            <div>
              <div className="top-nav__title">CADRIS.AI</div>
              <div className="top-nav__subtitle">Mission documentaire multi-agents</div>
            </div>
          </div>
          <div className="top-nav__links">
            <NavLink href="/mission" isActive={pathname === "/mission"}>
              Nouveau cadrage
            </NavLink>
            <NavLink href="/projects" isActive={pathname.startsWith("/projects") || pathname.startsWith("/dossiers")}>
              Mes projets
            </NavLink>
          </div>
        </nav>

        <header className="panel panel--accent">
          {breadcrumbs && breadcrumbs.length > 0 && (
            <nav className="breadcrumb" aria-label="Navigation">
              {breadcrumbs.map((item, i) => (
                <span key={i}>
                  {i > 0 && <span className="breadcrumb__separator" aria-hidden="true">/</span>}
                  {item.href ? (
                    <Link className="breadcrumb__link" href={item.href}>{item.label}</Link>
                  ) : (
                    <span className="breadcrumb__current" aria-current="page">{item.label}</span>
                  )}
                </span>
              ))}
            </nav>
          )}
          <div className="section-heading">
            <div className="section-eyebrow">{eyebrow}</div>
            <h1 className="section-title">{heading}</h1>
            <p className="section-description">{description}</p>
          </div>
        </header>

        {children}
      </div>
    </div>
  );
}

function NavLink({
  href,
  isActive,
  children
}: {
  href: string;
  isActive: boolean;
  children: ReactNode;
}) {
  return (
    <Link className={`top-nav__link ${isActive ? "top-nav__link--active" : ""}`} href={href}>
      {children}
    </Link>
  );
}

