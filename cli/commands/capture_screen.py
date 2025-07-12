from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_client_spec
from server.handlers.screenshot_handler import ScreenshotHandler

@with_default_category("Comandos de Captura")
class CaptureScreenCommand(CommandSet):
    """Comando para solicitar una captura de pantalla desde los clientes."""

    capture_screen_parser = Cmd2ArgumentParser(description="Solicita una captura de pantalla desde uno o todos los clientes.")
    capture_screen_parser.add_argument("--dest", type=str, required=False, help="Ruta de destino en el servidor (opcional). Si no se especifica, se usa la ruta por defecto.")
    capture_screen_parser.add_argument("--name", type=str, help="Nombre del archivo de la captura (opcional)")
    capture_screen_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(capture_screen_parser)
    def do_capture_screen(self, args):
        """Solicita una captura de pantalla desde los clientes.
        Uso: capture_screen --dest <ruta_destino> [--name <nombre_archivo>] [--client <ID|all>]
        Ejemplo: capture_screen --dest screenshots --name captura1.png --client 1"""
        console = get_console()

        # Validar nombre de archivo (si se proporciona)
        if args.name and not validate_path(args.name):
            console.print("[bold red]Error: El nombre del archivo no es válido.[/bold red]")
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
            resultado = self._cmd.client_manager.enviar_comando_capturar_pantalla(args.dest, args.name, cliente_id)
            if resultado:
                console.print(f"[bold green]✅ Captura recibida y guardada correctamente.[/bold green]")
            else:
                console.print("[bold red]❌ Falló la captura de pantalla o el cliente no respondió.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
