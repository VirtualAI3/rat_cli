from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_client_spec, validate_extension

@with_default_category("Comandos de Transferencia")
class GetFilesByExtensionCommand(CommandSet):
    """Comando para solicitar archivos por extensión desde los clientes."""
    
    get_files_parser = Cmd2ArgumentParser(description="Solicita archivos por extensión desde uno o todos los clientes.")
    get_files_parser.add_argument("--dir", type=str, required=True, help="Directorio en el cliente donde buscar")
    get_files_parser.add_argument("--ext", type=str, required=True, help="Extensión de archivo (ej. .txt)")
    get_files_parser.add_argument("--dest", type=str, required=True, help="Ruta de destino en el servidor")
    get_files_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(get_files_parser)
    def do_get_files_by_extension(self, args):
        """Solicita archivos por extensión desde los clientes.
        Uso: get_files_by_extension --dir <ruta_directorio> --ext <extensión> --dest <ruta_destino> [--client <ID|all>]
        Ejemplo: get_files_by_extension --dir /home/user/docs --ext .txt --dest received_files/txt_files --client 1"""
        console = get_console()
        
        # Validar directorio y destino
        if not validate_path(args.dir) or not validate_path(args.dest):
            console.print("[bold red]Error: Las rutas de directorio y destino deben ser válidas.[/bold red]")
            return
        
        # Validar extensión
        if not validate_extension(args.ext):
            console.print("[bold red]Error: La extensión debe ser válida (ej. .txt).[/bold red]")
            return
        
        # Validar número de clientes conectados
        if not self._cmd.client_manager.obtener_clientes_conectados():
            console.print("[bold red]Error: No hay clientes conectados.[/bold red]")
            return
        
        # Validar ID del cliente
        cliente_id = None
        if args.client != "all":
            if not validate_client_spec(args.client):
                console.print("[bold red]Error: ID de cliente debe ser un número o 'all'.[/bold red]")
                return
            try:
                cliente_id = int(args.client)
                if not self._cmd.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                    console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                    return
            except ValueError:
                console.print("[bold red]Error: ID de cliente no válido.[/bold red]")
                return
        
        # Enviar comando
        try:
            self._cmd.client_manager.enviar_comando_archivos_por_extension(args.dir, args.ext, args.dest, cliente_id)
            console.print(f"[bold green]Comando enviado: solicitar archivos con extensión '{args.ext}' desde '{args.dir}' hacia '{args.dest}'[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
