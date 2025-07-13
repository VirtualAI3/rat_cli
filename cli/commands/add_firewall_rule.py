from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_client_spec, validate_ip, validate_port

@with_default_category("Comandos de Seguridad")
class AddFirewallRuleCommand(CommandSet):
    """Comando para agregar una regla de firewall en los clientes."""

    firewall_rule_parser = Cmd2ArgumentParser(
        description="Agrega una regla de firewall en uno o todos los clientes."
    )
    firewall_rule_parser.add_argument("--name", type=str, required=True, help="Nombre de la regla")
    firewall_rule_parser.add_argument("--ip", type=str, help="Dirección IP para la regla (opcional)")
    firewall_rule_parser.add_argument("--port", type=int, required=True, help="Puerto para la regla")
    firewall_rule_parser.add_argument(
        "--action", type=str, required=True, choices=["allow", "block"],
        help="Acción de la regla: allow o block"
    )
    firewall_rule_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(firewall_rule_parser)
    def do_add_firewall_rule(self, args):
        """Agrega una regla de firewall en los clientes.
        Uso: add_firewall_rule --name <nombre> [--ip <ip>] --port <puerto> --action <allow|block> [--client <ID|all>]
        Ejemplo: add_firewall_rule --name block_ssh --ip 192.168.1.100 --port 22 --action block --client 1"""
        console = get_console()

        # Validar nombre
        if not validate_path(args.name):
            console.print("[bold red]Error: El nombre de la regla debe ser válido.[/bold red]")
            return

        # Validar IP (si se proporciona)
        if args.ip and not validate_ip(args.ip):
            console.print("[bold red]Error: La dirección IP no es válida.[/bold red]")
            return

        # Validar puerto
        if not validate_port(args.port):
            console.print("[bold red]Error: El puerto debe estar entre 1 y 65535.[/bold red]")
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
            console.print(f"[bold green]Comando enviado: agregar regla '{args.name}' (IP: {args.ip or 'any'}, Puerto: {args.port}, Acción: {args.action})[/bold green]")
            resultado = self._cmd.client_manager.enviar_comando_agregar_regla_firewall(
                args.name, args.ip, args.port, args.action, cliente_id
            )
            
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")