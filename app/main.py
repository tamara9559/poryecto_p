from fastapi import FastAPI
from .database import engine, Base
from .config import settings

# Routers
from .controllers.category_controller import router as category_router
from .controllers.product_controller import router as product_router

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def startup():
    # Crear tablas si no existen (solo para dev / despliegue inicial)
    Base.metadata.create_all(bind=engine)


# Incluir routers
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(product_router, prefix="/products", tags=["products"])


@app.get("/")
def read_root():
    return {"app": settings.APP_NAME, "message": "API de inventario funcionando"}
