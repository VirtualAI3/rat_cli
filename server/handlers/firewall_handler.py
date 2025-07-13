from utils.logger import get_console
from utils.validator import validate_path, validate_ip, validate_port, validate_client_spec

class FirewallHandler:
    """Maneja la adición de reglas de firewall en los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_agregar_regla(self, nombre, ip, puerto, accion, cliente_id=None):
        """Envía un comando para agregar una regla de firewall en los clientes."""
        if not validate_path(nombre):
            self.console.print("[bold red]Error: El nombre de la regla no es válido.[/bold red]")
            return False
        
        if ip and not validate_ip(ip):
            self.console.print("[bold red]Error: La dirección IP no es válida.[/bold red]")
            return False
        
        if not validate_port(puerto):
            self.console.print("[bold red]Error: El puerto debe estar entre 1 y 65535.[/bold red]")
            return False
        
        if accion not in ["allow", "block"]:
            self.console.print("[bold red]Error: La acción debe ser 'allow' o 'block'.[/bold red]")
            return False
        
        mensaje = {
            "accion": "agregar_regla_firewall",
            "nombre_regla": nombre,
            "ip": ip or 'any',
            "puerto": puerto,
            "accion_firewall": accion
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not validate_client_spec(str(cliente_id)):
                self.console.print("[bold red]Error: ID de cliente no válido.[/bold red]")
                return False
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        return True
    
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