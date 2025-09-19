from pydantic import BaseModel
from common.models import CostImpact

# ---------- Guardrails ----------

class GuardrailConfig(BaseModel):
    max_discount_pct_auto: float = 0.20    # Max 20% auto discount
    max_margin_erosion_pct: float = 0.15   # Max 15% margin loss
    never_below_cost: bool = True          # Never price below cost
    min_confidence_to_auto_approve: float = 0.7

def check_guardrails(cost_impact: CostImpact, proposal_confidence: float, config: GuardrailConfig):
    checks = {}

    # Check 1: Never below cost
    if config.never_below_cost and cost_impact.projected_margin and cost_impact.projected_margin.to_decimal() < 0:
        checks["never_below_cost"] = "FAIL"
    else:
        checks["never_below_cost"] = "PASS"

    # Check 2: Max discount %
    if cost_impact.delta_pct and abs(cost_impact.delta_pct) > config.max_discount_pct_auto:
        checks["max_discount_pct_auto"] = "FAIL"
    else:
        checks["max_discount_pct_auto"] = "PASS"

    # Check 3: Margin erosion
    if cost_impact.baseline_margin and cost_impact.projected_margin:
        erosion = (cost_impact.baseline_margin.to_decimal() - cost_impact.projected_margin.to_decimal()) / cost_impact.baseline_margin.to_decimal()
        if erosion > config.max_margin_erosion_pct:
            checks["margin_erosion"] = "FAIL"
        else:
            checks["margin_erosion"] = "PASS"

    # Check 4: Confidence
    if proposal_confidence < config.min_confidence_to_auto_approve:
        checks["confidence_threshold"] = "WARN"
    else:
        checks["confidence_threshold"] = "PASS"

    return checks
