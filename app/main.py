from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.database import engine, Base
from app.routers import auth, categories, products, cart, orders
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s -%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "E-commerce Backend API",
    description="A complete e-commerce backend with products, cart and orders",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")