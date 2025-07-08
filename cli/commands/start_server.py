from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_ip, validate_port
from config.settings import DEFAULT_HOST, DEFAULT_PORT

@with_default_category("Comandos de Gestión")
class StartServerCommand(CommandSet):
    """Comando para iniciar el servidor."""

    start_server_parser = Cmd2ArgumentParser(description="Inicia el servidor en el host y puerto especificados.", epilog="Ejemplo de uso: start_server --host 0.0.0.0 --port 8080", add_help=False)
    start_server_parser.add_argument("-h", "--help", action="help", help="Muestra este mensaje de ayuda")
    start_server_parser.add_argument("--host", type=str, default=DEFAULT_HOST, help="Host del servidor (por defecto: localhost)")
    start_server_parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Puerto del servidor (por defecto: 12345)")

    @with_argparser(start_server_parser)
    def do_start_server(self, args):
        """Inicia el servidor.
        Uso: start_server [--host <host>] [--port <puerto>]
        Ejemplo: start_server --host 0.0.0.0 --port 8080"""
        console = get_console()

        # Validar host
        if not validate_ip(args.host):
            console.print("[bold red]Error: La dirección host debe ser una IP válida.[/bold red]")
            return

        # Validar puerto
        if not validate_port(args.port):
            console.print("[bold red]Error: El puerto debe estar entre 1 y 65535.[/bold red]")
            return

        # Verificar si el servidor ya está ejecutando
        if hasattr(self._cmd, 'servidor') and self._cmd.servidor.ejecutando:
            console.print("[bold yellow]El servidor ya está en ejecución.[/bold yellow]")
            return

        # Iniciar el servidor
        try:
            self._cmd.iniciar_servidor(args.host, args.port)
            console.print(f"[bold green]Servidor iniciado en {args.host}:{args.port}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al iniciar el servidor: {e}[/bold red]")