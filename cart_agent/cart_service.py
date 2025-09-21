#cart-agent/cart_service.py
from common.models import Cart, CategorizedStrategies, CartItem
from pydantic_ai import Agent
from agent.models import fallback_model, testing_model
from agent.redis import get_current_run_id, get_categorized_strategies
from pathlib import Path
import json

def get_products_details()->list[dict]:
    file_path = Path(__file__).parent / "data" / "products_cost.json"
    data = json.loads(file_path.read_text())
    return data["products_details"]

def get_cart_related_strategies()->list[str]:
    run_id = get_current_run_id()
    if run_id:
        categorized_strategies = get_categorized_strategies(run_id)
        if categorized_strategies:
            return categorized_strategies.cart_related_strategies
    return []

def cart_details(cart: Cart)->float:
    cart_items: list[CartItem] = cart.items

    products_details = get_products_details()

    cart_value: float = 0

    for item in cart_items:
        cost = next((product['retail_price_usd'] for product in products_details if product['id'] == item.product_id), 0)
        cart_value += cost * item.quantity

    return cart_value

def create_instructions()->str:

    strategies = get_cart_related_strategies()

    instructions = f"""
    You are an agent that is responsible for generating user messages to encourage the user to complete the purchase.
    You will be given a list of strategies that you are to follow to generate the messages.
    Do not generate messages that do not align with the strategies.

    available strategies: {strategies}

    Your task:
    You will be provided the value of the abandoned cart. Take this value, cross check with the available strategies and generate the messages.

    Example 1:
    Available strategy: offer a discount of 10 percent on the cart value if the cart value is greater than 100 USD.
    Cart value: 90 USD
    Your message: "Add products worth 10 USD to the cart to get a discount of 10 percent."

    Example 2:
    Available strategy: offer a discount of 10 percent on the cart value if the cart value is greater than 100 USD.
    Cart value: 120 USD
    Your message: "You are eligible for a discount of 10 percent."

    Output requirement:
    - Should contain only the message to be sent to the user.
    - DO NOT include any other text in the output.
    """
    return instructions

async def run_agent(cart: Cart)->str:
    instructions = create_instructions()
    model = testing_model
    agent = Agent(model=model, instructions=instructions)

    cart_value = cart_details(cart)

    prompt = f""" this is the cart value: {cart_value}, generate the message to be sent to the user as per the instructions. your response should include only the message to be sent to the user. """
    message = await agent.run(prompt)

    return message

