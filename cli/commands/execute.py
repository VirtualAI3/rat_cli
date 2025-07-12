from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path
from utils.validator import validate_client_spec
import os

@with_default_category("Comandos de Ejecución")
class ExecuteCommand(CommandSet):
    """Comando para ejecutar un archivo con código en los clientes."""

    execute_parser = Cmd2ArgumentParser(description="Ejecuta un archivo de código en uno o todos los clientes.")
    execute_parser.add_argument("--file", type=str, required=True, help="Ruta del archivo con el código Python a ejecutar")
    execute_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(execute_parser)
    def do_execute(self, args):
        """Ejecuta un archivo con código en los clientes.
        Uso: execute --file <ruta> [--client <ID|all>]
        Ejemplo: execute --file /utils/payloads/shutdown.py --client 1"""
        console = get_console()

        # Validar archivo y leer código
        if not validate_path(args.file):
            if ' ' in args.file and not (args.file.startswith('"') or args.file.startswith("'")):
                console.print("[bold red]Error: La ruta contiene espacios. Usa comillas alrededor del valor de --file.[/bold red]")
            else:
                console.print(f"[bold red]Error al leer archivo: {e}[/bold red]")
            return

        # Validar archivo y leer código
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                codigo = f.read()
        except Exception as e:
            console.print(f"[bold red]Error 2 al leer archivo: {e}[/bold red]")
            return

        if not codigo.strip():
            console.print("[bold red]Error: El archivo está vacío o no contiene código válido.[/bold red]")
            return

        # Validar clientes conectados
        if not self._cmd.client_manager.obtener_clientes_conectados():
            console.print("[bold red]Error: No hay clientes conectados.[/bold red]")
            return

        # Validar ID de cliente
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
            console.print(f"[bold green]Código del archivo '{args.file}' cargado:[/bold green]")
            self._cmd.client_manager.enviar_comando_ejecutar(codigo, cliente_id)
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")