import os
from typing import Optional

class Settings:
    """Configuraciones de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Sistema de Punto de Venta"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API completa para gestión de productos, clientes, ventas y reportes"
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    
    # Configuración de la base de datos
    DATABASE_FILE: str = os.getenv("DATABASE_FILE", "pos_database.json")
    
    # Configuración de CORS
    CORS_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "*"  # En producción, especificar dominios específicos
    ]
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu-clave-secreta-aqui")
    
    @classmethod
    def get_database_url(cls) -> str:
        """Obtiene la URL de la base de datos"""
        return cls.DATABASE_FILE
    
    @classmethod
    def is_development(cls) -> bool:
        """Verifica si estamos en modo desarrollo"""
        return os.getenv("ENVIRONMENT", "development").lower() == "development"
    
    @classmethod
    def is_production(cls) -> bool:
        """Verifica si estamos en modo producción"""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"

# Instancia global de configuración
settings = Settings() 