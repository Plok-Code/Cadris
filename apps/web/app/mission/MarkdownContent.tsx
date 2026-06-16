"use client";

import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

// XSS defense: rehype-sanitize strips dangerous tags/attributes from the
// rendered markdown. A second layer (Content-Security-Policy) is enforced at
// the reverse proxy (deploy/Caddyfile) in production. Keep rehypeSanitize on
// any path that renders agent- or user-derived markdown.
export function MarkdownContent({ content }: { content: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
      {content || ""}
    </ReactMarkdown>
  );
}
