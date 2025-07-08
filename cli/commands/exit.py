from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser
from utils.logger import get_console

@with_default_category("Comandos de Gestión")
class ExitCommand(CommandSet):
    """Comando para cerrar el CLI."""

    exit_parser = Cmd2ArgumentParser(description="Cierra el CLI y detiene el servidor.")

    def do_exit(self, statement):
        """Cierra el CLI y detiene el servidor.
        Uso: exit
        Ejemplo: exit"""
        console = get_console()

        # Detener el servidor si está activo
        try:
            if hasattr(self._cmd, "servidor") and self._cmd.servidor.ejecutando:
                self._cmd.servidor.cerrar()
        except Exception as e:
            console.print(f"[bold red]Error al cerrar el servidor: {e}[/bold red]")

        console.print("[bold green]Saliendo de CyberCLI...[/bold green]")
        return True  # Indica a cmd2 que salga del bucle
