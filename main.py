import sys
from cli.cli_core import CyberCLICore
from utils.logger import setup_logging
from rich.console import Console

def main():
    """Punto de entrada principal para CyberCLI."""
    # Configurar logging con rich
    console = setup_logging()
    
    # Inicializar el CLI
    try:
        console.print("[bold green]Bienvenido a CyberCLI[/bold green]")
        cli = CyberCLICore()
        cli.cmdloop()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Saliendo de CyberCLI...[/bold yellow]")
        cli.do_exit(None)
    except Exception as e:
        console.print(f"[bold red]Error crítico: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()