# RatCLI

**RatCLI** (Remote Access Trojan Command Line Interface) es una herramienta de línea de comandos diseñada para el control remoto de múltiples clientes como parte de un proyecto académico orientado a la **evaluación de seguridad informática**. Este software simula las capacidades de un troyano de acceso remoto (RAT) y está destinado exclusivamente para fines educativos, pruebas en entornos controlados y auditorías de ciberseguridad.

> ⚠️ **Aviso Legal:** Este proyecto tiene fines exclusivamente académicos y de investigación. El uso no autorizado en sistemas ajenos sin consentimiento explícito es ilegal y va en contra de la ética profesional en ciberseguridad.

![RatCLI Interface](https://via.placeholder.com/800x400.png?text=RatCLI+Command+Interface)

## Características Principales

- 🖥️ **CLI interactiva** con autocompletado y sugerencias
- 📁 **Gestión de archivos remota**: transferencias, listados, eliminaciones
- 🌐 **Ejecución de comandos en clientes remotos**
- 🛡️ **Manejo de reglas de firewall simuladas**
- 📸 **Captura remota de pantallas**
- 💥 **Simulación de ataques HTTP a URLs**
- 💬 **Salida estilizada y coloreada para mejor legibilidad**
- 🧩 **Arquitectura modular**, fácilmente extensible
- 📊 **Sistema completo de logging** para seguimiento de operaciones

## Requisitos

- Python 3.8 o superior
- Instalar dependencias con:
  ```bash
  pip install -r requirements.txt
  ```

## Instalación Rápida

1. Clona el repositorio:

   ```bash
   https://github.com/VirtualAI3/rat_cli.git
   cd ratcli
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

## Uso Básico

```plaintext
c2> start_server --host 0.0.0.0 --port 5555     # Inicia el servidor C2
c2> list_clients                                # Lista clientes conectados
c2> execute script.py --client 1                # Ejecuta script en un cliente
c2> help_cmd                                    # Muestra ayuda
c2> exit                                        # Finaliza la CLI y para el servidor
```

## Comandos Disponibles

| Comando                  | Descripción                                     | Ejemplo                                                     |
| ------------------------ | ----------------------------------------------- | ----------------------------------------------------------- |
| `start_server`           | Inicia el servidor de control remoto            | `start_server --host 0.0.0.0 --port 5555`                                              |
| `stop_server`            | Detiene el servidor                             | `stop_server`                                               |
| `list_clients`           | Lista clientes conectados                       | `list_clients`                                              |
| `execute`                | Ejecuta comandos o scripts en el cliente remoto | `execute script.py --client 1`                              |
| `get_file`               | Descarga un archivo desde un cliente            | `get_file --source C:/Users/Documento.docx`               |
| `get_directory`          | Descarga un directorio completo                 | `get_directory --source /var/log/`                          |
| `list_directory`         | Lista los contenidos de un directorio remoto    | `list_directory --path /home/user`                          |
| `delete`                 | Elimina archivos o carpetas en el cliente       | `delete --path /tmp/test.txt`                               |
| `capture_screen`         | Captura la pantalla del cliente                 | `capture_screen --client 1`                                 |
| `add_firewall_rule`      | Simula la adición de una regla de firewall      | `add_firewall_rule --port 443`                              |
| `get_files_by_extension` | Descarga archivos por extensión                 | `get_files_by_extension --ext pdf`                          |
| `send_file`              | Envía archivos al cliente                       | `send_file --source payload.py`                             |
| `attack_url`             | Simula un ataque HTTP a una URL                 | `attack_url --url http://target.com --tiempo 10 --client 1` |
| `help_cmd`               | Muestra ayuda sobre un comando                  | `help_cmd get_file`                                         |

## Estructura del Proyecto

```plaintext
ratcli/
│   .gitignore
│   LICENSE
│   main.py                 # Punto de entrada principal
│   README.md               # Este archivo
│   requirements.txt        # Dependencias
│   setup.py                # Script de instalación
│
├───cli
│   │   cli_core.py
│   │   __init__.py
│   └───commands
│       │   add_firewall_rule.py
│       │   attack_url.py
│       │   capture_screen.py
│       │   delete.py
│       │   execute.py
│       │   exit.py
│       │   get_directory.py
│       │   get_file.py
│       │   get_files_by_extension.py
│       │   help_cmd.py
│       │   list_clients.py
│       │   list_directory.py
│       │   send_file.py
│       │   start_server.py
│       │   stop_server.py
│       └─── __init__.py
│
├───config
│       defaults.json
│       settings.py
│       __init__.py
│
├───data
│   ├───directories
│   ├───logs
│   │       cybercli.log
│   ├───received_files
│   └───screenshots
│
├───parser
│       command_parser.py
│       grammar.lark
│       suggestion_engine.py
│       __init__.py
│
├───server
│   │   client_manager.py
│   │   server_core.py
│   │   __init__.py
│   └───handlers
│       │   attack_url_handler.py
│       │   command_handler.py
│       │   directory_handler.py
│       │   file_handler.py
│       │   firewall_handler.py
│       │   screenshot_handler.py
│       └─── __init__.py
│
└───utils
    │   client_utils.py
    │   error_handler.py
    │   formatter.py
    │   logger.py
    │   response_waiter.py
    │   validator.py
    │   __init__.py
    └───payloads
            hola_mundo.py
```

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas colaborar:

1. Crea un *issue* para discutir cambios o sugerencias
2. Haz un fork del repositorio
3. Crea una nueva rama (`feature/nueva-funcionalidad`)
4. Realiza y prueba tus cambios
5. Envía un Pull Request explicando tus modificaciones

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

**RatCLI** – Herramienta de investigación y evaluación en ciberseguridad Desarrollado como proyecto académico universitario para el **CONCURSO PROYECTOS ESTUDIANTILES 2025 - I**
