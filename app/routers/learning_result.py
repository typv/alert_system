from fastapi import APIRouter
from typing import List
from ..services.service_learning_result import LearningResultsService
from ..schemas.learning_result import LearningResultSchema

router = APIRouter(prefix="/api/plr", tags=["learning-results"])

@router.post("/process-learning-results")
def process_learning_results(students: List[LearningResultSchema]):

    processed_results = LearningResultsService.process_academic_performance(
        [student.dict() for student in students]
    )
    return processed_results