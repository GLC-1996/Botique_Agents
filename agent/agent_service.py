# agent/agent_service.py
from pydantic_ai import Agent, PromptedOutput
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIChatModel
from agent.agent_utils import AgentUtils

class AgentService:
    def __init__(self, inputs: str, model: FallbackModel | OpenAIChatModel):
        self.goal = inputs
        self.utils = AgentUtils(inputs)
        self.model = model
        self.agent: Agent | None = None

    def create_agent(self)->Agent:
        
        instructions = self.utils.get_instructions()
        tools = [self.utils.get_products, self.utils.get_consumer_patterns, self.utils.get_products_cost]
        
        self.agent = Agent(model=self.model,
                      instructions=instructions,
                      output_type=list[str],
                      tools=tools)
        return self.agent
    
    async def run_agent(self)->list[str]:
        if self.agent is None:
            self.create_agent()
        prompt = self.utils.create_prompt()
        response = await self.agent.run(prompt)
        print(response.all_messages)
        return response.output