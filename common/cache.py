# common/cache.py
import redis
import json
from common.models import ApprovedPlan

# configure Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

key = "plan:demo-session"

def set_plan(plan: ApprovedPlan):
    redis_client.set(key, plan.model_dump_json())

def get_plan() -> ApprovedPlan | None:
    raw = redis_client.get(key)
    if not raw:
        return None
    return ApprovedPlan.model_validate_json(raw)

def clear_plan():
    redis_client.delete(key)
