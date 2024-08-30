from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import rentals, cars, renters

app = FastAPI(title="Garazh: Backend APIs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rentals.router, prefix="/rentals")
app.include_router(cars.router, prefix="/cars")
app.include_router(renters.router, prefix="/renters")
