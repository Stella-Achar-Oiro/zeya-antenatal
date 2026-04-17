import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/nextjs";
import Image from "next/image";
import Link from "next/link";
import { colors } from "@/styles/tokens";

export function NavBar() {
  return (
    <nav
      style={{ backgroundColor: colors.sage }}
      className="flex items-center justify-between px-6 py-3 shadow-sm"
    >
      <Link href="/" className="flex items-center gap-2.5">
        <Image src="/logo.svg" alt="Zeya logo" width={28} height={28} priority />
        <span className="text-xl font-semibold text-white tracking-wide">
          Zeya Antenatal
        </span>
      </Link>

      <div className="flex items-center gap-4">
        <SignedOut>
          <SignInButton mode="modal">
            <button
              style={{ backgroundColor: colors.sageDark }}
              className="px-4 py-1.5 rounded-md text-sm text-white hover:opacity-90 transition-opacity"
            >
              Sign in
            </button>
          </SignInButton>
        </SignedOut>
        <SignedIn>
          <Link
            href="/chat"
            className="text-sm text-white opacity-80 hover:opacity-100 transition-opacity"
          >
            Chat
          </Link>
          <UserButton />
        </SignedIn>
      </div>
    </nav>
  );
}
