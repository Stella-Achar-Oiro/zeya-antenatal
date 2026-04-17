# Zeya Antenatal

An AI-powered maternal health chatbot that answers antenatal questions in English and Swahili, detects danger signs, and streams responses in real time.

Built as a Week 1 project for the [AI in Production](https://github.com/ed-donner/production) course.

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (Pages Router), TypeScript, Tailwind CSS, Clerk v6 |
| Backend | FastAPI, Python 3.12, OpenAI `gpt-4o-mini` |
| Auth | Clerk |
| Package manager | `uv` (backend), `npm` (frontend) |
| Deployment | Vercel (frontend) · AWS App Runner via Docker (backend) |

---

## Local development

### Prerequisites

- Python 3.12+, [`uv`](https://docs.astral.sh/uv/)
- Node.js 18+, npm
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Clerk](https://clerk.com) application (free tier works)

### 1. Clone and install

```bash
git clone https://github.com/Stella-Achar-Oiro/zeya-antenatal.git
cd zeya-antenatal
make install
```

### 2. Configure environment variables

**Backend**

```bash
cp backend/.env.example backend/.env
# Fill in: OPENAI_API_KEY, CORS_ORIGINS
```

**Frontend**

```bash
cp frontend/.env.local.example frontend/.env.local
# Fill in: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY
```

### 3. Run

```bash
make dev          # starts both servers (Ctrl+C stops both)
# or separately:
make dev-api      # FastAPI on :8000
make dev-ui       # Next.js on :3000
```

Open [http://localhost:3000](http://localhost:3000).

### Tests and linting

```bash
make test         # pytest (17 tests, asyncio)
make lint         # ruff + mypy
```

---

## Architecture

```
browser → Next.js (Vercel)
              │  POST /api/register
              │  POST /api/chat  ←── Server-Sent Events stream
              ▼
         FastAPI (App Runner)
              │
              ├── danger_signs.py   regex scan before every AI call
              ├── ai_engine.py      OpenAI tool-call loop + word-chunked SSE
              ├── memory.py         in-memory history (6 turns, 24 h TTL)
              └── templates.py      system prompt + trimester guidance
```

**Request flow**

1. User sends a message from `/chat`.
2. Backend scans for 8 danger-sign categories (English + Swahili regex).
3. If a danger sign is found, an emergency response is streamed immediately.
4. Otherwise, the message goes to `gpt-4o-mini` with a system prompt that includes the user's trimester and language preference.
5. The model may call the `record_unanswered_question` tool before answering.
6. Tokens are streamed back as SSE events; the frontend appends them to the active bubble in real time.

---

## Project structure

```
zeya-antenatal/
├── backend/
│   ├── app/
│   │   ├── api/          health, register, chat endpoints
│   │   ├── models/       Pydantic request/response models
│   │   ├── services/     ai_engine, danger_signs, memory, templates
│   │   ├── enums.py      Language, DangerCategory
│   │   └── factory.py    FastAPI app factory + CORS
│   └── tests/
│       ├── unit/         danger sign detection (12 tests)
│       └── integration/  health, register, (chat covered manually)
├── frontend/
│   ├── components/
│   │   ├── chat/         MessageList, MessageBubble, ChatInput, DangerAlert
│   │   └── shared/       NavBar, LoadingSpinner
│   ├── lib/api.ts        all fetch calls (registerUser, streamChat)
│   ├── pages/            index, register, chat, _app, _document
│   └── styles/           tokens.ts (design tokens), globals.css
└── docs/plans/           design documents
```

---

## Danger sign detection

The backend detects the following categories before every AI call:

| Category | Example trigger |
|---|---|
| Vaginal bleeding | "I'm bleeding heavily" |
| Severe headache | "pounding headache and blurred vision" |
| Reduced fetal movement | "I haven't felt the baby move" |
| Water breaking | "my water broke" |
| Convulsions | "I had a seizure" |
| Severe swelling | "my face and hands are swollen" |
| Difficulty breathing | "I can't catch my breath" |
| Severe abdominal pain | "sharp pain in my stomach" |

All categories match in both English and Swahili.

---

## Deployment

See the course Day 5 guide for full deployment instructions.

**Frontend → Vercel**

Set these environment variables in the Vercel dashboard:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
- `CLERK_SECRET_KEY`
- `NEXT_PUBLIC_API_URL` (your App Runner URL)

**Backend → AWS App Runner**

```bash
# Build for linux/amd64 (required for App Runner on Apple Silicon)
docker build --platform linux/amd64 -t zeya-antenatal-api ./backend

# Push to ECR then deploy via App Runner console or CLI
```

Required environment variables on App Runner:
- `OPENAI_API_KEY`
- `CORS_ORIGINS` (your Vercel deployment URL)
