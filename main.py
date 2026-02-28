from fastapi import FastAPI, APIRouter
from models import CandidateProfile
from domain import launch

app = FastAPI()
router = APIRouter(prefix="/launch", tags=["launch"])

@router.post("/", status_code=201)
async def create_candidate(body: CandidateProfile):
    result = launch(body)
    return result

app.include_router(router)