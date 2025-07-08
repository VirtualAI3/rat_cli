# CyberCLI

CyberCLI es una herramienta de línea de comandos avanzada diseñada para la gestión remota de clientes en entornos de ciberseguridad. Desarrollada para un concurso universitario, combina modularidad, seguridad y facilidad de uso en una potente interfaz CLI.

![CyberCLI Demo](https://via.placeholder.com/800x400.png?text=CyberCLI+Interface+Demo)

## Características Principales

- 🖥️ **Interfaz CLI interactiva** con autocompletado y sugerencias
- 🔒 **Comunicaciones seguras** con cifrado TLS (en desarrollo)
- 📁 **Gestión avanzada de archivos**: transferencia, listado y eliminación
- 🌐 **Control remoto** de clientes conectados
- 🛡️ **Firewall management** para configurar reglas de seguridad
- 📸 **Captura de pantallas** remota
- 💬 **Salida mejorada** con estilización Rich para mejor legibilidad
- 🧩 **Diseño modular** para fácil mantenimiento y extensión

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
   # venv\Scripts\activate  # Windows
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. (Opcional) Genera certificados TLS para pruebas:
   ```bash
   openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes -subj "/CN=localhost"
   ```

5. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Uso Básico

```plaintext
c2> start_server  # Inicia el servidor
c2> list_clients  # Muestra clientes conectados
c2> execute whoami --client 1  # Ejecuta comando en cliente 1
c2> help_cmd  # Muestra ayuda
c2> exit  # Sale del CLI
```

## Comandos Disponibles

| Comando                  | Descripción                                  | Ejemplo                          |
|--------------------------|----------------------------------------------|----------------------------------|
| `start_server`           | Inicia el servidor                           | `start_server`                   |
| `stop_server`            | Detiene el servidor                          | `stop_server`                    |
| `list_clients`           | Muestra clientes conectados                  | `list_clients`                   |
| `execute`                | Ejecuta comando remoto                       | `execute whoami --client 1`      |
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
├── main.py               # Punto de entrada principal
├── requirements.txt      # Dependencias del proyecto
├── cli/                  # Módulo de interfaz de línea de comandos
│   ├── commands.py       # Implementación de comandos
│   └── interface.py      # Interfaz interactiva
├── server/               # Componentes del servidor
│   ├── handlers.py       # Manejadores de solicitudes
│   └── server.py         # Implementación del servidor
├── parser/               # Sistema de análisis sintáctico
│   ├── grammar.lark      # Gramática EBNF
│   └── command_parser.py # Validador de comandos
├── utils/                # Utilidades diversas
│   ├── security.py       # Funciones de seguridad
│   └── formatters.py     # Formateo de salida
├── config/               # Configuraciones
├── data/                 # Archivos generados
└── tests/                # Pruebas unitarias
```

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Crea un issue describiendo la mejora propuesta
2. Haz fork del repositorio
3. Crea una rama con tus cambios (`git checkout -b feature/nueva-funcionalidad`)
4. Envía un Pull Request detallado

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

**CyberCLI** - Herramienta avanzada de gestión remota para operaciones de ciberseguridad  
Desarrollado para el Concurso Universitario de Ciberseguridad 2023