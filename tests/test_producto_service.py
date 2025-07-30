import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.services import ProductoService
from app.models import ProductoCreate, Producto


class TestProductoService(unittest.TestCase):
    def setUp(self):
        self.example_data = {
            'id': '1',
            'nombre': 'TestProducto',
            'precio': 9.99,
            'stock': 5,
            'categoria': 'CategoriaTest',
            'fecha_creacion': '2021-01-01T00:00:00'
        }

    @patch('app.services.db_manager')
    def test_get_all_productos(self, mock_db):
        mock_db.get_productos.return_value = [self.example_data]
        result = ProductoService.get_all_productos()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        producto = result[0]
        self.assertIsInstance(producto, Producto)
        self.assertEqual(producto.id, self.example_data['id'])

    @patch('app.services.db_manager')
    def test_get_producto_by_id_success(self, mock_db):
        mock_db.get_producto_by_id.return_value = self.example_data
        producto = ProductoService.get_producto_by_id('1')
        self.assertIsInstance(producto, Producto)
        self.assertEqual(producto.nombre, self.example_data['nombre'])

    @patch('app.services.db_manager')
    def test_get_producto_by_id_not_found(self, mock_db):
        mock_db.get_producto_by_id.return_value = None
        with self.assertRaises(HTTPException) as ctx:
            ProductoService.get_producto_by_id('missing')
        self.assertEqual(ctx.exception.status_code, 404)

    @patch('app.services.get_current_timestamp', return_value='ts')
    @patch('app.services.generate_id', return_value='id1')
    @patch('app.services.db_manager')
    def test_create_producto(self, mock_db, mock_id, mock_ts):
        data = {'nombre': 'New', 'precio': 1.0, 'stock': 2, 'categoria': 'Cat'}
        create = ProductoCreate(**data)
        producto = ProductoService.create_producto(create)
        self.assertEqual(producto.id, 'id1')
        self.assertEqual(producto.fecha_creacion, 'ts')
        mock_db.add_producto.assert_called_once()
        saved = mock_db.add_producto.call_args[0][0]
        for key in ['id', 'nombre', 'precio', 'stock', 'categoria', 'fecha_creacion']:
            self.assertIn(key, saved)

    @patch('app.services.db_manager')
    def test_update_producto_success(self, mock_db):
        existing = dict(self.example_data)
        mock_db.get_producto_by_id.return_value = existing
        mock_db.update_producto.return_value = True
        data = {'nombre': 'Mod', 'precio': 2.0, 'stock': 3, 'categoria': 'C'}
        create = ProductoCreate(**data)
        producto = ProductoService.update_producto('1', create)
        self.assertEqual(producto.id, '1')
        self.assertEqual(producto.nombre, 'Mod')
        mock_db.update_producto.assert_called_once_with('1', producto.dict())

    @patch('app.services.db_manager')
    def test_update_producto_not_found(self, mock_db):
        mock_db.get_producto_by_id.return_value = None
        data = {'nombre': 'M', 'precio': 0.0, 'stock': 0, 'categoria': 'C'}
        create = ProductoCreate(**data)
        with self.assertRaises(HTTPException) as ctx:
            ProductoService.update_producto('x', create)
        self.assertEqual(ctx.exception.status_code, 404)

    @patch('app.services.db_manager')
    def test_delete_producto_success(self, mock_db):
        mock_db.delete_producto.return_value = True
        result = ProductoService.delete_producto('1')
        self.assertEqual(result, {'mensaje': 'Producto eliminado exitosamente'})

    @patch('app.services.db_manager')
    def test_delete_producto_not_found(self, mock_db):
        mock_db.delete_producto.return_value = False
        with self.assertRaises(HTTPException) as ctx:
            ProductoService.delete_producto('1')
        self.assertEqual(ctx.exception.status_code, 404)
