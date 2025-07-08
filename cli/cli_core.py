# cli_core.py
from cmd2 import Cmd
from utils.logger import get_console
from utils.error_handler import ErrorHandler
from server.server_core import ServidorSocket
from server.client_manager import ClientManager
from config.settings import DEFAULT_HOST, DEFAULT_PORT

# Importa todos tus CommandSets
from cli.commands.start_server import StartServerCommand
from cli.commands.stop_server import StopServerCommand
from cli.commands.list_clients import ListClientsCommand
from cli.commands.execute import ExecuteCommand
from cli.commands.get_file import GetFileCommand
from cli.commands.send_file import SendFileCommand
from cli.commands.get_directory import GetDirectoryCommand
from cli.commands.list_directory import ListDirectoryCommand
from cli.commands.delete import DeleteCommand
from cli.commands.capture_screen import CaptureScreenCommand
from cli.commands.add_firewall_rule import AddFirewallRuleCommand
from cli.commands.get_files_by_extension import GetFilesByExtensionCommand
from cli.commands.help_cmd import HelpCmdCommand
from cli.commands.exit import ExitCommand
import sys
from rich.text import Text

class CyberCLICore(Cmd):
    """Clase principal del CLI interactivo para CyberCLI."""

    def __init__(self):
        # Create instances of your CommandSets FIRST
        # These will be passed to the super().__init__() call
        command_set_instances = [
            StartServerCommand(),
            StopServerCommand(),
            ListClientsCommand(),
            ExecuteCommand(),
            GetFileCommand(),
            SendFileCommand(),
            GetDirectoryCommand(),
            ListDirectoryCommand(),
            DeleteCommand(),
            CaptureScreenCommand(),
            AddFirewallRuleCommand(),
            GetFilesByExtensionCommand(),
            HelpCmdCommand(), # Ensure HelpCmdCommand is included here and INSTANTIATED
            ExitCommand()
        ]

        super().__init__(command_sets=command_set_instances) 

        self.console = get_console() 
        
        # Set the prompt using rich.text.Text for color
        self.prompt = "c2> "

        self.intro = (
            "Servidor no iniciado. Usa 'start_server' para arrancarlo.\n"
            "Escribe 'help_cmd' para ver los comandos disponibles."
        )
        
        try:
            self.error_handler = ErrorHandler()
        except Exception as e:
            print(f"Error al inicializar ErrorHandler: {e}")
            sys.exit(1)

        try:
            self.servidor = ServidorSocket(host=DEFAULT_HOST, puerto=DEFAULT_PORT)
            self.client_manager = ClientManager(self.servidor, self)
            self.servidor.establecer_cli_instance(self)
        except Exception as e:
            if hasattr(self, 'error_handler'):
                self.error_handler.handle_error(e, "No se pudo inicializar el servidor.", exit_program=True)
            else:
                print(f"Error crítico al inicializar servidor y error_handler no disponible: {e}")
                sys.exit(1)

        self.allow_clipboard = False
        self.shortcuts = {"?": "help_cmd", "q": "exit"}

    def default(self, statement):
        from parser.suggestion_engine import SuggestionEngine 
        suggestion_engine = SuggestionEngine()

        self.console.print(f"[bold red]Comando no reconocido: '{statement.command}'[/bold red]")
        suggestion_engine.display_suggestion(statement.command)

    def iniciar_servidor(self, host, port):
        """Método para iniciar el servidor (usado por StartServerCommand)."""
        try:
            self.servidor.iniciar(host, port)
        except Exception as e:
            if hasattr(self, 'error_handler'):
                self.error_handler.handle_error(e, "Error al iniciar el servidor.")
            else:
                self.console.print(f"[bold red]Error al iniciar el servidor (error_handler no disponible): {e}[/bold red]")