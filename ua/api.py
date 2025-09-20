from fastapi import APIRouter, Body
from ua.service import ua_service
from ua.cat import cat
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/categorize-strategies")
async def categorize_strategies():
    strategies = cat.get_strategies()
    
    try:
        results = await cat.categorize_strategies(strategies)
        logger.info("Strategies categorized successfully")

    except Exception as e:
        logger.error(f"Error categorizing strategies: {e}")
        results = cat.fallback_categorize_strategies(strategies)
        logger.warning("Fallback categorization used")

    return results

@router.get("/generic-offers")
async def generic_offers():
    offers = await ua_service.run_generic_agent()
    return offers