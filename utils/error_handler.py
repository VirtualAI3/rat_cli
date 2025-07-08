import logging
from rich.console import Console
from utils.logger import get_console
from utils.formatter import format_error

class ErrorHandler:
    """Maneja errores de manera centralizada con mensajes estilizados y logging."""
    
    def __init__(self):
        self.console = get_console()
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, exception: Exception, custom_message: str = None, exit_program: bool = False) -> None:
        """Maneja una excepción mostrando un mensaje estilizado y registrándola."""
        error_message = custom_message or str(exception)
        format_error(error_message)
        self.logger.error(f"Error: {error_message}", exc_info=True)
        
        if exit_program:
            self.console.print("[bold red]Finalizando programa debido a un error crítico.[/bold red]")
            exit(1)
    
    def handle_validation_error(self, message: str) -> None:
        """Maneja errores de validación con un mensaje específico."""
        format_error(message)
        self.logger.warning(f"Validación fallida: {message}")
    
    def handle_connection_error(self, exception: Exception) -> None:
        """Maneja errores de conexión al servidor o clientes."""
        error_message = f"Error de conexión: {str(exception)}"
        format_error(error_message)
        self.logger.error(error_message, exc_info=True)
    
    def handle_file_error(self, exception: Exception, file_path: str) -> None:
        """Maneja errores relacionados con archivos."""
        error_message = f"Error al procesar archivo '{file_path}': {str(exception)}"
        format_error(error_message)
        self.logger.error(error_message, exc_info=True)
    
    def handle_syntax_error(self, command: str, exception: Exception) -> None:
        """Maneja errores de sintaxis en comandos."""
        error_message = f"Error de sintaxis en comando '{command}': {str(exception)}"
        format_error(error_message)
        self.logger.error(error_message, exc_info=True)
        from parser.suggestion_engine import SuggestionEngine
        suggestion_engine = SuggestionEngine()
        suggestion_engine.display_suggestion(command)