from pydantic import BaseModel


class InterestingQA(BaseModel):
    most_challenging_project: str
    reason_for_change: str
    interesting_facts: str
    managed_team: str


class CandidateProfile(BaseModel):
    name: str
    address: str
    age: int
    role: str
    years_of_experience: int
    current_salary: float
    target_salary: float
    current_company: str
    past_companies: list[str]
    interesting_qa: InterestingQA
