from difflib import get_close_matches
from utils.logger import get_console

class SuggestionEngine:
    """Proporciona sugerencias para comandos erróneos."""
    
    def __init__(self):
        self.console = get_console()
        self.commands = [
            "start_server", "stop_server", "list_clients", "execute", "get_file",
            "get_directory", "list_directory", "delete", "capture_screen",
            "add_firewall_rule", "get_files_by_extension", "send_file", "help_cmd", "exit"
        ]
    
    def suggest(self, invalid_command: str) -> str:
        """Devuelve una sugerencia para un comando inválido."""
        matches = get_close_matches(invalid_command, self.commands, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        return None
    
    def display_suggestion(self, invalid_command: str):
        """Muestra una sugerencia si el comando es inválido."""
        suggestion = self.suggest(invalid_command)
        if suggestion:
            self.console.print(f"[bold yellow]¿Quizás quisiste decir '{suggestion}'?[/bold yellow]")