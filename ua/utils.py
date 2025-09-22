from pathlib import Path

def categorization_instructions() -> str:
    return """
    Your are a part of a small online boutique's strategy team.
    You are given a specific strategy text.
    Your job is to identify whether the strategy is related to cart value or not.

    if the strategy is related to cart value, return 'True', otherwise return 'False'.

    Output requirements:
    - Return only 1 word: True or False
    - Do not include explanations, punctuations, characters or extra words.

    examples:
    Prompt: "Offer 5 percent discount if cart value is above $50"
    Response: True

    Prompt: "Offer free shipping for all orders above $50"
    Response: False
    """

    
def create_prompt(goal: str)->str:
    return f"""Give me strategies for {goal}. Use the available tools if needed."""

def get_products()->str:
    file_path = Path(__file__).parent / "data" / "products.json"
    return file_path.read_text()
    
def get_consumer_patterns()->str:
    file_path = Path(__file__).parent / "data" / "consumer_patterns.json"
    return file_path.read_text()
    
def get_products_cost()->str:
    file_path = Path(__file__).parent / "data" / "products_cost.json"
    return file_path.read_text()

def generic_offer_instructions()->str:
    return f"""
    You are part of a small online boutique's strategy team.
    You are given a specific strategy text.
    Your job is to create a specific offer for the strategy.
    You have the following tools available to you:
    - get_products: to get the list of products
    - get_consumer_patterns: to get the list of consumer patterns
    - get_products_cost: to get the cost of the products

    Your task:
    generate 3-5 specific offers based on the data you have which align with the given strategy.
    Each offer should be a single sentence.
    The offers should contain atleast one product from the list of products.
    Use product id to identify the product. Do not use product name.
    The offers should be in a format that can be easily understood by the user.

    Output requirements:
    - Return ONLY a list of strings.
    - Do not include explanations, punctuation, or extra words.
    - It should only contain the offers.

    Examples:
    Prompt: "Bundle similar products with a small discount"
    Response: ["Buy OLJCESPC7Z and 1YMWWN1N4O for 10% off", "Buy 66VCHSJNUP and L9ECAV7KIM for 15% off"]

    Your goal:
    generate 3-5 specific offers and return a list of strings.
    """