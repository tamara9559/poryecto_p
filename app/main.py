from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .config import settings

from .controllers.category_controller import router as category_router
from .controllers.product_controller import router as product_router

app = FastAPI(title=settings.APP_NAME)

# CORS (necesario para frontend web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar cuando tengas dominio fijo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(product_router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return {
        "app": settings.APP_NAME,
        "message": "API de inventario funcionando correctamente"
    }

