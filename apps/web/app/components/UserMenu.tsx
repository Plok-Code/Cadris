"use client";

import { useState, useRef, useEffect } from "react";
import { useSession, signOut } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function UserMenu() {
  const { data: session } = useSession();
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  // Close menu on outside click
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  if (!session?.user) return null;

  const initials = (session.user.name ?? session.user.email ?? "?")
    .split(" ")
    .map((w) => w[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  return (
    <div className="user-menu" ref={menuRef}>
      <button
        className="user-menu__trigger"
        onClick={() => setOpen(!open)}
        aria-label="Menu utilisateur"
      >
        {session.user.image ? (
          <img
            src={session.user.image}
            alt=""
            className="user-menu__avatar"
            referrerPolicy="no-referrer"
          />
        ) : (
          <span className="user-menu__initials">{initials}</span>
        )}
      </button>

      {open && (
        <div className="user-menu__dropdown">
          <div className="user-menu__info">
            <span className="user-menu__name">{session.user.name ?? "Utilisateur"}</span>
            <span className="user-menu__email">{session.user.email}</span>
          </div>
          <div className="user-menu__divider" />
          <button
            className="user-menu__item"
            onClick={() => {
              setOpen(false);
              router.push("/projects");
            }}
          >
            Mes projets
          </button>
          <button
            className="user-menu__item"
            onClick={() => {
              setOpen(false);
              router.push("/billing");
            }}
          >
            Abonnement
          </button>
          <button
            className="user-menu__item user-menu__item--danger"
            onClick={() => signOut({ callbackUrl: "/login" })}
          >
            Se déconnecter
          </button>
        </div>
      )}
    </div>
  );
}
