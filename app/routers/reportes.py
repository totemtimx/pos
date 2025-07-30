from fastapi import APIRouter
from typing import List

from ..models import ReporteVentas, ProductoPopular
from ..services import ReporteService

router = APIRouter(
    prefix="/reportes",
    tags=["reportes"],
    responses={200: {"description": "Reporte generado exitosamente"}},
)

@router.get("/ventas-totales", response_model=ReporteVentas)
async def reporte_ventas_totales():
    """Genera reporte de estadísticas generales de ventas"""
    return ReporteService.get_ventas_totales()

@router.get("/productos-populares", response_model=List[ProductoPopular])
async def reporte_productos_populares():
    """Genera reporte de los productos más populares"""
    return ReporteService.get_productos_populares() 