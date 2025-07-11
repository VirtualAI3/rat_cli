Guía de Uso y Buenas Prácticas de CyberCLI
Orientada a Docentes y Estudiantes en Entornos Educativos de Ciberseguridad

🎯 Objetivo de esta Guía
Brindar a docentes y estudiantes una guía clara y estructurada para la instalación, uso ético y pedagógico de la herramienta CyberCLI, garantizando que su aplicación se limite a entornos controlados con fines educativos y éticos, evitando cualquier uso indebido o malicioso.

🧠 ¿Qué es CyberCLI?
CyberCLI es una herramienta de línea de comandos diseñada para simular escenarios de gestión remota en ciberseguridad ofensiva y defensiva. Fue desarrollada con fines académicos para apoyar la formación en prácticas seguras, auditorías, y ejercicios de red teaming/red hardening.

⚠️ CyberCLI NO debe utilizarse en redes reales sin consentimiento explícito. Solo está autorizada para entornos controlados, laboratorios o simulaciones académicas.

🛠 Instalación Segura en Entornos Académicos
Requisitos Previos:

Python 3.8+

Conexión a una red local de laboratorio (sin acceso a sistemas reales)

Supervisión docente en todo momento

Pasos para la Instalación:

bash
Copiar
Editar
# Clona el repositorio
git clone https://github.com/tu_usuario/cybercli.git
cd cybercli

# Crea un entorno virtual (buena práctica)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
python main.py
🔐 Recomendación docente: usar entornos virtualizados (VirtualBox, VMware, etc.) o redes aisladas para asegurar el aislamiento de pruebas.

🔒 Buenas Prácticas y Uso Responsable
Propósito educativo únicamente:
Utiliza la herramienta solo para ejercicios guiados por docentes o proyectos académicos autorizados.

Consentimiento informado:
Toda actividad remota debe realizarse con el consentimiento de los participantes. Está prohibido el acceso a dispositivos no controlados.

Entornos simulados:
Utiliza máquinas virtuales con sistemas configurados para prácticas de ciberseguridad (e.g. Kali, Metasploitable, OWASP Juice Shop).

Supervisión constante:
Toda práctica debe estar supervisada por personal docente o técnicos de laboratorio.

No producción:
No está permitido instalar o ejecutar CyberCLI en redes empresariales, educativas en producción o equipos personales ajenos.

Auditoría:
Utiliza el sistema de logging de CyberCLI para registrar todas las acciones realizadas. Esto facilita evaluaciones y revisiones.

Ética profesional:
Usa CyberCLI para comprender, mejorar y defender sistemas, nunca para comprometerlos sin autorización.

👩‍🏫 Aplicaciones Educativas en Entornos Controlados
Escenario	Objetivo Educativo	Ejemplo de Comando
Simulación de red con clientes vulnerables	Enseñar prácticas de hardening	list_clients, add_firewall_rule
Transferencia de archivos maliciosos simulados	Analizar vectores de entrada	send_file --source malware_sim.py
Captura de pantalla en auditorías controladas	Práctica de evidencia forense	capture_screen --client 2
Comprobación de configuraciones remotas	Automatización de auditorías	execute audit_script.py --client 1

🧪 Recomendación docente: Documenta cada ejercicio con objetivos, pasos, resultados esperados y reflexión ética final.

🧭 Ejemplo de Flujo de Clase
Tema: Práctica de Gestión Remota Segura
Duración: 2 horas
Materiales: 3 VMs (1 servidor, 2 clientes), CyberCLI instalado

Explicación teórica (30 min): Introducción a gestión remota segura y ética.

Configuración del entorno (15 min): VMs conectadas por red virtual interna.

Ejecución práctica (1 hora): Uso de comandos start_server, list_clients, send_file, add_firewall_rule.

Reflexión final (15 min): Discusión sobre riesgos y responsabilidades éticas.

🧾 Licencia y Legalidad
CyberCLI se distribuye bajo la licencia MIT, lo que permite su uso, modificación y distribución con fines académicos. Sin embargo, el mal uso de la herramienta puede ser penado por ley en muchos países bajo legislaciones de delitos informáticos.

👨‍💻 Recomendaciones para Docentes
Incluir una rúbrica de evaluación ética junto a la técnica.

Fomentar el uso del sistema de logging para análisis forense.

Diseñar prácticas donde el uso de CyberCLI sea parte de un ciclo completo: planeación, ejecución, evaluación y documentación.

📚 Recursos Adicionales
MITRE ATT&CK Framework

Guía Ética en Ciberseguridad - INCIBE

Licencia MIT explicada

🧩 Conclusión
CyberCLI representa una potente herramienta para aprender ciberseguridad de forma práctica, segura y ética. Su uso debe estar siempre acompañado de reflexión crítica y supervisión académica para formar profesionales responsables.