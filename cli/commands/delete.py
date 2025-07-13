from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from utils.validator import validate_path, validate_client_spec

@with_default_category("Comandos de Gestión")
class DeleteCommand(CommandSet):
    """Comando para eliminar un archivo o directorio en los clientes."""

    delete_parser = Cmd2ArgumentParser(description="Elimina un archivo o directorio en uno o todos los clientes.")
    delete_parser.add_argument("path", type=str, help="Ruta del archivo o directorio a eliminar")
    delete_parser.add_argument("--client", type=str, default="all", help="ID del cliente o 'all' (por defecto: all)")

    @with_argparser(delete_parser)
    def do_delete(self, args):
        """Elimina un archivo o directorio en los clientes.
        Uso: delete <ruta> [--client <ID|all>]
        Ejemplo: delete /home/user/doc.txt --client 1"""
        console = get_console()

        # Validar ruta
        if not validate_path(args.path):
            console.print("[bold red]Error: La ruta debe ser válida.[/bold red]")
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
            resultado = self._cmd.client_manager.enviar_comando_eliminar(args.path, cliente_id)
            if resultado:
                console.print(f"[bold green]✅ Se elimino correctamente {args.path} del cliente.[/bold green]")
            else:
                console.print(f"[bold red]❌ Falló la eliminación de {args.path} o el cliente no respondió.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error al enviar comando: {e}[/bold red]")
