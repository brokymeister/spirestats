from fastapi import APIRouter
from services.send_stats import get_general_stats

router = APIRouter()

@router.get("/overview")
def overview():
    return get_general_stats()