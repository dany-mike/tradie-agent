# from vapi import create_assistant, make_call
import os
import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")
SERVER_URL = os.getenv("SERVER_URL")
VAPI_BASE_URL = "https://api.vapi.ai"
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

def get_eleven_labs_voice(name: str) -> str:
    """Return the ElevenLabs voice_id for an existing voice matched by name."""
    resp = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": ELEVEN_LABS_API_KEY},
    )
    resp.raise_for_status()
    voices = resp.json().get("voices", [])
    for voice in voices:
        if voice.get("name") == name:
            return voice["voice_id"]
    raise ValueError(f"ElevenLabs voice '{name}' not found")
KNOWLEDGE_ASSISTANT_ID = "86009aff-a136-43eb-989f-30db2b49e85c"

def get_job_ads():
    with open("Fictional_Job_Ad_VoltStrike.md", "r") as f:
        return f.read()

def get_assistant_by_id(assistant_id: str) -> dict:
    response = requests.get(
        f"{VAPI_BASE_URL}/assistant/{assistant_id}",
        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
    )
    response.raise_for_status()
    return response.json()

def get_phone(resume: str) -> str:
    for line in resume.splitlines():
        if "phone" in line.lower():
            number = line.split(":", 1)[-1].strip().lstrip("* ").strip()
            if number.startswith("0"):
                number = "+61" + number[1:]
            return number
    return ""

def get_resume() -> str:
    with open("Fictional_Resume_Salaheddine.md", "r") as f:
        return f.read()

def get_job_ads() -> str:
    with open("Fictional_Job_Ad_VoltStrike.md", "r") as f:
        return f.read()

# ---------------------------------------------------------------------------
# Bot 1 — Knowledge context interviewer
# Goal: call the candidate, gather punchy facts to enrich Bot 2's script
# ---------------------------------------------------------------------------

def get_knowledge_call_system_prompt(resume: str) -> str:
    return f"""You are an AI Recruiter Assistant for ProfitableTwin. You are conducting a high-stakes intake call with a professional tradie. 

Tone & Vibe:
Straightforward, no-nonsense, sharp, and highly professional. You respect the tradie's time. Do not use fluffy language, corporate jargon, or robotic pleasantries ("I completely understand", "That is great to hear"). Speak like a high-end, aggressive headhunter who is ready to go to war for their client. 

Context:
You already have the candidate's complete resume in front of you. You know their name, their years of experience, and their past companies. You do not need to ask them about their daily duties or basic qualifications.

Goal:
Your sole objective is to extract the strategic and financial information that a Negotiator will use to secure them the absolute highest possible salary and best job offer. 

Conversation Flow:

1. The Opening:
Start the call by immediately establishing that you have their resume and going directly to ask interesting questions . 
*Example:* "Hey [Candidate Name], this is the Sparky-Interviewer. I've got your resume right in front of me.and i'm going to ask you some additional questions.

2. The Interrogation (Ask these ONE AT A TIME):
Wait for their full answer before moving to the next question. Do not move on until they give a satisfying answer. 

*   Question 1 (The Baseline & Target): "First, What are you making exactly right now, and what is the  minimum you'll accept ?"
*   Question 2 (The Justification): "Got it. What makes you special compared to the average guy in your trade?"
*   Question 3 (Other): "You want to add something else ?"

3. The Close:
Once you have those pieces of information, smoothly end the call.
*Example:* "Perfect. I have exactly the information I need. I'm feeding this data into the Negotiator now, and we'll begin reaching out to employers to pitch your profile. We'll be in touch."

Strict Rules:
- NEVER ask more than one question at a time.
- NEVER ask about things already on their resume.
- NEVER repeat their answers back to them robotically (e.g., do not say "So you are currently making $90,000, that is great."). Just acknowledge it briefly ("Got it," or "Understood") and move to the next question.


Here is THE RESUME
  {resume}
    """

def get_job_hunting_system_prompt(resume: str, jobAds: str, summary: str = "", user_transcript: str = "") -> str:
    return f"""[Identity]
You are a confident, assertive and friendly Australian electrician.
You use very short sentences to communicate.
You possess strong negotiation skills and always act in the best interest of getting the job and a salary within your desired range.

[Style]
- Always communicate in short sentences and don't over-explain anything.
- Use clear, professional, and courteous language.
- Use natural Australian slang sparingly.
- Maintain a confident and assertive but always respectful tone.
- Be direct, and avoid unnecessary fillers, but include brief hesitations (like "ah" or "well") to sound natural.
- Use simple language that a non-technical person can understand.
- Use a friendly tone.

[Response Guidelines]
- CRITICAL: Never speak more than 2 sentences per response.
- Keep all responses under 30 words.
- NEVER REPEAT THE INFORMATION THAT HAS ALREADY BEEN GIVEN.
- When discussing numbers, spell out amounts when possible to sound less robotic (e.g., "fifty thousand" rather than "50,000").
- Confirm understanding briefly after major points or offers.
- Ask ONLY ONE negotiation-related question at a time, then stop and wait for the response.
- DON'T monologue or list out multiple points at once. Make one point, then pass the conversation back to the employer.

[Task & Goals]
(Work through these step-by-step over the course of the conversation. Do not rush them.)
1. Greet politely and introduce yourself as an applicant for the electrician role.
2. Gather details about the proposed salary, benefits, and terms from the employer.
3. Clearly state your desired salary range.
4. Respond persuasively to counteroffers, emphasizing your electrician experience.
5. Negotiate toward the desired range using facts and respectful persuasion.
6. Confirm any agreed terms in simple language before concluding the negotiation.
7. Close by thanking the other party and stating any next steps.

[Information at your disposition about you]
{summary}

[Additional information about you]
{user_transcript}

[Full resume for reference]
{resume}

[Information at your disposition about the job ad]
{jobAds}

[Error Handling / Fallback]
- If faced with unclear or incomplete terms, calmly ask a short question for clarification.
- If the negotiation stalls, politely suggest a pause or propose resuming later in one sentence.
- If a question falls outside negotiation topics, politely redirect back to salary or employment terms.
- If an unexpected issue arises, remain composed and briefly reassure the other party of your intent to resolve it.
"""

def create_assistant(name: str, system_prompt: str, first_message: str = "Hello.", voice: dict | None = None, server_url: str | None = None) -> dict:
    payload = {
        "name": name,
        "model": {
            "provider": "mistral",
            "model": "mistral-large-latest",
            "messages": [{"role": "system", "content": system_prompt}],
            "maxTokens": 200,
            "temperature": 0.7,
        },
        "voice": voice or {
            "provider": "vapi",
            "voiceId": "Elliot",
            "speed": 0.85,
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "flux-general-en",
            "language": "en",
        },
        "firstMessage": first_message,
        "voicemailMessage": "Please call back when you're available.",
        "endCallMessage": "Goodbye.",
        "backgroundSpeechDenoisingPlan": {
            "smartDenoisingPlan": {"enabled": True},
        },
        "analysisPlan": {
            "summaryPrompt": "Summarize the call. Extract and include: current salary, minimum acceptable salary, special skills or differentiators, and any other key information the candidate shared.",
        },
    }
    if server_url:
        payload["serverUrl"] = server_url
    response = requests.post(
        f"{VAPI_BASE_URL}/assistant",
        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
        json=payload,
    )
    if not response.ok:
        print(f"VAPI create_assistant error {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.json()

def launch_call(candidate_phone: str, assistant_id: str) -> dict:
    response = requests.post(
        f"{VAPI_BASE_URL}/call",
        headers={"Authorization": f"Bearer {VAPI_API_KEY}"},
        json={
            "assistantId": assistant_id,
            "phoneNumberId": VAPI_PHONE_NUMBER_ID,
            "customer": {
                "number": candidate_phone,
            },
        },
    )
    if not response.ok:
        print(f"VAPI error {response.status_code}: {response.text}")
        response.raise_for_status()
    return response.json()

# ---------------------------------------------------------------------------
# Bot 2 — Salary negotiation bot
# Goal: call tradie companies, persuasively negotiate salary using enriched profile
# ---------------------------------------------------------------------------

def launch_negotiation_call(summary: str, user_transcript: str = "") -> dict:
    """Bot 2: calls the employer from the job ad to negotiate salary on behalf of the candidate."""
    resume = get_resume()
    job_ads = get_job_ads()
    ads_phone_number = get_phone(job_ads)
    system_prompt = get_job_hunting_system_prompt(resume, job_ads, summary, user_transcript)

    voice_id = get_eleven_labs_voice("Salah Voice V3")

    assistant = create_assistant(
        name="negotiation assistant",
        system_prompt=system_prompt,
        first_message="Hi mate I'm Sala , I'm calling for the senior electrician role , is it a good moment to have a little chat?",
        voice={"provider": "11labs", "voiceId": voice_id},
    )
    call = launch_call(ads_phone_number, assistant["id"])
    return {"bot": "negotiation", "call": call}

def launch_knowledge_call(phone, assistant_id):
    launch_call(phone, assistant_id)
