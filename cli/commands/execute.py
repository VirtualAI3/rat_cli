from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_client_spec

@with_default_category("Comandos de Ejecución")
class ExecuteCommand(CommandSet):
    """Comando para ejecutar un comando en los clientes."""

    execute_parser = Cmd2ArgumentParser(description="Ejecuta un comando en uno o todos los clientes.")
    execute_parser.add_argument("code", type=str, help="Comando a ejecutar")
    execute_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(execute_parser)
    def do_execute(self, args):
        """Ejecuta un comando en los clientes.
        Uso: execute <comando> [--client <ID|all>]
        Ejemplo: execute whoami --client 1"""
        console = get_console()

        # Validar comando
        if not args.code or not isinstance(args.code, str):
            console.print("[bold red]Error: Debe especificar un comando válido.[/bold red]")
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
            self._cmd.client_manager.enviar_comando_ejecutar(args.code, cliente_id)
            console.print(f"[bold green]Comando enviado: ejecutar '{args.code}'[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
