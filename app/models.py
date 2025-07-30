from pydantic import BaseModel
from typing import List

# Modelos para Productos
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str

class Producto(ProductoBase):
    id: str
    fecha_creacion: str

class ProductoCreate(ProductoBase):
    pass

# Modelos para Clientes
class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: str

class Cliente(ClienteBase):
    id: str
    fecha_registro: str

class ClienteCreate(ClienteBase):
    pass

# Modelos para Ventas
class VentaItem(BaseModel):
    producto_id: str
    cantidad: int
    precio_unitario: float

class VentaBase(BaseModel):
    cliente_id: str
    items: List[VentaItem]
    total: float

class Venta(VentaBase):
    id: str
    fecha: str
    estado: str

class VentaCreate(BaseModel):
    cliente_id: str
    items: List[VentaItem]

# Modelos para Reportes
class ReporteVentas(BaseModel):
    total_ventas: int
    total_ingresos: float
    promedio_por_venta: float

class ProductoPopular(BaseModel):
    producto_id: str
    nombre: str
    cantidad_vendida: int 