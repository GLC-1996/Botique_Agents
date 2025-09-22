from fastapi import APIRouter, Body
from ua.generic_service import generic_service
from ua.cat import cat

router = APIRouter()

@router.post("/start-campaign")
async def categorize_strategies():
    strategies = cat.get_strategies()
    
    try:
        results = await cat.categorize_strategies(strategies)

    except Exception as e:
        results = cat.fallback_categorize_strategies(strategies)

    return results

@router.get("/generic-offers")
async def generic_offers():
    offers = await generic_service.run_generic_agent()
    return offers