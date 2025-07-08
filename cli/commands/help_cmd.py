from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console
from rich.table import Table
from cmd2 import CompletionItem

@with_default_category("Comandos de Ayuda")
class HelpCmdCommand(CommandSet):
    """Comando para mostrar ayuda sobre los comandos disponibles."""
    
    help_cmd_parser = Cmd2ArgumentParser(description="Muestra ayuda sobre los comandos disponibles.")
    help_cmd_parser.add_argument("command", type=str, nargs="?", help="Nombre del comando para ver ayuda detallada")

    @with_argparser(help_cmd_parser)
    def do_help_cmd(self, args):
        """Muestra ayuda sobre los comandos disponibles.
        Uso: help_cmd [comando]
        Ejemplo: help_cmd list_directory"""
        console = get_console()
        
        if args.command:
            # Delegate to cmd2's native help command on the parent instance.
            # This is the most reliable way to show help for any command,
            # letting cmd2 handle fetching the docstrings or help_ methods.
            self._cmd.onecmd(f"help {args.command}")
        else:
            # Show a list of commands with descriptions
            table = Table(title="[bold green]Comandos Disponibles[/bold green]")
            table.add_column("Comando", style="cyan")
            table.add_column("Descripción", style="green")
            
            # List of commands and their descriptions
            # It's a good practice to keep this list updated as you add/remove commands.
            commands = [
                ("start_server", "Inicia el servidor en el host y puerto especificados"),
                ("stop_server", "Detiene el servidor y cierra todas las conexiones"),
                ("list_clients", "Muestra una lista de todos los clientes conectados"),
                ("execute", "Ejecuta un comando en uno o todos los clientes"),
                ("get_file", "Solicita un archivo desde uno o todos los clientes"),
                ("get_directory", "Solicita un directorio desde uno o todos los clientes"),
                ("list_directory", "Lista el contenido de un directorio en los clientes"),
                ("delete", "Elimina un archivo o directorio en los clientes"),
                ("capture_screen", "Solicita una captura de pantalla desde los clientes"),
                ("add_firewall_rule", "Agrega una regla de firewall en los clientes"),
                ("get_files_by_extension", "Solicita archivos por extensión desde los clientes"),
                ("send_file", "Envía un archivo desde el servidor a los clientes"),
                ("help_cmd", "Muestra esta ayuda"),
                ("exit", "Cierra el CLI")
            ]
            
            for cmd_name, description in commands:
                table.add_row(cmd_name, description)
            
            console.print(table)
            console.print("[bold yellow]Usa 'help_cmd <comando>' para ver ayuda detallada.[/bold yellow]")
    def complete_help_cmd(self, text, line, begidx, endidx):
            """Autocompleta nombres de comandos para el argumento 'command' de help_cmd."""
            # Obtiene la lista de comandos disponibles en el CLI principal
            commands = self._cmd.get_all_commands()

            # Filtra comandos que empiezan con el texto actual escrito
            completions = [CompletionItem(cmd) for cmd in commands if cmd.startswith(text)]

            return completions