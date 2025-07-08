from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser
from utils.logger import get_console
from utils.formatter import format_clients

@with_default_category("Comandos de Gestión")
class ListClientsCommand(CommandSet):
    """Comando para listar los clientes conectados."""
    
    list_clients_parser = Cmd2ArgumentParser(description="Muestra una lista de todos los clientes conectados.")

    def do_list_clients(self, statement):
        """Muestra una lista de todos los clientes conectados.
        Uso: list_clients
        Ejemplo: list_clients"""
        console = get_console()
        
        # Obtener lista de clientes
        clients = self._cmd.client_manager.obtener_info_clientes()
        
        # Verificar si hay clientes conectados
        if not clients:
            console.print("[bold yellow]No hay clientes conectados.[/bold yellow]")
            return
        
        # Mostrar tabla de clientes
        try:
            formatted = format_clients(clients)
            console.print(formatted)
        except Exception as e:
            console.print(f"[bold red]Error al mostrar clientes: {e}[/bold red]")
