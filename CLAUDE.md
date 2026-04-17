# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## What This Is

**Zeya Antenatal** is an AI-powered antenatal education chatbot providing maternal health
guidance to pregnant women in English and Swahili. Built as the Week 1 project for the
"AI in Production" course. Not a medical device — educational information only.

## Guardrails — Read Before Touching Any File

| Rule | What it means in practice |
|---|---|
| **Design doc before code** | Write a plan in `docs/plans/` before implementing any feature. |
| **`enums.py` is the source of truth** | All domain string values (language, danger categories) defined there. Never raw string literals in model fields. |
| **All prompts in `templates.py`** | No prompt strings in `ai_engine.py`, `chat.py`, or anywhere else. |
| **No inline fetch in components** | All API calls go through `frontend/lib/api.ts`. One function per endpoint. |
| **Tokens file for all colours** | Hex values only in `frontend/styles/tokens.ts`. Never hardcoded in components. |
| **150-line hard cap** | No component or module file exceeds 150 lines. Split before hitting the limit. |
| **No emojis** | Never in code, comments, UI copy, or docs. SVG icons or text labels only. |
| **Services not routers** | Business logic lives in `backend/app/services/`. Routers do validation + delegation only. |
| **Tests/unit for pure logic** | Danger sign detection, prompt building, gestational age calculation — unit tested with no HTTP. |

## Commands

```bash
make install    # uv sync (backend) + npm install (frontend)
make dev        # both servers — Ctrl+C kills both
make dev-api    # FastAPI only on :8000
make dev-ui     # Next.js only on :3000
make test       # pytest (backend)
make lint       # ruff + mypy (backend)
```

## Locked Decisions

| Decision | Choice |
|---|---|
| Backend | Python 3.12, FastAPI, uv |
| Frontend | Next.js 14 Pages Router, TypeScript, Tailwind CSS v3 |
| AI | OpenAI `gpt-4o-mini`, streaming via SSE |
| Auth | Clerk `@clerk/nextjs@6.x` — pin to 6.x, v7 removed `SignedIn`/`SignedOut` |
| Session memory | In-memory dict, clerk_user_id as key, last 6 turns |
| Danger signs | Regex detection (8 categories, EN + SW) before every AI call |
| Prompts | All in `backend/app/services/templates.py` |
| Deployment | Vercel (frontend) + Docker/ECR/App Runner (backend) |

## Architecture

```
frontend (Next.js Pages Router)
  pages/index.tsx          — public landing
  pages/chat.tsx           — protected chat (Clerk)
  components/chat/         — page-specific components (MessageList, ChatInput, etc.)
  components/shared/       — NavBar, LoadingSpinner (2+ pages)
  lib/api.ts               — all fetch calls, one function per endpoint
  styles/tokens.ts         — design tokens

backend (FastAPI)
  app/factory.py           — create_app() + lifespan
  app/api/health.py        — GET /api/health
  app/api/chat.py          — POST /api/chat (SSE)
  app/api/register.py      — POST /api/register
  app/services/
    ai_engine.py           — OpenAI call + tool loop + streaming
    danger_signs.py        — regex detection, EN + SW
    templates.py           — all prompts
    memory.py              — in-memory conversation store
  app/models/              — Pydantic models only
  app/enums.py             — Language, DangerCategory
```

## React / Next.js Rules

- Named exports for all components; default export for page files only
- Page files: orchestration only — data fetch + component composition, max 80 lines
- Page-specific components under `components/<feature>/` (e.g. `components/chat/`)
- Shared components (2+ pages) under `components/shared/`
- JSDoc block required on every exported component and every helper function
- Props destructured in function signature — never `props.x` in body
- Three import groups: third-party → internal → CSS; one blank line between groups
- Do not import React unless `React` namespace is explicitly used

## Frontend Component Contracts

- `NavBar` — takes `user` prop (Clerk user object or null)
- `MessageBubble` — takes `role: "user" | "assistant"`, `content: string`
- `DangerAlert` — takes `categories: string[]`, shown when danger signs detected
- `ChatInput` — takes `onSend: (message: string) => void`, `disabled: boolean`

## Out of Scope

- WhatsApp integration
- PostgreSQL or Redis
- Admin dashboard
- Voice input
- Push notifications
- Tablet / desktop-optimised layouts (mobile-first only in Phase 1)
