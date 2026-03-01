from fastapi import FastAPI, APIRouter, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from domain import get_phone, get_knowledge_call_system_prompt, create_assistant, launch_negotiation_call, launch_knowledge_call, SERVER_URL

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
router = APIRouter(prefix="/launch", tags=["launch"])

call_state = {
    "status": "idle",
    "knowledge_assistant_id": None,
    "negotiation_assistant_id": None,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.get("/status")
async def get_status():
    return {"status": call_state["status"]}

@router.post("/", status_code=201)
async def create_candidate(resume: UploadFile = File(...)):
    content = await resume.read()
    resume_text = content.decode("utf-8")
    phone = get_phone(resume_text)
    knowledge_system_prompt = get_knowledge_call_system_prompt(resume_text)
    assistant = create_assistant("interview assistant", knowledge_system_prompt, "Hello here Manila", voice={"provider": "11labs", "voiceId": "FGY2WhTYpPnrIDTdsKH5"}, server_url=f"{SERVER_URL}/webhook")
    launch_knowledge_call(phone, assistant["id"])

    call_state["status"] = "call_in_progress"
    call_state["knowledge_assistant_id"] = assistant["id"]
    call_state["negotiation_assistant_id"] = None

    return {"status": "call_in_progress", "message": "Knowledge call launched successfully"}

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
            print(f"Call ended: {ended_reason}, assistant: {assistant_id}")

            # Bot 1 (knowledge call) ended → launch Bot 2 (negotiation)
            if assistant_id == call_state.get("knowledge_assistant_id"):
                messages = artifact.get("messages", [])
                user_messages = [m.get("message", "") for m in messages if m.get("role") == "user"]
                user_transcript = "\n".join(user_messages)
                result = launch_negotiation_call(summary, user_transcript)
                call_state["status"] = "waiting_for_negotiation"
                neg_assistant_id = result.get("call", {}).get("assistantId")
                if neg_assistant_id:
                    call_state["negotiation_assistant_id"] = neg_assistant_id

            # Bot 2 (negotiation call) ended → scenario complete
            elif assistant_id == call_state.get("negotiation_assistant_id"):
                call_state["status"] = "scenario_ended"

    return {"status": "ok"}

app.include_router(router)