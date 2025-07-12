from utils.logger import get_console
from utils.validator import validate_client_spec

class CommandHandler:
    """Maneja la ejecución de comandos en los clientes."""
    
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
    
    def enviar_comando_ejecutar(self, codigo, cliente_id=None):
        """Envía un comando para ejecutar en los clientes."""
        if not codigo or not isinstance(codigo, str):
            self.console.print("[bold red]Error: El comando debe ser una cadena válida.[/bold red]")
            return False
        
        mensaje = {
            "accion": "ejecutar",
            "codigo": codigo
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
        
        self.console.print(f"[bold green]Código para ejecutar en la maquina/maquinas del cliente/clientes:\n'{codigo}'[/bold green]")
        return True