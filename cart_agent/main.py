#cart-agent/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import cart_agent.cart_poller as cart_poller
import cart_agent.cart_service as cart_service
from common.models import Cart, CartItem
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.last_cart = None
    app.state.latest_message = ""

    # trigger callback
    async def on_cart_update(cart: Cart):
        message = await cart_service.run_agent(cart)

        #only save if cart matches the latest state
        if cart == app.state.last_cart:
            app.state.latest_message = message
            print(f"Offers updated: {message}")
        else:
            print(f"Message discarded due to cart mismatch")
    
    app.state.on_cart_update = on_cart_update

    #start the cart poller
    await cart_poller.start_cart_poller(app.state)

    yield

    #shutdown logic
    print("Shutting down cart agent")


app = FastAPI(
    title="Cart Agent",
    description="Cart Agent is a service that polls the cart service and updates the cart",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/cart/message")
async def get_cart_message():
    return {"message": app.state.latest_message}



if __name__ == "__main__":
    uvicorn.run(
        "cart_agent.main:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )