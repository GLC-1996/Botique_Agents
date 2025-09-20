# models.py
from typing import List, Literal, Dict, Any
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal
from datetime import datetime, timezone

MoneyString = str  # use canonical string like "12.50 USD" OR {"units": 12, "nanos": 500000000, "currency_code":"USD"}

# ---------- Common types ----------
class Money(BaseModel):
    currency_code: str = Field("USD", description="ISO 4217")
    units: int
    nanos: int = 0

    def to_decimal(self) -> Decimal:
        return Decimal(self.units) + (Decimal(self.nanos) / Decimal(1_000_000_000))

class ProductRef(BaseModel):
    id: str
    name: str | None = None
    price: Money | None = None
    categories: List[str] | None = []

class AgentMeta(BaseModel):
    agent_id: str
    agent_version: str | None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

# ---------- Manager Input ----------
class CRAInput(BaseModel):
    ac_timeout: int = 20
    max_recover_disc_pct: float = 0.20

class SCAInput(BaseModel):
    skus: dict[str, float]

class ManagerInputs(BaseModel):
    manager_inputs: dict[Literal["AOV","CART_RECOVERY","STOCK_CLEARANCE"],Any]

    @model_validator(mode="after")
    def validate_manager_inputs(self):
        validated = {}
        for goal, inputs in self.manager_inputs.items():
            if goal == "AOV":
                if inputs is not None:
                    raise ValueError("Manager inputs are not required for AOV")
                validated[goal] = None
            elif goal == "CART_RECOVERY":
                if not inputs:
                    raise ValueError("Manager inputs are required for CART_RECOVERY")
                validated[goal] = CRAInput.model_validate(inputs)
            elif goal == "STOCK_CLEARANCE":
                if not inputs:
                    raise ValueError("Manager inputs are required for STOCK_CLEARANCE")
                validated[goal] = SCAInput.model_validate(inputs)
            else:
                raise ValueError(f"Unknown goal: {goal}")
        self.manager_inputs = validated
        return self

# ---------- Proposal (from specialized agents -> BGA) ----------
class CostImpact(BaseModel):
    actual_gmv: Money                        # GMV before strategy
    discounted_gmv: Money                    # GMV after strategy
    actual_shipping_cost: Money | None = None
    discounted_shipping_cost: Money | None = None
    baseline_margin: Money | None = None
    projected_margin: Money | None = None
    delta_amount: Money | None = None        # actual_gmv – discounted_gmv - (actual shipping - discounted shipping)
    delta_pct: float | None = None        # % change vs actual_gmv
    notes: str | None = None              # assumptions made

class LLMProposal(BaseModel):
    goal: Literal["AOV","CART_RECOVERY","STOCK_CLEARANCE"]
    strategies: list[str]

class ApproveRequest(BaseModel):
    goal: Literal["AOV","CART_RECOVERY","STOCK_CLEARANCE"]
    strategy_text: str

class ApprovedStrategy(BaseModel):
    strategy_id: str
    goal: Literal["AOV","CART_RECOVERY","STOCK_CLEARANCE"]
    strategy_text: str

class CategorizedStrategies(BaseModel):
    cart_related_strategies: list[str]
    generic_strategies: list[str]
