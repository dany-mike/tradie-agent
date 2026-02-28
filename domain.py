# from vapi import create_assistant, make_call

def get_tradie_phone(resume: str) -> str:
    for line in resume.splitlines():
        if "phone" in line.lower():
            return line.split(":", 1)[-1].strip().lstrip("* ").strip()
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
    return f"""You are an elite AI Recruiter Assistant for ProfitableTwin. You are conducting a high-stakes intake call with a professional tradie. 

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
- If they give a vague answer (especially about numbers, money, or the ROI), push back respectfully to get a hard, specific answer.

Here is THE RESUME
  {resume}
    """

def get_job_hunting_system_prompt(resume: str, jobAds: str) -> str:
    return f"""You are a confident, professional recruitment agent negotiating a salary offer for your candidate."""

def launch_knowledge_call(candidate_phone: str, knowledge_call_system_prompt) -> dict:
    print("launch knowledge call")
    # print("knowledge call launched", candidate_phone, knowledge_call_system_prompt)

# ---------------------------------------------------------------------------
# Bot 2 — Salary negotiation bot
# Goal: call tradie companies, persuasively negotiate salary using enriched profile
# ---------------------------------------------------------------------------

def launch_negotiation_call(
    company_phone: str,
    enriched_qa: dict | None = None,
) -> dict:
    """Bot 2: calls tradie companies to negotiate salary on behalf of the candidate."""
    resume = get_resume()
    system_prompt = get_knowledge_call_system_prompt(resume)
    first_message = (
        f"Hi, my name is Jordan and I'm a recruitment consultant. "
        f"I'm calling on behalf of , a "
        f"with years of experience. "
        "Is the hiring manager available for a quick two-minute chat?"
    )
    # return {"bot": "negotiation", "call": call}
