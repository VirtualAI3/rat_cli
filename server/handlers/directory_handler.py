import os
from utils.logger import get_console
from utils.validator import validate_path
from config.settings import DIRECTORIES_DIR

class DirectoryHandler:
    """Maneja la transferencia de directorios desde los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_solicitar_directorio(self, ruta_origen, ruta_destino, cliente_id=None):
        """Solicita un directorio desde un cliente."""
        if not validate_path(ruta_origen) or not validate_path(ruta_destino):
            self.console.print("[bold red]Error: Las rutas de origen o destino no son válidas.[/bold red]")
            return False
        
        mensaje = {
            "accion": "enviar_directorio",
            "ruta_origen": ruta_origen,
            "ruta_destino": os.path.join(DIRECTORIES_DIR, os.path.basename(ruta_destino))
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
        self.console.print(f"[bold green]Comando enviado: solicitar directorio '{ruta_origen}' hacia '{ruta_destino}'[/bold green]")
        return True