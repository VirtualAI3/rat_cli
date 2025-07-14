import sys
from cli.cli_core import CyberCLICore
from utils.logger import setup_logging

def main():
    """Punto de entrada principal para RatCLI."""
    # Configurar logging con rich
    console = setup_logging()
    
    # Inicializar el CLI
    try:
        console.print("[bold green]Bienvenido a RatCLI[/bold green]")
        cli = CyberCLICore()
        cli.cmdloop()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Saliendo de RatCLI...[/bold yellow]")
        cli.do_exit(None)
    except Exception as e:
        console.print(f"[bold red]Error crítico: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()