/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // NEXT_PUBLIC_API_URL is set at build time; defaults to localhost for local dev.
  // NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is required — set in .env.local or Vercel env.
};

export default nextConfig;
