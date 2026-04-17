from fastapi import APIRouter
from services.send_stats import get_card_stats

router = APIRouter()

@router.get("/cards")
def cards():
    return get_card_stats()