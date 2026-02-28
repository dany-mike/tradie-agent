import os

VAPI_BASE_URL = "https://api.vapi.ai"


def _headers() -> dict:
    api_key = os.environ["VAPI_API_KEY"]
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


# ---------------------------------------------------------------------------
# Assistants
# ---------------------------------------------------------------------------

def create_assistant(
    name: str,
    system_prompt: str,
    first_message: str,
    voice_provider: str = "elevenlabs",
    voice_id: str = "Bella",
    model_provider: str = "openai",
    model_id: str = "gpt-4o",
) -> dict:
    """Create a VAPI assistant and return the full assistant object (contains `id`)."""
    payload = {
        "name": name,
        "model": {
            "provider": model_provider,
            "model": model_id,
            "messages": [{"role": "system", "content": system_prompt}],
        },
        "voice": {
            "provider": voice_provider,
            "voiceId": voice_id,
        },
        "firstMessage": first_message,
        "firstMessageMode": "assistant-speaks-first",
    }
    resp = requests.post(f"{VAPI_BASE_URL}/assistant", headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()


def get_assistant(assistant_id: str) -> dict:
    """Fetch a single assistant by ID."""
    resp = requests.get(f"{VAPI_BASE_URL}/assistant/{assistant_id}", headers=_headers())
    resp.raise_for_status()
    return resp.json()


def list_assistants(limit: int = 100) -> list[dict]:
    """Return all assistants in the account."""
    resp = requests.get(
        f"{VAPI_BASE_URL}/assistant",
        headers=_headers(),
        params={"limit": limit},
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Calls
def make_call(
    phone_number: str,
    assistant_id: str,
) -> dict:
    return "this is a call"

def get_call(call_id: str) -> dict:
    """Fetch call details (status, transcript, recording, analysis) by call ID."""
    resp = requests.get(f"{VAPI_BASE_URL}/call/{call_id}", headers=_headers())
    resp.raise_for_status()
    return resp.json()
