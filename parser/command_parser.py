from lark import Lark, Transformer
from utils.logger import get_console
import os

class CommandTransformer(Transformer):
    """Transforma el árbol de parseo en un diccionario de argumentos."""
    
    def command(self, items):
        return {"command": items[0], "args": items[1:]}
    
    def PATH(self, token):
        return str(token)
    
    def NUMBER(self, token):
        return int(token)
    
    def client_arg(self, items):
        return items[0]
    
    def files_flag(self, items):
        return True

def create_parser():
    """Crea un parser basado en la gramática definida en grammar.lark."""
    grammar_path = os.path.join(os.path.dirname(__file__), "grammar.lark")
    with open(grammar_path, "r") as f:
        grammar = f.read()
    
    parser = Lark(grammar, start="command", parser="lalr")
    return parser

def parse_command(command_str):
    """Parsea un comando y devuelve sus componentes."""
    console = get_console()
    try:
        parser = create_parser()
        tree = parser.parse(command_str)
        transformed = CommandTransformer().transform(tree)
        return transformed
    except Exception as e:
        console.print(f"[bold red]Error de sintaxis: {e}[/bold red]")
        return None