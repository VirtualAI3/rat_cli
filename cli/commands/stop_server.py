from cmd2 import CommandSet, with_default_category, Cmd2ArgumentParser, with_argparser
from utils.logger import get_console

@with_default_category("Comandos de Gestión")
class StopServerCommand(CommandSet):
    """Comando para detener el servidor."""

    stop_server_parser = Cmd2ArgumentParser(description="Detiene el servidor y cierra todas las conexiones.")

    #@with_argparser(stop_server_parser)
    def do_stop_server(self, args):
        """Detiene el servidor.
        Uso: stop_server
        Ejemplo: stop_server"""
        console = get_console()

        # Verificar si el servidor está ejecutando
        if not hasattr(self._cmd, 'servidor') or not self._cmd.servidor.ejecutando:
            console.print("[bold yellow]El servidor no está en ejecución.[/bold yellow]")
            return

        # Detener el servidor
        try:
            self._cmd.servidor.cerrar()
            console.print("[bold green]Servidor detenido exitosamente.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error al detener el servidor: {e}[/bold red]")
