from pydantic_ai import Agent
from ua.models import fallback_model, testing_model
from ua.utils import categorization_instructions
from pydantic import BaseModel, ValidationError
from typing import Literal
from common.redis import get_all_strategy_ids, get_approved_strategy, set_categorized_strategies, set_current_run_id
from common.models import CategorizedStrategies
import uuid

class BoolOutput(BaseModel):
    value: Literal["true", "false"]

class Cat:
    def __init__(self):
        self.model = testing_model
        self.instructions = categorization_instructions()
        self.agent = Agent(model=self.model, instructions=self.instructions)

    def get_strategies(self)->list[str]:
        strategy_ids = get_all_strategy_ids()
        strategies = []
        for s in strategy_ids:
            strategy_text = get_approved_strategy(s).strategy_text
            strategies.append(strategy_text)
        return strategies
    
    def output_function(self, response: str)->bool:
        try:
            parsed = BoolOutput(value=response.strip().lower())
        except ValidationError as e:
            raise e
        return parsed.value == "true"
    
    async def categorize_strategies(self, strategies: list[str])->str:
        cart_related_strategies = []
        generic_strategies = []
        for strategy in strategies:
            result = await self.agent.run(strategy)
            if self.output_function(result.output):
                cart_related_strategies.append(strategy)
            else:
                generic_strategies.append(strategy)
        
        run_id = str(uuid.uuid4())
        categorized_strategies = CategorizedStrategies(
            cart_related_strategies=cart_related_strategies,
            generic_strategies=generic_strategies
        )

        set_categorized_strategies(run_id, categorized_strategies)
        set_current_run_id(run_id)

        return run_id
    
    def fallback_categorize_strategies(self, strategies: list[str])->str:
        cart_related_strategies = []
        generic_strategies = []
        for strategy in strategies:
            if "cart value" in strategy.lower():
                cart_related_strategies.append(strategy)
            else:
                generic_strategies.append(strategy)
        run_id = str(uuid.uuid4())
        categorized_strategies = CategorizedStrategies(
            cart_related_strategies=cart_related_strategies,
            generic_strategies=generic_strategies
        )
        set_categorized_strategies(run_id, categorized_strategies)
        set_current_run_id(run_id)
        return run_id
    
cat = Cat()
