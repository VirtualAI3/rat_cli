from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_file_exists, validate_client_spec
from server.handlers.file_handler import FileHandler

@with_default_category("Comandos de Transferencia")
class SendFileCommand(CommandSet):
    """Comando para enviar un archivo a los clientes."""
    
    send_file_parser = Cmd2ArgumentParser(description="Envía un archivo desde el servidor a uno o todos los clientes.")
    send_file_parser.add_argument("--source", type=str, required=True, help="Ruta del archivo en el servidor")
    send_file_parser.add_argument("--dest", type=str, required=True, help="Ruta de destino en el cliente")
    send_file_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(send_file_parser)
    def do_send_file(self, args):
        """Envía un archivo a los clientes.
        Uso: send_file --source <ruta_origen> --dest <ruta_destino> [--client <ID|all>]
        Ejemplo: send_file --source local/doc.txt --dest /home/user/doc.txt --client 1"""
        console = get_console()
        
        # Validar rutas y existencia del archivo
        if not validate_path(args.source) or not validate_path(args.dest):
            console.print("[bold red]Error: Las rutas de origen y destino deben ser válidas.[/bold red]")
            return
        if not validate_file_exists(args.source):
            console.print(f"[bold red]Error: El archivo '{args.source}' no existe.[/bold red]")
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
            file_handler = FileHandler(self._cmd.client_manager)
            if file_handler.enviar_archivo_a_clientes(args.source, args.dest, cliente_id):
                console.print(f"[bold green]Comando enviado: enviar archivo '{args.source}' hacia '{args.dest}'[/bold green]")
            else:
                console.print("[bold red]Error al enviar comando.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
