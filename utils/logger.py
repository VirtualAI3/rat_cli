import logging
import os
from rich.console import Console
from rich.logging import RichHandler
from config.settings import LOG_DIR, LOG_FILE, LOG_LEVEL

def setup_logging():
    """Configura el logging con rich para consola y archivo."""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Configurar logging para archivo
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=LOG_FILE,
        filemode="a"
    )
    
    # Configurar consola con rich
    console = Console()
    rich_handler = RichHandler(console=console, show_time=True, show_level=True)
    logging.getLogger().addHandler(rich_handler)
    
    return console

def get_console():
    """Obtiene la instancia de rich.Console."""
    return Console()