import { AlertTriangle } from "lucide-react";
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
      <AlertTriangle size={18} className="mt-0.5 shrink-0" />
      <p className="text-sm leading-relaxed font-medium">{message}</p>
    </div>
  );
}
