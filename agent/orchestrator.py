# agent/orchestrator.py
from agent.agent_service import AgentService
from agent.models import testing_model, fallback_model
from common.models import LLMProposal
from agent.redis import set_proposals, get_proposals

class Orchestrator:
    def __init__(self):
        self.model = testing_model
        self.agent_services: list[AgentService] = []
        self.proposals: list[LLMProposal] | None = None
    
    def activate(self, inputs: list[str])->list[AgentService]:
        self.agent_services = []
        for i in inputs:
            agent_service = AgentService(i, self.model)
            self.agent_services.append(agent_service)
        return self.agent_services
    
    async def run_agents(self, inputs: list[str])-> list[LLMProposal]:
        self.activate(inputs)
        results: list[LLMProposal] = []
        for agent_service in self.agent_services:
            response = await agent_service.run_agent()
            proposal = LLMProposal(
                goal=agent_service.goal,
                strategies=response
            )
            results.append(proposal)
        self.proposals = results
        # set_proposals(results)
        return results
    
    def fetch_proposals(self)-> list[LLMProposal] | None:
        return self.proposals


orchestrator = Orchestrator()