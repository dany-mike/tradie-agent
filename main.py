from fastapi import FastAPI, APIRouter, UploadFile, File
from domain import launch_knowledge_call, get_tradie_phone, get_knowledge_call_system_prompt

app = FastAPI()
router = APIRouter(prefix="/launch", tags=["launch"])

@router.post("/", status_code=201)
async def create_candidate(resume: UploadFile = File(...)):
    content = await resume.read()
    resume_text = content.decode("utf-8")
    phone = get_tradie_phone(resume_text)
    system_prompt = get_knowledge_call_system_prompt(resume_text)
    result = launch_knowledge_call(phone, system_prompt)
    # return result

app.include_router(router)