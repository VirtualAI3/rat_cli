# CyberCLI

CyberCLI es una herramienta avanzada de línea de comandos para la gestión remota de clientes en entornos de ciberseguridad. Desarrollada para un concurso universitario, combina modularidad, seguridad y facilidad de uso en una potente interfaz CLI.

![CyberCLI Interface](https://via.placeholder.com/800x400.png?text=CyberCLI+Command+Interface)

## Características Principales

- 🖥️ **Interfaz CLI interactiva** con autocompletado y sugerencias
- 📁 **Gestión avanzada de archivos**: transferencia, listado y eliminación
- 🌐 **Control remoto** de clientes conectados
- 🛡️ **Gestión de firewall** para configurar reglas de seguridad
- 📸 **Captura de pantallas** remota
- 💬 **Salida mejorada** con estilización para mejor legibilidad
- 🧩 **Diseño modular** para fácil mantenimiento y extensión
- 📊 **Sistema de logging** completo para auditoría

## Requisitos

- Python 3.8+
- Dependencias:
  ```bash
  pip install -r requirements.txt
  ```

## Instalación Rápida

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/cybercli.git
   cd cybercli
   ```

2. Configura entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso Básico

```plaintext
c2> start_server        # Inicia el servidor
c2> list_clients        # Muestra clientes conectados
c2> get_file --source /ruta/archivo.txt --dest descargas/  # Descarga archivo
c2> help_cmd            # Muestra ayuda
c2> exit                # Sale del CLI
```

## Comandos Disponibles

| Comando                  | Descripción                                  | Ejemplo                          |
|--------------------------|----------------------------------------------|----------------------------------|
| `start_server`           | Inicia el servidor                           | `start_server`                   |
| `stop_server`            | Detiene el servidor                          | `stop_server`                    |
| `list_clients`           | Muestra clientes conectados                  | `list_clients`                   |
| `execute`                | Ejecuta comando/script remoto                | `execute codigo.py --client 1`   |
| `get_file`               | Descarga archivo desde cliente               | `get_file --source /path/file.txt` |
| `get_directory`          | Descarga directorio completo                 | `get_directory --source /data`   |
| `list_directory`         | Lista contenido de directorio remoto         | `list_directory --path /docs`    |
| `delete`                 | Elimina archivo/directorio remoto            | `delete --path /temp/file.log`   |
| `capture_screen`         | Captura pantalla remota                      | `capture_screen --client 1`      |
| `add_firewall_rule`      | Agrega regla de firewall                     | `add_firewall_rule --port 80`    |
| `get_files_by_extension` | Descarga archivos por extensión              | `get_files_by_extension --ext pdf` |
| `send_file`              | Envía archivo a cliente                      | `send_file --source local.txt`   |
| `help_cmd`               | Muestra ayuda detallada                      | `help_cmd execute`               |

## Estructura del Proyecto

```plaintext
cybercli/
│   .gitignore
│   LICENSE
│   main.py               # Punto de entrada principal
│   README.md             # Este archivo
│   requirements.txt      # Dependencias
│   setup.py              # Script de instalación
│
├───cli
│   │   cli_core.py       # Núcleo de la interfaz CLI
│   │   __init__.py
│   │
│   └───commands          # Implementación de comandos
│           add_firewall_rule.py
│           capture_screen.py
│           delete.py
│           execute.py
│           exit.py
│           get_directory.py
│           get_file.py
│           get_files_by_extension.py
│           help_cmd.py
│           list_clients.py
│           list_directory.py
│           send_file.py
│           start_server.py
│           stop_server.py
│           __init__.py
│
├───config                # Configuraciones
│       defaults.json
│       settings.py
│       __init__.py
│
├───data                  # Almacenamiento
│   ├───directories       # Directorios descargados
│   ├───logs              # Registros del sistema
│   │       cybercli.log
│   ├───received_files    # Archivos recibidos
│   └───screenshots       # Capturas de pantalla
│
├───parser                # Sistema de análisis
│       command_parser.py # Validador de comandos
│       grammar.lark      # Gramática EBNF
│       suggestion_engine.py # Motor de sugerencias
│       __init__.py
│
├───server                # Componentes del servidor
│   │   client_manager.py # Gestión de clientes
│   │   server_core.py    # Núcleo del servidor
│   │   __init__.py
│   │
│   └───handlers          # Manejadores de operaciones
│           command_handler.py
│           directory_handler.py
│           file_handler.py
│           firewall_handler.py
│           screenshot_handler.py
│           __init__.py
│
└───utils                 # Utilidades
        error_handler.py  # Manejo de errores
        formatter.py      # Formateo de salida
        logger.py         # Sistema de logging
        response_waiter.py# Espera de respuestas
        validator.py      # Validación de datos
        __init__.py
```

## Contribuciones

¡Las contribuciones son bienvenidas! Sigue estos pasos:

1. Reporta errores o sugerencias creando un issue
2. Haz fork del repositorio
3. Crea una rama para tu función (`git checkout -b feature/nueva-funcionalidad`)
4. Realiza tus cambios y prueba exhaustivamente
5. Envía un Pull Request con una descripción detallada

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

**CyberCLI** - Plataforma avanzada de gestión remota para operaciones de ciberseguridad  
Desarrollado para el Concurso Universitario de Ciberseguridad 2023