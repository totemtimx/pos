from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import productos, clientes, ventas, reportes
from .config import settings

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(productos.router)
app.include_router(clientes.router)
app.include_router(ventas.router)
app.include_router(reportes.router)

@app.get("/")
async def root():
    """Endpoint raíz de la aplicación"""
    return {
        "mensaje": f"{settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "environment": "development" if settings.is_development() else "production",
        "documentacion": "/docs",
        "endpoints": {
            "productos": "/productos",
            "clientes": "/clientes", 
            "ventas": "/ventas",
            "reportes": "/reportes"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return {"status": "healthy", "message": "API funcionando correctamente"} 


def hola():
    print("asdas")
    var1 = [1,2,3]
    print(var1)