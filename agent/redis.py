from redis import Redis
from common.models import LLMProposal, ApprovedStrategy

redis_client = Redis(host="localhost", port=6379, decode_responses=True)

def set_proposals(proposals: list[LLMProposal]):
    for proposal in proposals:
        redis_client.set(f"goal:{proposal.goal}", proposal.model_dump_json())

def get_proposals(goal: str) -> LLMProposal | None:
    prop = redis_client.get(f"goal:{goal}")
    if prop:
        return LLMProposal.model_validate_json(prop)
    return None

def set_approved_strategy(strategy: ApprovedStrategy):
    redis_client.set(f"strategy_id:{strategy.strategy_id}", strategy.model_dump_json())

def get_approved_strategy(strategy_id: str) -> ApprovedStrategy | None:
    strategy = redis_client.get(f"strategy_id:{strategy_id}")
    if strategy:
        return ApprovedStrategy.model_validate_json(strategy)
    return None