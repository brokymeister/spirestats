from fastapi import APIRouter
from services.send_stats import get_relic_stats

router = APIRouter()

@router.get("/relics")
def relics():
    return get_relic_stats()