#cart-agent/cart_poller.py
import os
import grpc
import asyncio
from common.models import Cart, CartItem
import cart_agent.cart_pb2 as cart_pb2
import cart_agent.cart_pb2_grpc as cart_pb2_grpc

#---------- Config ----------
CART_SERVICE_ADDRESS = os.getenv("CART_SERVICE_ADDRESS","cartservice:7070")
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "3.0"))
DEFAULT_USER_ID = "12345678-1234-1234-123456789123"
USER_ID = os.getenv("USER_ID", DEFAULT_USER_ID)

#---------- Functions ----------

async def get_cart(stub: cart_pb2_grpc.CartServiceStub):
    request = cart_pb2.GetCartRequest(user_id=USER_ID)
    response = await stub.GetCart(request)
    
    items = [CartItem(product_id=item.product_id, quantity=item.quantity) for item in response.items]
    return Cart(user_id=USER_ID, items=items)

async def poll_loop(app_state):

    while True:
        try:
            async with grpc.aio.insecure_channel(CART_SERVICE_ADDRESS) as channel:
                stub = cart_pb2_grpc.CartServiceStub(channel)
                cart = await get_cart(stub)

            if cart != app_state.last_cart:
                app_state.last_cart = cart

                if hasattr(app_state, "on_cart_update") and app_state.on_cart_update:
                    asyncio.create_task(app_state.on_cart_update(cart))
            
            await asyncio.sleep(POLL_INTERVAL)
        except Exception as e:
            print(f"Error polling cart: {e}")
            await asyncio.sleep(POLL_INTERVAL)

async def start_cart_poller(app_state):
    asyncio.create_task(poll_loop(app_state))