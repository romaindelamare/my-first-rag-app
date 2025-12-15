from fastapi import APIRouter
from app.evaluation.benchmark import run_benchmark

router = APIRouter(prefix="/benchmark", tags=["benchmark"])


@router.post("/run")
def run():
    return {
        "results": run_benchmark()
    }
