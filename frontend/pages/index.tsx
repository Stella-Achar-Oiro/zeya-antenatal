import { SignedIn, SignedOut, SignInButton } from "@clerk/nextjs";
import { useRouter } from "next/router";
import { NavBar } from "@/components/shared/NavBar";
import { colors } from "@/styles/tokens";

export default function Home() {
  const router = useRouter();

  return (
    <div style={{ backgroundColor: colors.bg }} className="min-h-screen flex flex-col">
      <NavBar />

      <main className="flex-1 flex flex-col items-center justify-center px-6 text-center">
        <div className="max-w-xl">
          <h1 style={{ color: colors.sageDark }} className="text-4xl font-semibold mb-4 leading-tight">
            Your pregnancy companion, in your language
          </h1>
          <p style={{ color: colors.gray }} className="text-lg mb-8 leading-relaxed">
            Zeya answers your antenatal questions in English or Swahili, alerts you to
            danger signs, and supports you from first trimester through delivery.
          </p>

          <SignedOut>
            <SignInButton mode="modal">
              <button
                style={{ backgroundColor: colors.sage }}
                className="px-8 py-3 rounded-lg text-white text-base font-medium hover:opacity-90 transition-opacity shadow-sm"
              >
                Get started — it&apos;s free
              </button>
            </SignInButton>
          </SignedOut>

          <SignedIn>
            <button
              style={{ backgroundColor: colors.sage }}
              className="px-8 py-3 rounded-lg text-white text-base font-medium hover:opacity-90 transition-opacity shadow-sm"
              onClick={() => router.push("/chat")}
            >
              Go to chat
            </button>
          </SignedIn>
        </div>

        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-2xl w-full text-left">
          {FEATURES.map(({ icon, title, body }) => (
            <div
              key={title}
              style={{ backgroundColor: colors.sageLight, borderColor: colors.sageLightMid }}
              className="rounded-xl border p-5"
            >
              <div className="text-2xl mb-2">{icon}</div>
              <h3 style={{ color: colors.sageDark }} className="font-semibold mb-1">
                {title}
              </h3>
              <p style={{ color: colors.gray }} className="text-sm leading-relaxed">
                {body}
              </p>
            </div>
          ))}
        </div>
      </main>

      <footer
        style={{ borderColor: colors.divider, color: colors.gray }}
        className="border-t py-4 text-center text-sm"
      >
        Zeya Antenatal — maternal health support · not a substitute for medical advice
      </footer>
    </div>
  );
}

const FEATURES = [
  {
    icon: "🌿",
    title: "Safe pregnancy guidance",
    body: "Evidence-based answers on nutrition, symptoms, and what to expect each trimester.",
  },
  {
    icon: "🚨",
    title: "Danger sign alerts",
    body: "Instantly recognises warning signs and directs you to emergency care.",
  },
  {
    icon: "🗣️",
    title: "English & Swahili",
    body: "Chat in the language you're most comfortable with — switch any time.",
  },
];
