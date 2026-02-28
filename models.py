from pydantic import BaseModel

class CandidateProfile(BaseModel):
    phone: str
