import { colors } from "@/styles/tokens";

interface DangerAlertProps {
  message: string;
}

export function DangerAlert({ message }: DangerAlertProps) {
  return (
    <div
      role="alert"
      style={{ backgroundColor: colors.dangerBg, borderColor: colors.danger, color: colors.danger }}
      className="flex items-start gap-3 rounded-xl border p-4 mx-4 my-2"
    >
      <span className="text-xl leading-none mt-0.5" aria-hidden>🚨</span>
      <p className="text-sm leading-relaxed font-medium">{message}</p>
    </div>
  );
}
