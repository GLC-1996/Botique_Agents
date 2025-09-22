# models.py
from typing import Literal
from pydantic import BaseModel

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

# ---------- Cart models ----------

class CartItem(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: list[CartItem]

