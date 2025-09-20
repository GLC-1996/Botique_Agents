# agent/agent_api.py
import uuid
from fastapi import APIRouter
from common.models import LLMProposal, ApproveRequest, ApprovedStrategy
from agent.orchestrator import orchestrator
from agent.redis import set_approved_strategy

router = APIRouter()

@router.post("/activate", response_model=list[LLMProposal])
async def activate(request: list[str]):
    for i in request:
        if i not in ["AOV", "CART_RECOVERY", "STOCK_CLEARANCE"]:
            raise ValueError(f"Invalid goal: {i}")
    if len(request) == 0:
        raise ValueError("No goals provided")
    response = await orchestrator.run_agents(request)
    return response

@router.post("/fetch_proposals", response_model=list[LLMProposal] | None)
async def fetch_proposals():
    """
    Returns proposals from in-memory cache only.
    If None, frontend should trigger /activate to regenerate proposals.
    """
    response = orchestrator.fetch_proposals()
    return response

@router.post("/approve_strategy", response_model=ApprovedStrategy)
def approve_strategy(request: ApproveRequest):
    strategy_id = str(uuid.uuid4())
    approved_strategy = ApprovedStrategy(
        strategy_id=strategy_id,
        goal=request.goal,
        strategy_text=request.strategy_text
    )
    set_approved_strategy(approved_strategy)
    return approved_strategy

@router.post("/clear_proposals", response_model=None)
def clear_proposals():
    orchestrator.clear_proposals()
    return None