"use client";

import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";
import remarkGfm from "remark-gfm";

export function MarkdownContent({ content }: { content: string }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}>
      {content || ""}
    </ReactMarkdown>
  );
}
