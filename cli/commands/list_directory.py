from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path
import time

@with_default_category("Comandos de Directorio")
class ListDirectoryCommand(CommandSet):
    """Comando para listar el contenido de un directorio en los clientes."""
    
    list_directory_parser = Cmd2ArgumentParser(description="Lista el contenido de un directorio en uno o todos los clientes.")
    list_directory_parser.add_argument("path", type=str, help="Ruta del directorio a listar")
    list_directory_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")
    list_directory_parser.add_argument("--files", action="store_true", help="Incluir archivos en el listado")

    @with_argparser(list_directory_parser)
    def do_list_directory(self, args):
        """Lista el contenido de un directorio en los clientes.
        Uso: list_directory <ruta> [--client <ID|all>] [--files]
        Ejemplo: list_directory /home/user --client 1 --files"""
        console = get_console()
        
        # Validar ruta
        if not args.path or not validate_path(args.path):
            console.print("[bold red]Error: Debe especificar una ruta válida.[/bold red]")
            return
        
        # Validar número de clientes conectados
        if not self._cmd.client_manager.obtener_clientes_conectados():
            console.print("[bold red]Error: No hay clientes conectados.[/bold red]")
            return
        
        # Validar ID del cliente
        cliente_id = None
        if args.client != "all":
            try:
                cliente_id = int(args.client)
                if not self._cmd.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                    console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                    return
            except ValueError:
                console.print("[bold red]Error: ID de cliente debe ser un número o 'all'.[/bold red]")
                return
        
        # Enviar comando
        try:
            console.print(f"[bold green]Comando enviado: listar directorio '{args.path}' {'con archivos' if args.files else 'sin archivos'}[/bold green]")

            resultado = self._cmd.client_manager.enviar_comando_listar_directorio(args.path, args.files, cliente_id)
            if resultado:
                console.print(resultado)
            
            #time.sleep(3.0)
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
