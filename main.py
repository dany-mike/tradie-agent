from fastapi import FastAPI, APIRouter, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from domain import get_phone, get_knowledge_call_system_prompt, create_assistant, launch_negotiation_call, launch_knowledge_call, SERVER_URL

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
router = APIRouter(prefix="/launch", tags=["launch"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@router.post("/", status_code=201)
async def create_candidate(resume: UploadFile = File(...)):
    content = await resume.read()
    resume_text = content.decode("utf-8")
    phone = get_phone(resume_text)
    knowledge_system_prompt = get_knowledge_call_system_prompt(resume_text)
    assistant = create_assistant("interview assistant", knowledge_system_prompt, "Hello here Manoa", server_url=f"{SERVER_URL}/webhook")
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