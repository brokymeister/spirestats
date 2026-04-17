from fastapi import APIRouter
from services.send_stats import get_encounter_stats

router = APIRouter()

@router.get("/encounters")
def relics():
    return get_encounter_stats()