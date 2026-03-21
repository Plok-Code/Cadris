"use client";

import { useEffect, useState } from "react";

export function ClientDateTime({ value }: { value: string }) {
  const [formatted, setFormatted] = useState("...");

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- sync initialization from props
    setFormatted(
      new Intl.DateTimeFormat("fr-FR", {
        dateStyle: "short",
        timeStyle: "short"
      }).format(new Date(value))
    );
  }, [value]);

  return <span suppressHydrationWarning>{formatted}</span>;
}
