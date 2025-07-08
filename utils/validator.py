import re
import os
from utils.logger import get_console

console = get_console()

def validate_path(path: str) -> bool:
    """Valida si una ruta tiene un formato básico válido (no verifica existencia real)."""
    if not path or not isinstance(path, str):
        return False
    # Permitir letras, números, espacios, /, \\, :, _, -, .
    pattern = r'^[a-zA-Z0-9_\-\.\\/ :]+$'
    return bool(re.match(pattern, path))

def validate_ip(ip: str) -> bool:
    """Valida si una cadena es una dirección IP válida."""
    if not ip or not isinstance(ip, str):
        return False
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def validate_port(port: int) -> bool:
    """Valida si un puerto está en el rango válido (1-65535)."""
    try:
        port = int(port)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        return False

def validate_extension(ext: str) -> bool:
    """Valida si una extensión es válida (ej. .txt, .png)."""
    if not ext or not isinstance(ext, str):
        return False
    pattern = r'^\.[a-zA-Z0-9]+$'
    return bool(re.match(pattern, ext))

def validate_file_exists(path: str) -> bool:
    """Verifica si un archivo existe en el sistema."""
    return os.path.isfile(path)

def validate_client_spec(client_spec: str) -> bool:
    """Valida si el especificador de cliente es un número o 'all'."""
    if client_spec == "all":
        return True
    try:
        client_id = int(client_spec)
        return client_id > 0
    except (ValueError, TypeError):
        return False