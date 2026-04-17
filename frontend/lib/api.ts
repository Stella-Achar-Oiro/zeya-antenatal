/**
 * API client — one function per backend endpoint.
 * No inline fetch calls anywhere else in the codebase.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface RegisterPayload {
  clerk_user_id: string;
  name?: string;
  gestational_age_weeks?: number;
  language?: "en" | "sw";
}

export interface RegisterResponse {
  clerk_user_id: string;
  registered: boolean;
}

export interface ChatPayload {
  message: string;
  clerk_user_id: string;
  language?: "en" | "sw";
}

/**
 * Register or update a user's antenatal profile.
 *
 * @param payload - Registration data including Clerk user ID and optional profile fields.
 * @returns The server confirmation with registered flag.
 * @throws Error if the request fails.
 */
export async function registerUser(payload: RegisterPayload): Promise<RegisterResponse> {
  const res = await fetch(`${API_URL}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Registration failed: ${res.status}`);
  }
  return res.json();
}

/**
 * Open a streaming SSE connection to the chat endpoint.
 * Returns the raw Response so the caller can read the stream.
 *
 * @param payload - Chat request with message and clerk_user_id.
 * @returns Raw fetch Response with Content-Type text/event-stream.
 * @throws Error if the request cannot be initiated.
 */
export async function streamChat(payload: ChatPayload): Promise<Response> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }
  return res;
}
