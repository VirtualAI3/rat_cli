import os
import base64
from utils.logger import get_console
from utils.validator import validate_path, validate_file_exists
from config.settings import RECEIVED_FILES_DIR

class FileHandler:
    """Maneja la transferencia de archivos entre servidor y clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_solicitar_archivo(self, ruta_origen, ruta_destino, cliente_id=None):
        """Solicita un archivo desde un cliente."""
        if not validate_path(ruta_origen) or not validate_path(ruta_destino):
            self.console.print("[bold red]Error: Rutas de origen o destino no válidas.[/bold red]")
            return False
        
        mensaje = {
            "accion": "enviar_archivo",
            "ruta_origen": ruta_origen,
            "ruta_destino": os.path.join(RECEIVED_FILES_DIR, os.path.basename(ruta_destino))
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
        return True
    
    def enviar_archivo_a_clientes(self, ruta_origen, ruta_destino, cliente_id=None):
        """Envía un archivo desde el servidor a los clientes."""
        if not validate_file_exists(ruta_origen):
            self.console.print(f"[bold red]Error: El archivo no existe: {ruta_origen}[/bold red]")
            return False
        
        if not validate_path(ruta_destino):
            self.console.print("[bold red]Error: Ruta de destino no válida.[/bold red]")
            return False
        
        try:
            with open(ruta_origen, "rb") as f:
                datos_archivo = base64.b64encode(f.read()).decode()
            
            nombre_archivo = os.path.basename(ruta_origen)
            mensaje = {
                "accion": "recibir_archivo",
                "nombre_archivo": nombre_archivo,
                "ruta_destino": os.path.join(ruta_destino, nombre_archivo),
                "datos_archivo": datos_archivo
            }
            
            if cliente_id is None:
                self.client_manager.servidor.enviar_comando_todos(mensaje)
            else:
                if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                    self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                    return False
                self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
            
            self.console.print(f"[bold green]Archivo enviado: {ruta_origen}[/bold green]")
            return True
        except Exception as e:
            self.console.print(f"[bold red]Error al enviar archivo: {e}[/bold red]")
            return False