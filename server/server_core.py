import socket
import threading
import json
import time
from utils.logger import get_console
from server.client_manager import ClientManager
from rich.console import Console

class ServidorSocket:
    """Servidor socket para manejar conexiones de clientes."""
    
    def __init__(self, host='0.0.0.0', puerto=5555):
        self.host = host
        self.puerto = puerto
        self.socket_servidor = None
        self.clientes = []  # Lista de dicts: {"id": int, "socket": socket, "direccion": tuple, "ultimo_contacto": float}
        self.ejecutando = False
        self.contador_ids = 0
        self.console = get_console()
        self.client_manager = None
        self.cli_instance =None
    
    def establecer_client_manager(self, client_manager: ClientManager):
        """Establece el administrador de clientes."""
        self.client_manager = client_manager
    
    def establecer_cli_instance(self, cli_instance):
        """Establece la referencia a la instancia CLI."""
        self.cli_instance = cli_instance
    
    def _print_with_prompt_refresh(self, message):
        """Imprime un mensaje y refresca el prompt correctamente."""
        if self.cli_instance:
            # Usar el método async_alert de cmd2 para notificaciones no intrusivas
            self.cli_instance.async_alert(message)
        else:
            # Fallback al método tradicional
            self.console.print(message)
    def iniciar(self, host, puerto):
        self.host = host
        self.puerto = puerto
        try:
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ejecutando = True
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind((self.host, self.puerto))
            self.socket_servidor.listen(5)
            self.console.print(f"[bold green][+] Servidor iniciado en {self.host}:{self.puerto}[/bold green]")
            threading.Thread(target=self.aceptar_conexiones, daemon=True).start()
        except Exception as e:
            self.console.print(f"[bold red][!] Error al iniciar el servidor: {e}[/bold red]")
            raise
    
    def aceptar_conexiones(self):
        """Acepta nuevas conexiones de clientes."""
        while self.ejecutando:
            try:
                cliente_socket, direccion = self.socket_servidor.accept()
                self.contador_ids += 1
                info_cliente = {
                    "id": self.contador_ids,
                    "socket": cliente_socket,
                    "direccion": direccion,
                    "ultimo_contacto": time.time()
                }
                self.clientes.append(info_cliente)
                self._print_with_prompt_refresh(
                    f"[+] Nueva conexión desde {direccion[0]}:{direccion[1]} (ID {self.contador_ids})"
                )
                threading.Thread(target=self.manejar_cliente, args=(info_cliente,), daemon=True).start()
            except socket.error:
                if not self.ejecutando:
                    break
            except Exception as e:
                if self.ejecutando:
                    self.console.print(f"[bold red][!] Error al aceptar conexión: {e}[/bold red]")
    
    def manejar_cliente(self, cliente):
        """Maneja la comunicación con un cliente."""
        cliente_socket = cliente["socket"]
        try:
            while self.ejecutando:
                datos = self.recibir_mensaje(cliente_socket)
                if not datos:
                    break
                if self.client_manager:
                    self.client_manager.procesar_respuesta_cliente(datos, cliente)
                cliente["ultimo_contacto"] = time.time()
        except ConnectionResetError:
            self.console.print(f"[bold yellow][!] Conexión cerrada por cliente {cliente['direccion'][0]}:{cliente['direccion'][1]} (ID {cliente['id']})[/bold yellow]")
        except Exception as e:
            if self.ejecutando:
                self.console.print(f"[bold red][!] Error al manejar cliente {cliente['direccion'][0]} (ID {cliente['id']}): {e}[/bold red]")
        finally:
            self.remover_cliente(cliente)
    
    def remover_cliente(self, cliente):
        """Remueve un cliente desconectado."""
        if cliente in self.clientes:
            self.clientes.remove(cliente)
            try:
                cliente["socket"].close()
            except:
                pass
            if self.ejecutando:
                self.console.print(f"[bold yellow][-] Cliente ID {cliente['id']} ({cliente['direccion'][0]}:{cliente['direccion'][1]}) desconectado[/bold yellow]")
    
    def enviar_mensaje(self, cliente_socket, mensaje):
        """Envía un mensaje a un cliente."""
        try:
            if isinstance(mensaje, dict):
                mensaje = json.dumps(mensaje)
            longitud = len(mensaje.encode())
            cliente_socket.send(longitud.to_bytes(4, byteorder='big'))
            cliente_socket.send(mensaje.encode())
            return True
        except Exception as e:
            self.console.print(f"[bold red][!] Error al enviar mensaje: {e}[/bold red]")
            return False
    
    def recibir_mensaje(self, cliente_socket):
        """Recibe un mensaje de un cliente."""
        try:
            longitud_bytes = cliente_socket.recv(4)
            if not longitud_bytes:
                return None
            longitud = int.from_bytes(longitud_bytes, byteorder='big')
            chunks = []
            bytes_recibidos = 0
            while bytes_recibidos < longitud:
                chunk = cliente_socket.recv(min(longitud - bytes_recibidos, 4096))
                if not chunk:
                    return None
                chunks.append(chunk)
                bytes_recibidos += len(chunk)
            return b''.join(chunks).decode()
        except Exception as e:
            if self.ejecutando:
                self.console.print(f"[bold red][!] Error al recibir mensaje: {e}[/bold red]")
            return None
    
    def enviar_comando_todos(self, comando):
        """Envía un comando a todos los clientes."""
        clientes_desconectados = []
        for cliente in self.clientes:
            try:
                if not self.enviar_mensaje(cliente["socket"], comando):
                    clientes_desconectados.append(cliente)
            except Exception:
                clientes_desconectados.append(cliente)
        for cliente in clientes_desconectados:
            self.remover_cliente(cliente)
    
    def enviar_comando_cliente(self, cliente_id, comando):
        """Envía un comando a un cliente específico."""
        cliente = next((c for c in self.clientes if c["id"] == cliente_id), None)
        if cliente:
            try:
                if self.enviar_mensaje(cliente["socket"], comando):
                    return True
                else:
                    self.remover_cliente(cliente)
                    return False
            except Exception:
                self.remover_cliente(cliente)
                return False
        else:
            self.console.print(f"[bold red][!] Error: Cliente con ID {cliente_id} no encontrado.[/bold red]")
            return False
    
    def obtener_cliente_por_id(self, cliente_id):
        """Obtiene un cliente por su ID."""
        return next((c for c in self.clientes if c["id"] == cliente_id), None)
    
    def cerrar(self):
        """Cierra el servidor y todas las conexiones."""
        self.ejecutando = False
        clientes_a_cerrar = self.clientes[:]
        for cliente in clientes_a_cerrar:
            try:
                cliente["socket"].close()
            except:
                pass
        self.clientes.clear()
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass
        self.console.print("[bold green][+] Servidor cerrado[/bold green]")