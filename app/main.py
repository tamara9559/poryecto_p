from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import engine, Base
from .config import settings

from .controllers.category_controller import router as category_router
from .controllers.product_controller import router as product_router

app = FastAPI(title=settings.APP_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(product_router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

