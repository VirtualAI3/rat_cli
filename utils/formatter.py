from rich.table import Table
from rich.console import Console
from utils.logger import get_console

def format_clients(clients):
    """Formatea la lista de clientes conectados como una tabla."""
    console = get_console()
    table = Table(title="[bold green]Clientes Conectados[/bold green]")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("IP", style="green")
    table.add_column("Puerto", style="yellow")
    
    for id_cliente, ip, puerto in clients:
        table.add_row(str(id_cliente), ip, str(puerto))
    
    console.print(table)
    console.print(f"[bold green]Total: {len(clients)} clientes[/bold green]")

def format_error(message):
    """Formatea un mensaje de error."""
    console = get_console()
    console.print(f"[bold red]Error: {message}[/bold red]")

def format_success(message):
    """Formatea un mensaje de éxito."""
    console = get_console()
    console.print(f"[bold green]Éxito: {message}[/bold green]")