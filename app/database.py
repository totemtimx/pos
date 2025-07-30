import json
import os
from typing import Dict, List, Any, Optional

from .config import settings

class DatabaseManager:
    def __init__(self, db_file: str = None):
        self.db_file = db_file or settings.get_database_url()
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Asegura que el archivo de base de datos existe con la estructura correcta"""
        if not os.path.exists(self.db_file):
            initial_data = {
                "productos": [],
                "clientes": [],
                "ventas": []
            }
            self.save_database(initial_data)
    
    def load_database(self) -> Dict[str, List[Any]]:
        """Carga la base de datos desde el archivo JSON"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si hay error, crear una nueva base de datos
            initial_data = {
                "productos": [],
                "clientes": [],
                "ventas": []
            }
            self.save_database(initial_data)
            return initial_data
    
    def save_database(self, data: Dict[str, List[Any]]) -> None:
        """Guarda la base de datos en el archivo JSON"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_productos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los productos"""
        db = self.load_database()
        return db["productos"]
    
    def get_producto_by_id(self, producto_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un producto por su ID"""
        productos = self.get_productos()
        for producto in productos:
            if producto["id"] == producto_id:
                return producto
        return None
    
    def add_producto(self, producto: Dict[str, Any]) -> None:
        """Agrega un nuevo producto"""
        db = self.load_database()
        db["productos"].append(producto)
        self.save_database(db)
    
    def update_producto(self, producto_id: str, producto_data: Dict[str, Any]) -> bool:
        """Actualiza un producto existente"""
        db = self.load_database()
        for i, producto in enumerate(db["productos"]):
            if producto["id"] == producto_id:
                producto_data["id"] = producto_id
                producto_data["fecha_creacion"] = producto["fecha_creacion"]
                db["productos"][i] = producto_data
                self.save_database(db)
                return True
        return False
    
    def delete_producto(self, producto_id: str) -> bool:
        """Elimina un producto"""
        db = self.load_database()
        for i, producto in enumerate(db["productos"]):
            if producto["id"] == producto_id:
                del db["productos"][i]
                self.save_database(db)
                return True
        return False
    
    def get_clientes(self) -> List[Dict[str, Any]]:
        """Obtiene todos los clientes"""
        db = self.load_database()
        return db["clientes"]
    
    def get_cliente_by_id(self, cliente_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un cliente por su ID"""
        clientes = self.get_clientes()
        for cliente in clientes:
            if cliente["id"] == cliente_id:
                return cliente
        return None
    
    def add_cliente(self, cliente: Dict[str, Any]) -> None:
        """Agrega un nuevo cliente"""
        db = self.load_database()
        db["clientes"].append(cliente)
        self.save_database(db)
    
    def update_cliente(self, cliente_id: str, cliente_data: Dict[str, Any]) -> bool:
        """Actualiza un cliente existente"""
        db = self.load_database()
        for i, cliente in enumerate(db["clientes"]):
            if cliente["id"] == cliente_id:
                cliente_data["id"] = cliente_id
                cliente_data["fecha_registro"] = cliente["fecha_registro"]
                db["clientes"][i] = cliente_data
                self.save_database(db)
                return True
        return False
    
    def delete_cliente(self, cliente_id: str) -> bool:
        """Elimina un cliente"""
        db = self.load_database()
        for i, cliente in enumerate(db["clientes"]):
            if cliente["id"] == cliente_id:
                del db["clientes"][i]
                self.save_database(db)
                return True
        return False
    
    def get_ventas(self) -> List[Dict[str, Any]]:
        """Obtiene todas las ventas"""
        db = self.load_database()
        return db["ventas"]
    
    def get_venta_by_id(self, venta_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una venta por su ID"""
        ventas = self.get_ventas()
        for venta in ventas:
            if venta["id"] == venta_id:
                return venta
        return None
    
    def add_venta(self, venta: Dict[str, Any]) -> None:
        """Agrega una nueva venta"""
        db = self.load_database()
        db["ventas"].append(venta)
        self.save_database(db)
    
    def get_ventas_by_cliente(self, cliente_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las ventas de un cliente específico"""
        ventas = self.get_ventas()
        return [venta for venta in ventas if venta["cliente_id"] == cliente_id]
    
    def update_producto_stock(self, producto_id: str, cantidad: int) -> bool:
        """Actualiza el stock de un producto"""
        db = self.load_database()
        for producto in db["productos"]:
            if producto["id"] == producto_id:
                producto["stock"] -= cantidad
                self.save_database(db)
                return True
        return False

# Instancia global del gestor de base de datos
db_manager = DatabaseManager() 