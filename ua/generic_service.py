from pydantic_ai import Agent
from ua.utils import get_consumer_patterns, get_products_details, generic_offer_instructions
from ua.models import fallback_model
from pydantic import BaseModel

class GenericService:
    def __init__(self):
        self.model = fallback_model
    
    def create_generic_agent(self)->Agent:
        instructions = generic_offer_instructions()
        tools = [get_consumer_patterns, get_products_details]
        agent = Agent(model=self.model, instructions=instructions, tools=tools, output_type=list[str])
        return agent
    
    async def run_generic_agent(self, strategy_text: str)->list[str]:
        agent = self.create_generic_agent()
        result = await agent.run(strategy_text)
        return result.output

            
generic_service = GenericService()