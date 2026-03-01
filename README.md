# A Profitable Digital Twin

> Mistral AI Hackathon Project

An autonomous AI system that handles job application calls on behalf of a candidate. It runs two sequential AI voice bots via [Vapi](https://vapi.ai):

1. **Bot 1 — Interviewer**: Calls the candidate to extract salary expectations and key differentiators.
2. **Bot 2 — Negotiator**: Calls the employer from the job ad and negotiates the best salary using the data gathered from Bot 1.

## Architecture

```
Browser (index.html)
    │  POST /launch/  (resume file)
    ▼
FastAPI (main.py :8000)
    │  creates Vapi assistant + launches call
    ▼
Vapi API ──► calls candidate (Bot 1)
    │  POST /webhook  (end-of-call-report)
    ▼
FastAPI webhook handler
    │  launches negotiation call (Bot 2)
    ▼
Vapi API ──► calls employer (Bot 2)
    │  POST /webhook  (end-of-call-report)
    ▼
status = "scenario_ended"
```

The webhook is p$ublicly exposed via **ngrok**.

## Prerequisites

- Python 3.10+
- [ngrok](https://ngrok.com) installed and authenticated
- API keys in `.env` (see below)

## Environment Variables

Create a `.env` file at the project root:

```env
MISTRAL_API_KEY=your_mistral_key
VAPI_API_KEY=your_vapi_key
VAPI_PHONE_NUMBER_ID=your_vapi_phone_number_id
SERVER_URL=https://your-ngrok-domain.ngrok-free.dev
ELEVEN_LABS_API_KEY=your_elevenlabs_key
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Project

> **Order matters:** start ngrok first so the tunnel is live before Vapi tries to reach the webhook.

**Terminal 1 — ngrok tunnel:**
```bash
ngrok http --url=your-ngrok-domain.ngrok-free.dev 8000
```

**Terminal 2 — FastAPI server:**
```bash
uvicorn main:app --reload --port 8000
```

The UI is available at [http://localhost:8000](http://localhost:8000).

## Usage

1. Open [http://localhost:8000](http://localhost:8000) in your browser.
2. Upload a candidate resume (`.md`, `.txt`, `.pdf`, `.doc`, `.docx`).
3. Click **Launch**.
4. The UI polls `/status` every 2 seconds and shows the current state:
   - `call_in_progress` — Bot 1 is interviewing the candidate
   - `waiting_for_negotiation` — Bot 2 is negotiating with the employer
   - `scenario_ended` — Full scenario complete

## Project Structure

```
hackathon-project/
├── main.py                        # FastAPI app, routes, webhook handler
├── domain.py                      # Vapi & ElevenLabs helpers, system prompts
├── index.html                     # Frontend UI (Alpine.js)
├── assets/                        # Static assets (logo, etc.)
├── Fictional_Resume_Salaheddine.md   # Sample candidate resume
├── Fictional_Job_Ad_VoltStrike.md    # Sample job ad (employer to call)
├── requirements.txt
└── .env                           # API keys (not committed)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serve frontend |
| `GET` | `/status` | Current call state |
| `POST` | `/launch/` | Upload resume and start the scenario |
| `POST` | `/webhook` | Vapi end-of-call callback |
