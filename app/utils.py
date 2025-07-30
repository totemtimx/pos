import uuid
from datetime import datetime
from typing import Dict, Any

def generate_id() -> str:
    """Genera un ID único"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Obtiene el timestamp actual en formato ISO"""
    return datetime.now().isoformat()

def format_currency(amount: float) -> str:
    """Formatea una cantidad como moneda"""
    return f"${amount:.2f}"

def validate_email(email: str) -> bool:
    """Valida formato básico de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Valida formato básico de teléfono"""
    import re
    # Acepta números, espacios, guiones y paréntesis
    pattern = r'^[\d\s\-\(\)\+]+$'
    return re.match(pattern, phone) is not None

def calculate_total(items: list) -> float:
    """Calcula el total de una lista de items"""
    return sum(item.get('precio_unitario', 0) * item.get('cantidad', 0) for item in items)

def format_response(data: Any, message: str = "Operación exitosa", success: bool = True) -> Dict[str, Any]:
    """Formatea una respuesta estándar de la API"""
    return {
        "success": success,
        "message": message,
        "data": data,
        "timestamp": get_current_timestamp()
    }

def paginate_results(items: list, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Pagina una lista de resultados"""
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    
    paginated_items = items[start_index:end_index]
    
    return {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    } 