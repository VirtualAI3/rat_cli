import os
from utils.logger import get_console
from utils.validator import validate_path
from config.settings import DIRECTORIES_DIR
import tempfile
import zipfile
import base64

class DirectoryHandler:
    """Maneja la transferencia de directorios desde los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_solicitar_directorio(self, ruta_origen, ruta_destino=None, cliente_id=None):
        """Solicita un directorio desde un cliente."""
        if not validate_path(ruta_origen):
            self.console.print("[bold red]Error: La ruta de origen debe se válida.[/bold red]")
            return False
        
        if not ruta_destino:
            ruta_destino_final = os.path.normpath(DIRECTORIES_DIR)
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
            "accion": "enviar_directorio",
            "ruta_origen": ruta_origen,
            "ruta_destino": ruta_destino_final
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
        self.console.print(f"[bold green]Comando enviado: solicitar directorio '{ruta_origen}' hacia '{ruta_destino_final}'[/bold green]")
        return True
    
    def enviar_comando_eliminar(self, ruta, cliente_id=None):
        # Validar ruta
        if not ruta or not validate_path(ruta):
            self.console.print("[bold red]Error: Ruta no válida para eliminación.[/bold red]")
            return False
        
        mensaje = {
            "accion": "eliminar",
            "ruta": ruta
        }
        
        # Verificar si cliente existe si se especifica uno
        if cliente_id is not None:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        else:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
            
        self.console.print(f"[bold green]Comando de eliminación enviado para '{ruta}'[/bold green]")
        return True
            
    def enviar_comando_listar_directorio(self, ruta, incluir_archivos=False, cliente_id=None):
        """Envía comando para listar un directorio."""

        # Validar ruta
        if not ruta or not validate_path(ruta):
            self.console.print("[bold red]Error: Ruta no válida.[/bold red]")
            return False

        mensaje = {
            "accion": "listar_directorio",
            "ruta": ruta,
            "incluir_archivos": incluir_archivos
        }

        # Enviar comando según cliente
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.client_manager.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)

        self.console.print(f"[bold green]Comando enviado: listar directorio '{ruta}' {'con archivos' if incluir_archivos else 'sin archivos'}[/bold green]")
        return True
    
    def _procesar_directorio_enviado(self, datos_dict, cliente_id):
        """Procesa un directorio enviado como ZIP."""
        nombre_directorio = datos_dict.get("nombre_directorio")
        ruta_destino = datos_dict.get("ruta_destino", DIRECTORIES_DIR)
        datos_zip = datos_dict.get("datos_zip")
        ruta_origen = datos_dict.get("ruta_origen")
        
        try:
            cliente_formateado = f"cliente_{cliente_id.replace('[Cliente ', '').replace(']', '')}"
            
            ruta_destino_cliente = os.path.join(ruta_destino, cliente_formateado)
            ruta_destino_completa = os.path.join(ruta_destino_cliente, nombre_directorio)
            os.makedirs(ruta_destino_completa, exist_ok=True)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                temp_zip_path = temp_zip.name
                temp_zip.write(base64.b64decode(datos_zip))
            
            with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
                zipf.extractall(ruta_destino_completa)
            
            os.unlink(temp_zip_path)
            
            self.console.print(f"\n{cliente_id} [bold green]Directorio recibido y extraído en:[/bold green] {ruta_destino_completa}")
            self.console.print(f"{cliente_id} Directorio origen: {ruta_origen}")
        except Exception as e:
            self.console.print(f"\n{cliente_id} [bold red]Error al procesar directorio:[/bold red] {str(e)}")
            
    def _procesar_eliminacion_exitosa(self, datos_dict, cliente_id):
        """Procesa una eliminación exitosa."""
        tipo_elemento = datos_dict.get("tipo", "elemento")
        ruta_eliminada = datos_dict.get("ruta")
        mensaje = datos_dict.get("mensaje")
        
        self.console.print(f"\n{cliente_id} [bold green]✅ Eliminación exitosa:[/bold green]")
        self.console.print(f"{cliente_id} Tipo: {tipo_elemento.capitalize()}")
        self.console.print(f"{cliente_id} Ruta: {ruta_eliminada}")
        self.console.print(f"{cliente_id} {mensaje}")