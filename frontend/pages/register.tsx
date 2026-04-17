import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import { NavBar } from "@/components/shared/NavBar";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";
import { registerUser } from "@/lib/api";
import { colors } from "@/styles/tokens";

export default function Register() {
  const { user, isLoaded } = useUser();
  const router = useRouter();

  const [name, setName] = useState("");
  const [weeks, setWeeks] = useState("");
  const [language, setLanguage] = useState<"en" | "sw">("en");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Pre-fill name from Clerk if available
  useEffect(() => {
    if (user?.fullName) setName(user.fullName);
  }, [user]);

  // Redirect unauthenticated users
  useEffect(() => {
    if (isLoaded && !user) router.replace("/");
  }, [isLoaded, user, router]);

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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!user) return;
    setError(null);
    setSubmitting(true);

    const weeksNum = weeks ? parseInt(weeks, 10) : undefined;
    if (weeksNum !== undefined && (weeksNum < 1 || weeksNum > 42)) {
      setError("Gestational age must be between 1 and 42 weeks.");
      setSubmitting(false);
      return;
    }

    try {
      await registerUser({
        clerk_user_id: user.id,
        name: name.trim() || undefined,
        gestational_age_weeks: weeksNum,
        language,
      });
      router.push("/chat");
    } catch {
      setError("Something went wrong. Please try again.");
      setSubmitting(false);
    }
  }

  return (
    <div style={{ backgroundColor: colors.bg }} className="min-h-screen flex flex-col">
      <NavBar />

      <main className="flex-1 flex items-center justify-center px-4 py-12">
        <div
          style={{ backgroundColor: colors.white, borderColor: colors.divider }}
          className="w-full max-w-md rounded-2xl border shadow-sm p-8"
        >
          <h1 style={{ color: colors.sageDark }} className="text-2xl font-semibold mb-1">
            Set up your profile
          </h1>
          <p style={{ color: colors.gray }} className="text-sm mb-6">
            This helps Zeya give you trimester-appropriate advice.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            {/* Name */}
            <div className="flex flex-col gap-1">
              <label htmlFor="name" style={{ color: colors.mid }} className="text-sm font-medium">
                Your name <span style={{ color: colors.gray }}>(optional)</span>
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Amina"
                style={{ borderColor: colors.divider, outlineColor: colors.sage, color: colors.dark }}
              />
            </div>

            {/* Gestational age */}
            <div className="flex flex-col gap-1">
              <label htmlFor="weeks" style={{ color: colors.mid }} className="text-sm font-medium">
                Weeks pregnant <span style={{ color: colors.gray }}>(optional)</span>
              </label>
              <input
                id="weeks"
                type="number"
                min={1}
                max={42}
                value={weeks}
                onChange={(e) => setWeeks(e.target.value)}
                placeholder="e.g. 24"
                style={{ borderColor: colors.divider, outlineColor: colors.sage, color: colors.dark }}
                className="rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-offset-1"
              />
            </div>

            {/* Language */}
            <div className="flex flex-col gap-1">
              <span style={{ color: colors.mid }} className="text-sm font-medium">
                Preferred language
              </span>
              <div className="flex gap-3">
                {(["en", "sw"] as const).map((lang) => (
                  <button
                    key={lang}
                    type="button"
                    onClick={() => setLanguage(lang)}
                    style={{
                      backgroundColor: language === lang ? colors.sage : colors.white,
                      borderColor: language === lang ? colors.sage : colors.divider,
                      color: language === lang ? colors.white : colors.mid,
                    }}
                    className="flex-1 py-2 rounded-lg border text-sm font-medium transition-colors"
                  >
                    {lang === "en" ? "English" : "Kiswahili"}
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <p style={{ color: colors.danger }} className="text-sm">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={submitting}
              style={{ backgroundColor: submitting ? colors.sageLightMid : colors.sage }}
              className="mt-1 py-3 rounded-lg text-white font-medium text-sm transition-colors disabled:cursor-not-allowed"
            >
              {submitting ? "Saving…" : "Start chatting"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
