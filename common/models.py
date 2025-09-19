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
    manager_inputs: dict[Literal["AOV","CART_RECOVERY","CLEAR_STOCK"],Any]

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
            elif goal == "CLEAR_STOCK":
                if not inputs:
                    raise ValueError("Manager inputs are required for CLEAR_STOCK")
                validated[goal] = SCAInput.model_validate(inputs)
            else:
                raise ValueError(f"Unknown goal: {goal}")
        self.manager_inputs = validated
        return self

# ---------- Activations ----------
class ActivationRequest(BaseModel):
    request_id: str
    # manager_inputs: list[ManagerInputs]
    meta: AgentMeta | None = None

class ActivationResponse(BaseModel):
    request_id: str
    status: Literal["READY", "FAILED"]
    meta: AgentMeta | None = None

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


class ActionItem(BaseModel):
    action_id: str
    action_type: str                      # free text, agent can invent
    title: str
    description: str | None = None
    products: list[ProductRef] | None = None
    discount_pct: float | None = None
    discount_amount: Money | None = None
    conditions: dict[str, str] | None = None
    display_meta: dict[str, str] | None = None


class Proposal(BaseModel):
    proposal_id: str
    goal: Literal["AOV","CART_RECOVERY","CLEAR_STOCK"]
    selected_playbook: str | None  # e.g., "bundle_with_complement"
    strategy_text: str                 # LLM natural language summary
    structured_actions: List[ActionItem]
    cost_impact: CostImpact
    confidence: float | None = Field(..., ge=0.0, le=1.0)
    # guardrail checks (agents should include)
    guardrail_checks: Dict[str, Literal["PASS","WARN","FAIL"]]
    meta: AgentMeta | None

class LLMProposal(BaseModel):
    goal: Literal["AOV","CART_RECOVERY","CLEAR_STOCK"]
    strategies: list[str]

class ApproveRequest(BaseModel):
    goal: Literal["AOV","CART_RECOVERY","CLEAR_STOCK"]
    strategy_text: str

class ApprovedStrategy(BaseModel):
    strategy_id: str
    goal: Literal["AOV","CART_RECOVERY","CLEAR_STOCK"]
    strategy_text: str

# ---------- BGA Validation result ----------
class ValidatedProposal(BaseModel):
    proposal_id: str
    status: Literal["APPROVE","REJECT","REQUIRE_OVERRIDE"]
    reason: str | None = None
    proposal: Proposal
    meta: AgentMeta | None

# ---------- Approved plan (BGA -> UA) ----------
class ApprovedPlan(BaseModel):
    plan_id: str
    goal: Literal["AOV","CART_RECOVERY","CLEAR_STOCK"]
    # Snapshot of Proposal details
    strategy_text: str                     # LLM summary of strategy
    cost_impact: CostImpact
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    guardrails_applied: Dict[str, str] = {}
    # Execution metadata
    approved_by: str                       # manager id
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actions: List[ActionItem]              # UA will render these
    meta: AgentMeta | None = None


# ---------- Render Plan ----------
class RenderPlan(BaseModel):
    render_as: Literal["banner", "popup", "product-card", "list"]
    headline: str
    body: str | None = None
    products: list[ProductRef] | None = None
    price_info: dict[str, str] | None = None   # {"before": "$100", "after": "$80"}
    style: dict[str, str] | None = None        # {"badge": "🔥 Hot Deal", "color": "red"}
    conditions: dict[str, str] | None = None   # {"expires_in_hours": "24"}


# ---------- UA -> user event telemetry (optional) ----------
class UserEvent(BaseModel):
    event_id: str
    user_id: str | None
    session_id: str | None
    plan_id: str | None
    action_id: str | None
    event_type: Literal["VIEW","CLICK","ADD_TO_CART","CHECKOUT_ATTEMPT"]
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    details: Dict[str,str] | None = {}

class UserChatMessage(BaseModel):
    message_id: str
    session_id: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class AgentChatResponse(BaseModel):
    message_id: str
    reply_to: str
    text: str
    suggested_actions: list[RenderPlan] | None = None
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))


