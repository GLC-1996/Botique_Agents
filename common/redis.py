from redis import Redis
from common.models import LLMProposal, ApprovedStrategy, CategorizedStrategies
import os

redis_host = os.getenv("REDIS_HOST", "redis-botique")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)

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

def delete_approved_strategy(strategy_id: str):
    redis_client.delete(f"strategy_id:{strategy_id}")

def delete_all_approved_strategies():
    keys = redis_client.keys("strategy_id:*")
    if keys:
        redis_client.delete(*keys)

def get_all_strategy_ids() -> list[str]:
    keys = redis_client.keys("strategy_id:*")
    strategy_ids = [key.split(":",1)[1] for key in keys]
    return strategy_ids

def set_categorized_strategies(run_id: str, categorized_strategies: CategorizedStrategies):
    redis_client.set(f"run_id:{run_id}", categorized_strategies.model_dump_json())

def get_categorized_strategies(run_id: str) -> CategorizedStrategies | None:
    categorized_strategies = redis_client.get(f"run_id:{run_id}")
    if categorized_strategies:
        return CategorizedStrategies.model_validate_json(categorized_strategies)
    return None

def get_all_run_ids() -> list[str]:
    keys = redis_client.keys("run_id:*")
    run_ids = [key.split(":",1)[1] for key in keys]
    return run_ids

def delete_categorized_strategies(run_id: str):
    redis_client.delete(f"run_id:{run_id}")

def delete_all_categorized_strategies():
    keys = redis_client.keys("run_id:*")
    if keys:
        redis_client.delete(*keys)

def set_current_run_id(run_id: str):
    redis_client.set("current_run_id", run_id)

def get_current_run_id() -> str | None:
    run_id = redis_client.get("current_run_id")
    if run_id:
        return run_id
    return None