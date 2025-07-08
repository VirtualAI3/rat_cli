CyberCLI
CyberCLI es una herramienta de línea de comandos (CLI) diseñada para la gestión remota de clientes en un entorno de ciberseguridad. Permite ejecutar comandos, transferir archivos, gestionar directorios, capturar pantallas, y configurar reglas de firewall en clientes conectados, con un enfoque en modularidad, seguridad, y facilidad de uso. Este proyecto está desarrollado para un concurso universitario de ciberseguridad.
Características

Interfaz CLI interactiva basada en cmd2, con soporte para autocompletado y ayuda.
Parser de comandos con gramática EBNF (lark) para validar sintaxis y detectar errores.
Sugerencias de comandos para mejorar la experiencia de usuario.
Gestión de clientes con soporte para selección específica (--client <ID|all>).
Transferencia segura de archivos y directorios con validaciones robustas.
Captura de pantallas y gestión de reglas de firewall.
Cifrado TLS para comunicaciones seguras (en desarrollo).
Salidas estilizadas con rich para una mejor legibilidad.
Estructura modular con comandos y manejadores separados para fácil mantenimiento.

Requisitos

Python 3.8+
Dependencias listadas en requirements.txt:pip install -r requirements.txt



Instalación

Clona el repositorio:git clone https://github.com/tu_usuario/cybercli.git
cd cybercli


Crea un entorno virtual (opcional pero recomendado):python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


Instala las dependencias:pip install -r requirements.txt


(Opcional) Genera certificados TLS para pruebas:openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes -subj "/CN=localhost"


Ejecuta el CLI:python main.py



Uso

Inicia el servidor:c2> start_server


Lista los clientes conectados:c2> list_clients


Ejecuta un comando en un cliente:c2> execute whoami --client 1


Solicita un archivo:c2> get_file --source /home/user/doc.txt --dest received_files/doc.txt --client 1


Ver ayuda:c2> help_cmd


Sal del CLI:c2> exit



Comandos Disponibles

start_server: Inicia el servidor.
stop_server: Detiene el servidor.
list_clients: Muestra clientes conectados.
execute: Ejecuta un comando en los clientes.
get_file: Solicita un archivo.
get_directory: Solicita un directorio.
list_directory: Lista el contenido de un directorio.
delete: Elimina un archivo o directorio.
capture_screen: Solicita una captura de pantalla.
add_firewall_rule: Agrega una regla de firewall.
get_files_by_extension: Solicita archivos por extensión.
send_file: Envía un archivo a los clientes.
help_cmd: Muestra ayuda.
exit: Cierra el CLI.

Estructura del Proyecto
cybercli/
├── main.py               # Entrada principal
├── requirements.txt      # Dependencias
├── README.md             # Documentación
├── cli/                  # CLI interactivo
├── server/               # Servidor y manejadores
├── parser/               # Parser y gramática
├── utils/                # Utilidades
├── config/               # Configuraciones
├── data/                 # Archivos generados

Contribuciones
Este proyecto está abierto a contribuciones. Por favor, crea un issue o envía un pull request con tus mejoras.
Licencia
MIT License (ver LICENSE para detalles).