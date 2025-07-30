#!/usr/bin/env python3
"""
Script de prueba para demostrar el uso de la API del Sistema de Punto de Venta
"""
# NOTA: Asegúrate de que el servidor de la API esté en ejecución antes de correr este script.
# Puedes iniciarlo con `python main.py`.
#
import requests
import json
import time
import sys
import os

# Agregar el directorio raíz al path para importar el módulo app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Iniciando pruebas del Sistema de Punto de Venta")
    print("=" * 50)
    
    # Variables para almacenar IDs
    producto_id = None
    cliente_id = None
    venta_id = None
    
    try:
        # 1. Crear productos
        print("\n📦 Creando productos...")
        productos_data = [
            {
                "nombre": "Laptop HP Pavilion",
                "precio": 1200.00,
                "stock": 15,
                "categoria": "Electrónicos"
            },
            {
                "nombre": "Mouse Inalámbrico",
                "precio": 25.50,
                "stock": 50,
                "categoria": "Accesorios"
            },
            {
                "nombre": "Teclado Mecánico",
                "precio": 89.99,
                "stock": 20,
                "categoria": "Accesorios"
            }
        ]
        
        productos_creados = []
        for producto in productos_data:
            response = requests.post(f"{BASE_URL}/productos", json=producto)
            if response.status_code == 200:
                producto_creado = response.json()
                productos_creados.append(producto_creado)
                print(f"✅ Producto creado: {producto_creado['nombre']} (ID: {producto_creado['id']})")
                if producto_id is None:
                    producto_id = producto_creado['id']
            else:
                print(f"❌ Error creando producto: {response.text}")
        
        # 2. Crear clientes
        print("\n👥 Creando clientes...")
        clientes_data = [
            {
                "nombre": "Juan Pérez",
                "email": "juan.perez@email.com",
                "telefono": "123456789"
            },
            {
                "nombre": "María García",
                "email": "maria.garcia@email.com",
                "telefono": "987654321"
            }
        ]
        
        for cliente in clientes_data:
            response = requests.post(f"{BASE_URL}/clientes", json=cliente)
            if response.status_code == 200:
                cliente_creado = response.json()
                print(f"✅ Cliente creado: {cliente_creado['nombre']} (ID: {cliente_creado['id']})")
                if cliente_id is None:
                    cliente_id = cliente_creado['id']
            else:
                print(f"❌ Error creando cliente: {response.text}")
        
        # 3. Listar productos
        print("\n📋 Listando productos...")
        response = requests.get(f"{BASE_URL}/productos")
        if response.status_code == 200:
            productos = response.json()
            print(f"✅ Total de productos: {len(productos)}")
            for producto in productos:
                print(f"   - {producto['nombre']}: ${producto['precio']} (Stock: {producto['stock']})")
        
        # 4. Listar clientes
        print("\n👥 Listando clientes...")
        response = requests.get(f"{BASE_URL}/clientes")
        if response.status_code == 200:
            clientes = response.json()
            print(f"✅ Total de clientes: {len(clientes)}")
            for cliente in clientes:
                print(f"   - {cliente['nombre']}: {cliente['email']}")
        
        # 5. Crear venta
        print("\n💰 Creando venta...")
        if producto_id and cliente_id:
            venta_data = {
                "cliente_id": cliente_id,
                "items": [
                    {
                        "producto_id": producto_id,
                        "cantidad": 1,
                        "precio_unitario": 1200.00
                    }
                ]
            }
            
            response = requests.post(f"{BASE_URL}/ventas", json=venta_data)
            if response.status_code == 200:
                venta_creada = response.json()
                venta_id = venta_creada['id']
                print(f"✅ Venta creada: ID {venta_id}, Total: ${venta_creada['total']}")
            else:
                print(f"❌ Error creando venta: {response.text}")
        
        # 6. Listar ventas
        print("\n📊 Listando ventas...")
        response = requests.get(f"{BASE_URL}/ventas")
        if response.status_code == 200:
            ventas = response.json()
            print(f"✅ Total de ventas: {len(ventas)}")
            for venta in ventas:
                print(f"   - Venta {venta['id'][:8]}...: ${venta['total']} ({venta['estado']})")
        
        # 7. Obtener reportes
        print("\n📈 Obteniendo reportes...")
        
        # Reporte de ventas totales
        response = requests.get(f"{BASE_URL}/reportes/ventas-totales")
        if response.status_code == 200:
            reporte = response.json()
            print(f"✅ Reporte de ventas:")
            print(f"   - Total de ventas: {reporte['total_ventas']}")
            print(f"   - Total de ingresos: ${reporte['total_ingresos']:.2f}")
            print(f"   - Promedio por venta: ${reporte['promedio_por_venta']:.2f}")
        
        # Reporte de productos populares
        response = requests.get(f"{BASE_URL}/reportes/productos-populares")
        if response.status_code == 200:
            productos_populares = response.json()
            print(f"✅ Productos más populares:")
            for i, producto in enumerate(productos_populares, 1):
                print(f"   {i}. {producto['nombre']}: {producto['cantidad_vendida']} unidades")
        
        # 8. Verificar stock actualizado
        print("\n📦 Verificando stock actualizado...")
        response = requests.get(f"{BASE_URL}/productos/{producto_id}")
        if response.status_code == 200:
            producto = response.json()
            print(f"✅ Stock actualizado para {producto['nombre']}: {producto['stock']}")
        
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. Asegúrate de que esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_api() 