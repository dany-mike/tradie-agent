from fastapi import FastAPI, APIRouter, UploadFile, File
from domain import launch_knowledge_call, get_tradie_phone, get_knowledge_call_system_prompt, create_assistant

app = FastAPI()
router = APIRouter(prefix="/launch", tags=["launch"])

@router.post("/", status_code=201)
async def create_candidate(resume: UploadFile = File(...)):
    content = await resume.read()
    resume_text = content.decode("utf-8")
    phone = get_tradie_phone(resume_text)
    knowledge_system_prompt = get_knowledge_call_system_prompt(resume_text)
    # assistant = create_assistant("interview assistant", knowledge_system_prompt, "Hello here Manoa")
    # print(assistant["id"])
    launch_knowledge_call(phone, knowledge_system_prompt, "3e986ac7-5e9e-4d14-b939-7c3a3add0ebb")
    # return result

app.include_router(router)