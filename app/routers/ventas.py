from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Venta, VentaCreate
from ..services import VentaService

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Venta no encontrada"}},
)

@router.get("/", response_model=List[Venta])
async def obtener_ventas():
    """Obtiene todas las ventas"""
    return VentaService.get_all_ventas()

@router.get("/{venta_id}", response_model=Venta)
async def obtener_venta(venta_id: str):
    """Obtiene una venta específica por su ID"""
    return VentaService.get_venta_by_id(venta_id)

@router.post("/", response_model=Venta)
async def crear_venta(venta: VentaCreate):
    """Crea una nueva venta"""
    return VentaService.create_venta(venta)

@router.get("/cliente/{cliente_id}", response_model=List[Venta])
async def obtener_ventas_por_cliente(cliente_id: str):
    """Obtiene todas las ventas de un cliente específico"""
    return VentaService.get_ventas_by_cliente(cliente_id) 