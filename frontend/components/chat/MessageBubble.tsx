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
        <span className={message.streaming ? "streaming-cursor" : ""}>
          {message.content}
        </span>
      </div>
    </div>
  );
}
