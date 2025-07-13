import os
import base64
from utils.logger import get_console
from utils.validator import validate_path, validate_file_exists
from config.settings import RECEIVED_FILES_DIR

class FileHandler:
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()

    def _enviar_mensaje(self, mensaje, cliente_id=None):
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        return True

    def enviar_comando_solicitar_archivo(self, ruta_origen, ruta_destino=None, cliente_id=None):
        if not validate_path(ruta_origen):
            self.console.print("[bold red]Error: Ruta de origen no válida.[/bold red]")
            return False

        if not ruta_destino:
            ruta_destino_final = os.path.normpath(RECEIVED_FILES_DIR)
        else:
            # Validar ruta_destino
            if not validate_path(ruta_destino):
                self.console.print("[bold red]Error: La ruta de destino no es válida.[/bold red]")
                return False
            
            # Determinar si es ruta absoluta o relativa
            if os.path.isabs(ruta_destino):
                ruta_destino_final = os.path.normpath(ruta_destino)
            else:
                from config.settings import DATA_DIR
                ruta_destino_final = os.path.normpath(os.path.join(DATA_DIR, ruta_destino))

        mensaje = {
            "accion": "enviar_archivo",
            "ruta_origen": ruta_origen,
            "ruta_destino": ruta_destino_final
        }
        
        self.console.print(f"[bold green] Archivo solicitado de la ruta {ruta_origen} del o de los clientes[/bold green]")

        return self._enviar_mensaje(mensaje, cliente_id)

    def enviar_archivo_a_clientes(self, ruta_origen, ruta_destino, cliente_id=None):
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

            if self._enviar_mensaje(mensaje, cliente_id):
                self.console.print(f"[bold green]Archivo enviado: {ruta_origen}[/bold green]")
                return True

        except Exception as e:
            self.console.print(f"[bold red]Error al enviar archivo: {e}[/bold red]")

        return False
    
    def _procesar_archivo_enviado(self, datos_dict, cliente_id):
        """Procesa un archivo enviado por el cliente."""
        nombre_archivo = datos_dict.get("nombre_archivo")
        ruta_destino = datos_dict.get("ruta_destino", os.path.join(RECEIVED_FILES_DIR, nombre_archivo))
        datos_archivo = datos_dict.get("datos_archivo")
        
        directorio = os.path.dirname(ruta_destino)
        os.makedirs(directorio, exist_ok=True)
        
        with open(ruta_destino, "wb") as f:
            f.write(base64.b64decode(datos_archivo))
        
        self.console.print(f"\n{cliente_id} [bold green]Archivo recibido y guardado en:[/bold green] {ruta_destino}")