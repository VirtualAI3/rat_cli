import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "defaults.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

# Configuraciones del servidor
DEFAULT_HOST = config["server"]["host"]
DEFAULT_PORT = config["server"]["port"]
MAX_CONNECTIONS = config["server"]["max_connections"]

# Rutas
BASE_DIR = os.path.abspath(config["paths"]["base_dir"])
RECEIVED_FILES_DIR = os.path.join(BASE_DIR, config["paths"]["received_files_dir"])
DIRECTORIES_DIR = os.path.join(BASE_DIR, config["paths"]["directories_dir"])
SCREENSHOTS_DIR = os.path.join(BASE_DIR, config["paths"]["screenshots_dir"])
LOG_DIR = os.path.join(BASE_DIR, config["paths"]["log_dir"])

# Logging
LOG_FILE = os.path.join(BASE_DIR, config["logging"]["log_file"])
LOG_LEVEL = config["logging"]["log_level"]

# Clientes
CLIENT_TIMEOUT = config["client"]["timeout"]