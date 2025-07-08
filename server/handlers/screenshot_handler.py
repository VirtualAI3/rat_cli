import os
from utils.logger import get_console
from utils.validator import validate_path
from config.settings import SCREENSHOTS_DIR

class ScreenshotHandler:
    """Maneja la transferencia de capturas de pantalla desde los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_capturar_pantalla(self, ruta_destino, nombre_archivo=None, cliente_id=None):
        """Solicita una captura de pantalla desde un cliente."""
        if not validate_path(ruta_destino):
            self.console.print("[bold red]Error: La ruta de destino no es válida.[/bold red]")
            return False
        
        if nombre_archivo and not validate_path(nombre_archivo):
            self.console.print("[bold red]Error: El nombre del archivo no es válido.[/bold red]")
            return False
        
        mensaje = {
            "accion": "capturar_pantalla",
            "ruta_destino": os.path.join(SCREENSHOTS_DIR, nombre_archivo or "screenshot.png")
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
        self.console.print(f"[bold green]Comando enviado: capturar pantalla hacia '{mensaje['ruta_destino']}'[/bold green]")
        return True