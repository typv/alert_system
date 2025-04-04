from pydantic import BaseModel, Field
from typing import Optional

class LearningResultSchema(BaseModel):
    id: str
    major: str
    gender: str
    target: str
    region: str
    admission_block: str
    admission_score: str
    semester: str
    registered_credits: str
    semester_average: str
    accumulated_credits: str
    cumulative_average: str
    final_score: str
    academic_processing: Optional[str] = Field(default="")

class LearningResultResponseSchema(LearningResultSchema):
    pass