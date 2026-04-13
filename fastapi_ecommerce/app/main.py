from fastapi import FastAPI, Request
from app.routers import categories, products, users, reviews, orders, cart
from fastapi.staticfiles import StaticFiles
from app.logger.logger import log_middleware


app = FastAPI(title='FastAPI e-shop', version='0.1.0')

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.middleware("http")(log_middleware)



@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}

app.mount("/media", StaticFiles(directory="media"), name="media")