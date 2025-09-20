# agent/agent_utils.py
from pathlib import Path

class AgentUtils:
    def __init__(self, inputs: str):
        self.inputs = inputs
        self.goal = inputs
    
    def get_instructions(self)->str:
        base_instr = """
        You are part of a small online boutique's strategy team.
        Your task is to propose high-level product promotions strategies on the goal mentioned below.
        - You report to the manager
        - Your strategies should be general, so they can later be turned into specific offers using product and customer data.
        - Provide 3 to 5 clear, practical strategies with strategy text for each strategy. Each strategy should be a single sentence.
        - You may use the available tools (products, consumer patterns, costs) if needed.
        - Just return the strategies, no other text.

        Example strategies:
        - Offer 5 percent discount if cart value > $50 and 10 percent if > $100.
        - Bundle similar products with a small discount.
        - Free shipping above $80.
        - Buy 2, get 20 percent off.

        Output Example:
        ["Offer free shipping for orders above $50","Bundle similar products with a small discount","Free shipping above $80"]
        """
        instructions = {
            "AOV": f"""{base_instr}

            Your Goal: generate strategies to increase the Average Order Value (AOV). Return a list of strategy texts.
            """,
            "CART_RECOVERY": f"""{base_instr}

            Your Goal: generate strategies to encourage cart recovery (reduce cart abandonment). Return a list of strategy texts.
            """,
            "STOCK_CLEARANCE": f"""{base_instr}

            Your Goal: generate strategies to clear excess stock efficiently. Return a list of strategy texts.
            """,
        }

        return instructions[self.goal]

    def create_prompt(self)->str:
        return f"""Give me strategies for {self.goal}. Use the available tools if needed."""

    def get_products(self)->str:
        file_path = Path(__file__).parent / "data" / "products.json"
        return file_path.read_text()
    
    def get_consumer_patterns(self)->str:
        file_path = Path(__file__).parent / "data" / "consumer_patterns.json"
        return file_path.read_text()
    
    def get_products_cost(self)->str:
        file_path = Path(__file__).parent / "data" / "products_cost.json"
        return file_path.read_text()