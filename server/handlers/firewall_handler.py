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
            "nombre": nombre,
            "ip": ip,
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
        
        self.console.print(f"[bold green]Comando enviado: agregar regla '{nombre}'[/bold green]")
        return True