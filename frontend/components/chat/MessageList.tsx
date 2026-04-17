import { useEffect, useRef } from "react";
import { MessageBubble, type Message } from "./MessageBubble";
import { DangerAlert } from "./DangerAlert";

interface MessageListProps {
  messages: Message[];
  dangerText: string | null;
}

export function MessageList({ messages, dangerText }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, dangerText]);

  return (
    <div className="flex-1 overflow-y-auto py-4 flex flex-col gap-3">
      {dangerText && <DangerAlert message={dangerText} />}
      {messages.map((msg, i) => (
        <MessageBubble key={i} message={msg} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
