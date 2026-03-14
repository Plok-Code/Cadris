"use client";

import { useEffect, useState } from "react";

export function ClientDateTime({ value }: { value: string }) {
  const [formatted, setFormatted] = useState("...");

  useEffect(() => {
    setFormatted(
      new Intl.DateTimeFormat("fr-FR", {
        dateStyle: "short",
        timeStyle: "short"
      }).format(new Date(value))
    );
  }, [value]);

  return <span suppressHydrationWarning>{formatted}</span>;
}
