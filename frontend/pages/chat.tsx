import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/router";
import { useState, useEffect, useCallback } from "react";
import { Leaf } from "lucide-react";
import { NavBar } from "@/components/shared/NavBar";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";
import { MessageList } from "@/components/chat/MessageList";
import { ChatInput } from "@/components/chat/ChatInput";
import { streamChat } from "@/lib/api";
import { colors } from "@/styles/tokens";
import type { Message } from "@/components/chat/MessageBubble";

export default function Chat() {
  const { user, isLoaded } = useUser();
  const router = useRouter();

  const [messages, setMessages] = useState<Message[]>([]);
  const [dangerText, setDangerText] = useState<string | null>(null);
  const [streaming, setStreaming] = useState(false);
  const [language] = useState<"en" | "sw">("en");

  useEffect(() => {
    if (isLoaded && !user) router.replace("/");
  }, [isLoaded, user, router]);

  const sendMessage = useCallback(
    async (text: string) => {
      if (!user || streaming) return;

      setMessages((prev) => [...prev, { role: "user", content: text }]);
      setDangerText(null);
      setStreaming(true);

      const assistantIndex = messages.length + 1;
      setMessages((prev) => [...prev, { role: "assistant", content: "", streaming: true }]);

      try {
        const res = await streamChat({
          message: text,
          clerk_user_id: user.id,
          language,
        });

        const reader = res.body?.getReader();
        if (!reader) throw new Error("No stream body");

        const decoder = new TextDecoder();
        let buffer = "";
        let accum = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? "";

          for (const line of lines) {
            if (!line.startsWith("data: ")) continue;
            const raw = line.slice(6).trim();
            if (raw === "[DONE]") continue;

            let token: string;
            try {
              token = JSON.parse(raw).token ?? "";
            } catch {
              continue;
            }

            // Backend prefixes danger-sign emergency responses with 🚨
            if (token.startsWith("🚨")) {
              setDangerText(token);
              accum = "";
            } else {
              accum += token;
              setMessages((prev) => {
                const next = [...prev];
                next[assistantIndex] = { role: "assistant", content: accum, streaming: true };
                return next;
              });
            }
          }
        }

        setMessages((prev) => {
          const next = [...prev];
          if (next[assistantIndex]) {
            next[assistantIndex] = { role: "assistant", content: accum, streaming: false };
          }
          return next;
        });
      } catch (err) {
        console.error("Stream error", err);
        setMessages((prev) => {
          const next = [...prev];
          next[assistantIndex] = {
            role: "assistant",
            content: "Sorry, something went wrong. Please try again.",
            streaming: false,
          };
          return next;
        });
      } finally {
        setStreaming(false);
      }
    },
    [user, streaming, messages.length, language]
  );

  if (!isLoaded || !user) {
    return (
      <div style={{ backgroundColor: colors.bg }} className="min-h-screen flex flex-col">
        <NavBar />
        <div className="flex-1 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <div style={{ backgroundColor: colors.bg }} className="min-h-screen flex flex-col">
      <NavBar />

      <div className="flex-1 flex flex-col max-w-2xl w-full mx-auto">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-3 text-center px-6">
            <Leaf size={36} style={{ color: colors.sage }} />
            <p style={{ color: colors.mid }} className="font-medium">
              Hi{user.firstName ? `, ${user.firstName}` : ""}! I&apos;m Zeya.
            </p>
            <p style={{ color: colors.gray }} className="text-sm max-w-sm">
              Ask me anything about your pregnancy — nutrition, symptoms, what to expect,
              or when to seek care.
            </p>
          </div>
        ) : (
          <MessageList messages={messages} dangerText={dangerText} />
        )}

        <ChatInput onSend={sendMessage} disabled={streaming} />
      </div>
    </div>
  );
}
