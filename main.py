#!/usr/bin/env python3
"""
Punto de entrada principal para el Sistema de Punto de Venta
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD
    ) 