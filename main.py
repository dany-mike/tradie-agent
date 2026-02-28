from fastapi import FastAPI, APIRouter
from models import CandidateProfile

app = FastAPI()
router = APIRouter(prefix="/launch", tags=["launch"])
@router.post("/", status_code=201)
async def create_candidate(body: CandidateProfile):
    return body

app.include_router(router)