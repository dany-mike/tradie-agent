from fastapi import FastAPI, APIRouter, UploadFile, File, Request
from domain import launch_knowledge_call, get_phone, get_knowledge_call_system_prompt, create_assistant, launch_negotiation_call

app = FastAPI()
router = APIRouter(prefix="/launch", tags=["launch"])

@router.post("/", status_code=201)
async def create_candidate(resume: UploadFile = File(...)):
    content = await resume.read()
    resume_text = content.decode("utf-8")
    phone = get_phone(resume_text)
    knowledge_system_prompt = get_knowledge_call_system_prompt(resume_text)
    assistant = create_assistant("interview assistant", knowledge_system_prompt, "Hello here Manoa")
    launch_knowledge_call(phone, assistant["id"])

@app.post("/webhook")
async def vapi_webhook(request: Request):
    body = await request.json()
    message = body.get("message", {})

    if message.get("type") == "end-of-call-report":
        call = message.get("call", {})
        assistant_id = call.get("assistantId")

        if assistant_id:
            artifact = message.get("artifact", {})
            summary = artifact.get("summary", "")
            ended_reason = message.get("endedReason", "")
            print(f"Call ended: {ended_reason}")

            launch_negotiation_call(summary)

    return {"status": "ok"}

app.include_router(router)