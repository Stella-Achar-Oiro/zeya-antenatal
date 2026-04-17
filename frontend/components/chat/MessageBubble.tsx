import ReactMarkdown from "react-markdown";
import { colors } from "@/styles/tokens";

export interface Message {
  role: "user" | "assistant";
  content: string;
  streaming?: boolean;
}

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} px-4`}>
      <div
        style={{
          backgroundColor: isUser ? colors.userBubble : colors.assistantBubble,
          color: isUser ? colors.userBubbleText : colors.assistantBubbleText,
          maxWidth: "75%",
        }}
        className="rounded-2xl px-4 py-3 text-sm leading-relaxed"
      >
        {isUser ? (
          <span>{message.content}</span>
        ) : (
          <div className={`prose prose-sm max-w-none ${message.streaming ? "streaming-cursor" : ""}`}>
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                strong: ({ children }) => (
                  <strong style={{ color: colors.sageDark }} className="font-semibold">
                    {children}
                  </strong>
                ),
                ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                li: ({ children }) => <li>{children}</li>,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
