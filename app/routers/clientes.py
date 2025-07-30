from fastapi import APIRouter, HTTPException
from typing import List

from ..models import Cliente, ClienteCreate
from ..services import ClienteService

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"description": "Cliente no encontrado"}},
)

@router.get("/", response_model=List[Cliente])
async def obtener_clientes():
    """Obtiene todos los clientes"""
    return ClienteService.get_all_clientes()

@router.get("/{cliente_id}", response_model=Cliente)
async def obtener_cliente(cliente_id: str):
    """Obtiene un cliente específico por su ID"""
    return ClienteService.get_cliente_by_id(cliente_id)

@router.post("/", response_model=Cliente)
async def crear_cliente(cliente: ClienteCreate):
    """Crea un nuevo cliente"""
    return ClienteService.create_cliente(cliente)

@router.put("/{cliente_id}", response_model=Cliente)
async def actualizar_cliente(cliente_id: str, cliente: ClienteCreate):
    """Actualiza un cliente existente"""
    return ClienteService.update_cliente(cliente_id, cliente)

@router.delete("/{cliente_id}")
async def eliminar_cliente(cliente_id: str):
    """Elimina un cliente"""
    return ClienteService.delete_cliente(cliente_id) 