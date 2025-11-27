from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from config import get_settings
from database import init_db
from controllers import category_router, product_router

settings = get_settings()

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Sistema de Gestión de Inventario - API REST"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(category_router, prefix=settings.API_PREFIX)
app.include_router(product_router, prefix=settings.API_PREFIX)

# Montar archivos estáticos para el frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.on_event("startup")
async def startup_event():
    """Inicializa la base de datos al iniciar la aplicación"""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Sirve la interfaz web"""
    html_path = Path("frontend/templates/index.html")
    return html_path.read_text()


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "version": settings.API_VERSION}