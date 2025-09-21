#cart-agent/main.py
from fastapi import FastAPI, asynccontextmanager
import cart_poller
import cart_service
from common.models import Cart, CartItem


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