# GateBrief AI

> **Rules verify. Nemotron reasons. Tavily grounds. Humans decide.**

GateBrief AI is a human-in-the-loop aviation operations decision-support prototype for the **Nebius x NVIDIA Global AI Hackathon 2026**. It turns a structured flight folder into a concise readiness brief by combining deterministic validation, optional live research, and NVIDIA Nemotron reasoning through Nebius Token Factory.

## Why this project

Flight-operations information is often fragmented across confirmations, checklists, messages, and external sources. GateBrief demonstrates how an agentic workflow can detect missing or conflicting information, research current context when required, and prepare an action-oriented brief without pretending to replace authorized operational personnel.

> **Safety boundary:** GateBrief AI does not issue flight safety clearance, dispatch authority, or operational certification. All outputs require authorized human review.

## Architecture

```text
Flutter Web
    |
    v
FastAPI API
    |
    +--> Deterministic Rules Engine
    |
    +--> Tavily (conditional live research)
    |
    +--> Nebius Token Factory --> NVIDIA Nemotron
    |
    v
Readiness Brief + Findings + Sources + Human Review
```

## Repository structure

```text
backend/        FastAPI API, rules, Nebius and Tavily integrations
frontend/       Flutter web demo UI
docs/           Architecture, roadmap, Devpost draft, submission checklist
scripts/        Development utilities
```

## Quick start - backend

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` and try `GET /api/v1/demo`.

Without API keys, the app remains usable in deterministic demo mode. With `NEBIUS_API_KEY`, it calls Nebius Token Factory. With `TAVILY_API_KEY`, the demo can also perform live research.

## Configure Nebius

Create `backend/.env`:

```env
NEBIUS_API_KEY=your_key_here
NEBIUS_MODEL=
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1/
TAVILY_API_KEY=your_key_here
ENABLE_LIVE_RESEARCH=true
```

Do **not** commit `.env`.

If `NEBIUS_MODEL` is blank, GateBrief lists models available to the account and prefers an NVIDIA Nemotron model containing `super`, then another Nemotron model.

To inspect NVIDIA/Nemotron models manually:

```bash
export NEBIUS_API_KEY=your_key_here
python scripts/list_nebius_models.py
```

## Quick start - Flutter

Make sure Flutter is installed, then:

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

The starter frontend expects the backend at `http://127.0.0.1:8000`.

## Demo scenario

The included synthetic demo flight intentionally contains:
- a missing catering confirmation;
- a departure-time mismatch;
- a research query that can exercise Tavily when enabled.

No real passenger, airline, airport, or confidential operational data is included.

## Hackathon targets

Primary: **Apps & Agents**.
Secondary: **Best Use of Tavily**, if eligible under final sponsor rules.

## License

Apache-2.0. See `LICENSE`.
