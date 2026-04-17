import { useRef } from "react";
import { colors } from "@/styles/tokens";

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const ref = useRef<HTMLTextAreaElement>(null);

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function submit() {
    const text = ref.current?.value.trim();
    if (!text || disabled) return;
    onSend(text);
    if (ref.current) ref.current.value = "";
  }

  return (
    <div
      style={{ borderColor: colors.divider, backgroundColor: colors.white }}
      className="border-t px-4 py-3 flex items-end gap-2"
    >
      <textarea
        ref={ref}
        rows={1}
        disabled={disabled}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question…"
        style={{ borderColor: colors.divider, outlineColor: colors.sage, color: colors.dark }}
        className="flex-1 resize-none rounded-xl border px-3 py-2 text-sm leading-relaxed outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50"
      />
      <button
        onClick={submit}
        disabled={disabled}
        style={{ backgroundColor: disabled ? colors.sageLightMid : colors.sage }}
        className="rounded-xl px-4 py-2 text-white text-sm font-medium transition-colors disabled:cursor-not-allowed"
      >
        Send
      </button>
    </div>
  );
}
