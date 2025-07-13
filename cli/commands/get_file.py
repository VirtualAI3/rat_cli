from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_client_spec
from server.handlers.file_handler import FileHandler

@with_default_category("Comandos de Transferencia")
class GetFileCommand(CommandSet):
    """Comando para solicitar un archivo desde los clientes."""
    
    get_file_parser = Cmd2ArgumentParser(description="Solicita un archivo desde uno o todos los clientes.")
    get_file_parser.add_argument("--source", type=str, required=True, help="Ruta del archivo en el cliente")
    get_file_parser.add_argument("--dest", type=str, required=False, help="Ruta de destino en el servidor (Opcional). Ya existe una ruta por defecto.")
    get_file_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(get_file_parser)
    def do_get_file(self, args):
        """Solicita un archivo desde los clientes.
        Uso: get_file --source <ruta_origen> [--dest <ruta_destino>] [--client <ID|all>]
        Ejemplo: get_file --source /home/user/doc.txt --dest received_files/doc.txt --client 1"""
        console = get_console()

        # Validar rutas
        if not validate_path(args.source):
            console.print("[bold red]Error: La ruta de origen debe se válida.[/bold red]")
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
            resultado = self._cmd.client_manager.enviar_comando_solicitar_archivo(args.source, args.dest, cliente_id)
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
