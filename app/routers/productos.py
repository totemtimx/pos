from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Producto, ProductoCreate
from ..services import ProductoService

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={404: {"description": "Producto no encontrado"}},
)

@router.get("/", response_model=List[Producto])
async def obtener_productos():
    """Obtiene todos los productos"""
    return ProductoService.get_all_productos()

@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: str):
    """Obtiene un producto específico por su ID"""
    return ProductoService.get_producto_by_id(producto_id)

@router.post("/", response_model=Producto)
async def crear_producto(producto: ProductoCreate):
    """Crea un nuevo producto"""
    return ProductoService.create_producto(producto)

@router.put("/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: str, producto: ProductoCreate):
    """Actualiza un producto existente"""
    return ProductoService.update_producto(producto_id, producto)

@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):
    """Elimina un producto"""
    return ProductoService.delete_producto(producto_id) 