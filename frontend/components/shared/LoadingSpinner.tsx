import { colors } from "@/styles/tokens";

interface LoadingSpinnerProps {
  size?: number;
  label?: string;
}

export function LoadingSpinner({ size = 24, label = "Loading…" }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-2" role="status" aria-label={label}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        className="animate-spin"
        aria-hidden="true"
      >
        <circle
          cx="12"
          cy="12"
          r="10"
          stroke={colors.sageLightMid}
          strokeWidth="3"
        />
        <path
          d="M12 2a10 10 0 0 1 10 10"
          stroke={colors.sage}
          strokeWidth="3"
          strokeLinecap="round"
        />
      </svg>
      {label && (
        <span style={{ color: colors.gray }} className="text-sm">
          {label}
        </span>
      )}
    </div>
  );
}
