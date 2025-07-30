from typing import List, Dict, Any
from fastapi import HTTPException

from .models import Producto, ProductoCreate, Cliente, ClienteCreate, Venta, VentaCreate, ReporteVentas, ProductoPopular
from .database import db_manager
from .utils import generate_id, get_current_timestamp, validate_email, validate_phone, calculate_total

class ProductoService:
    @staticmethod
    def get_all_productos() -> List[Producto]:
        """Obtiene todos los productos"""
        productos_data = db_manager.get_productos()
        return [Producto(**producto) for producto in productos_data]
    
    @staticmethod
    def get_producto_by_id(producto_id: str) -> Producto:
        """Obtiene un producto por su ID"""
        producto_data = db_manager.get_producto_by_id(producto_id)
        if not producto_data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return Producto(**producto_data)
    
    @staticmethod
    def create_producto(producto: ProductoCreate) -> Producto:
        """Crea un nuevo producto"""
        nuevo_producto = Producto(
            id=generate_id(),
            **producto.dict(),
            fecha_creacion=get_current_timestamp()
        )
        db_manager.add_producto(nuevo_producto.dict())
        return nuevo_producto
    
    @staticmethod
    def update_producto(producto_id: str, producto: ProductoCreate) -> Producto:
        """Actualiza un producto existente"""
        producto_existente = db_manager.get_producto_by_id(producto_id)
        if not producto_existente:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto_actualizado = Producto(
            id=producto_id,
            **producto.dict(),
            fecha_creacion=producto_existente["fecha_creacion"]
        )
        
        success = db_manager.update_producto(producto_id, producto_actualizado.dict())
        if not success:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return producto_actualizado
    
    @staticmethod
    def delete_producto(producto_id: str) -> Dict[str, str]:
        """Elimina un producto"""
        success = db_manager.delete_producto(producto_id)
        if not success:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado exitosamente"}

class ClienteService:
    @staticmethod
    def get_all_clientes() -> List[Cliente]:
        """Obtiene todos los clientes"""
        clientes_data = db_manager.get_clientes()
        return [Cliente(**cliente) for cliente in clientes_data]
    
    @staticmethod
    def get_cliente_by_id(cliente_id: str) -> Cliente:
        """Obtiene un cliente por su ID"""
        cliente_data = db_manager.get_cliente_by_id(cliente_id)
        if not cliente_data:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return Cliente(**cliente_data)
    
    @staticmethod
    def create_cliente(cliente: ClienteCreate) -> Cliente:
        """Crea un nuevo cliente"""
        # Validar email y teléfono
        if not validate_email(cliente.email):
            raise HTTPException(status_code=400, detail="Formato de email inválido")
        
        if not validate_phone(cliente.telefono):
            raise HTTPException(status_code=400, detail="Formato de teléfono inválido")
        
        nuevo_cliente = Cliente(
            id=generate_id(),
            **cliente.dict(),
            fecha_registro=get_current_timestamp()
        )
        db_manager.add_cliente(nuevo_cliente.dict())
        return nuevo_cliente
    
    @staticmethod
    def update_cliente(cliente_id: str, cliente: ClienteCreate) -> Cliente:
        """Actualiza un cliente existente"""
        cliente_existente = db_manager.get_cliente_by_id(cliente_id)
        if not cliente_existente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        cliente_actualizado = Cliente(
            id=cliente_id,
            **cliente.dict(),
            fecha_registro=cliente_existente["fecha_registro"]
        )
        
        success = db_manager.update_cliente(cliente_id, cliente_actualizado.dict())
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        return cliente_actualizado
    
    @staticmethod
    def delete_cliente(cliente_id: str) -> Dict[str, str]:
        """Elimina un cliente"""
        success = db_manager.delete_cliente(cliente_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return {"mensaje": "Cliente eliminado exitosamente"}

class VentaService:
    @staticmethod
    def get_all_ventas() -> List[Venta]:
        """Obtiene todas las ventas"""
        ventas_data = db_manager.get_ventas()
        return [Venta(**venta) for venta in ventas_data]
    
    @staticmethod
    def get_venta_by_id(venta_id: str) -> Venta:
        """Obtiene una venta por su ID"""
        venta_data = db_manager.get_venta_by_id(venta_id)
        if not venta_data:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        return Venta(**venta_data)
    
    @staticmethod
    def create_venta(venta: VentaCreate) -> Venta:
        """Crea una nueva venta"""
        # Validar que el cliente existe
        cliente_existe = db_manager.get_cliente_by_id(venta.cliente_id)
        if not cliente_existe:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Validar productos y calcular total
        total = 0
        for item in venta.items:
            producto = db_manager.get_producto_by_id(item.producto_id)
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
            
            if producto["stock"] < item.cantidad:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto['nombre']}")
            
            total += item.precio_unitario * item.cantidad
        
        # Crear la venta
        nueva_venta = Venta(
            id=generate_id(),
            cliente_id=venta.cliente_id,
            items=venta.items,
            total=total,
            fecha=get_current_timestamp(),
            estado="completada"
        )
        
        # Actualizar stock de productos
        for item in venta.items:
            db_manager.update_producto_stock(item.producto_id, item.cantidad)
        
        db_manager.add_venta(nueva_venta.dict())
        return nueva_venta
    
    @staticmethod
    def get_ventas_by_cliente(cliente_id: str) -> List[Venta]:
        """Obtiene todas las ventas de un cliente específico"""
        ventas_data = db_manager.get_ventas_by_cliente(cliente_id)
        return [Venta(**venta) for venta in ventas_data]

class ReporteService:
    @staticmethod
    def get_ventas_totales() -> ReporteVentas:
        """Genera reporte de ventas totales"""
        ventas = db_manager.get_ventas()
        total_ventas = len(ventas)
        total_ingresos = sum(venta["total"] for venta in ventas)
        promedio_por_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        return ReporteVentas(
            total_ventas=total_ventas,
            total_ingresos=total_ingresos,
            promedio_por_venta=promedio_por_venta
        )
    
    @staticmethod
    def get_productos_populares() -> List[ProductoPopular]:
        """Genera reporte de productos más populares"""
        ventas = db_manager.get_ventas()
        productos = db_manager.get_productos()
        
        # Contar productos vendidos
        productos_vendidos = {}
        for venta in ventas:
            for item in venta["items"]:
                if item["producto_id"] not in productos_vendidos:
                    productos_vendidos[item["producto_id"]] = 0
                productos_vendidos[item["producto_id"]] += item["cantidad"]
        
        # Crear diccionario de nombres de productos
        productos_info = {producto["id"]: producto["nombre"] for producto in productos}
        
        # Crear lista de productos populares
        productos_populares = []
        for producto_id, cantidad in productos_vendidos.items():
            productos_populares.append(ProductoPopular(
                producto_id=producto_id,
                nombre=productos_info.get(producto_id, "Producto desconocido"),
                cantidad_vendida=cantidad
            ))
        
        # Ordenar por cantidad vendida y retornar top 10
        productos_populares.sort(key=lambda x: x.cantidad_vendida, reverse=True)
        return productos_populares[:10] 