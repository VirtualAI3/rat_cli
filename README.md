## Guía de Uso y Buenas Prácticas de **RAT CLI**

**Orientada a Docentes y Estudiantes en Entornos Educativos de Ciberseguridad**

---

## 🎯 Objetivo de esta Guía

Brindar a **docentes y estudiantes** una guía clara y estructurada para la **instalación, uso ético y pedagógico** de la herramienta **RAT CLI**, garantizando que su aplicación se limite a **entornos controlados** con fines **educativos y éticos**, evitando cualquier uso indebido o malicioso.

---

## 🧠 ¿Qué es RAT CLI?

**RAT CLI** (Remote Administration Tool Command-Line Interface) es una herramienta educativa diseñada para simular escenarios de administración remota en contextos de **ciberseguridad ofensiva y defensiva**. Su propósito es didáctico: permitir prácticas controladas en laboratorios, con fines exclusivamente académicos.

> ⚠️ **RAT CLI no debe ser utilizada en redes reales o dispositivos personales.** Está diseñada para entornos simulados bajo supervisión docente.

---

## 🛠 Instalación Segura en Entornos Académicos

**Requisitos Previos:**

* Python 3.8 o superior
* Red virtual o entorno aislado
* Supervisión docente

**Pasos de instalación:**

```bash
# Clonar el repositorio
git clone https://github.com/tu_usuario/rat-cli.git
cd rat-cli

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

> 🔐 Se recomienda usar máquinas virtuales para ejecutar RAT CLI dentro de un laboratorio aislado o entorno de práctica.

---

## 🔒 Buenas Prácticas y Uso Responsable

1. **Uso exclusivo para formación académica.**
   Cualquier otro uso está expresamente prohibido.

2. **Consentimiento obligatorio.**
   Todas las máquinas involucradas deben estar controladas por el equipo educativo.

3. **Entornos virtuales y simulados.**
   Nunca ejecutar RAT CLI en redes de producción ni en equipos personales ajenos.

4. **Supervisión docente.**
   Toda práctica debe ser guiada por instructores capacitados.

5. **Registro de actividad.**
   El sistema de logging incorporado permite revisar todas las acciones ejecutadas.

6. **Responsabilidad ética.**
   El objetivo es formar profesionales en ciberseguridad con integridad y conciencia social.

---

## 👩‍🏫 Aplicaciones Educativas en Entornos Controlados

| Escenario                            | Objetivo Educativo                       | Comando de ejemplo                   |
| ------------------------------------ | ---------------------------------------- | ------------------------------------ |
| Simulación de red comprometida       | Análisis de comportamiento de RAT        | `list_clients`, `start_server`       |
| Transferencia de archivos maliciosos | Estudio de vectores de entrada           | `send_file --source malware_sim.py`  |
| Captura de pantalla remota           | Práctica de adquisición de evidencias    | `capture_screen --client 2`          |
| Automatización de auditorías         | Ejecución remota de scripts de revisión  | `execute audit_script.py --client 1` |
| Reglas de firewall simuladas         | Evaluación de protección ante conexiones | `add_firewall_rule --port 22`        |

> 🧪 **Consejo docente:** documenta cada práctica con objetivos, pasos, resultados y reflexiones éticas.

---

## 🧭 Ejemplo de Flujo de Clase

**Tema:** Gestión Remota y Seguridad Ética
**Duración:** 2 horas
**Recursos:** 3 máquinas virtuales conectadas (1 servidor, 2 clientes)

1. **Teoría inicial (30 min):** Fundamentos de administración remota segura.
2. **Preparación del entorno (15 min):** Configuración de las VMs con red interna.
3. **Práctica técnica (1 hora):** Uso de comandos `start_server`, `get_file`, `list_clients`.
4. **Discusión final (15 min):** Reflexión sobre ética, riesgos y mitigación.

---

## 🧾 Licencia y Consideraciones Legales

Este software se distribuye bajo la **Licencia MIT**.
Sin embargo, **el uso indebido de RAT CLI puede incurrir en responsabilidad legal bajo normativas locales de delitos informáticos**.

---

## 👨‍🏫 Recomendaciones para Docentes

* Complementar con guías de ética profesional y seguridad digital.
* Evaluar la documentación y el comportamiento responsable del estudiante.
* Fomentar el uso del logging para análisis post-mortem y forense.
* Desarrollar proyectos donde el uso de RAT CLI sea parte de un ciclo completo: **planificación → ejecución → evaluación ética y técnica**.

---

## 📚 Recursos Adicionales

* [MITRE ATT\&CK Framework](https://attack.mitre.org/)
* [Guía de Buenas Prácticas en Ciberseguridad - INCIBE](https://www.incibe.es/)
* [Licencia MIT Explicada](https://choosealicense.com/licenses/mit/)

---

## ✅ Conclusión

**RAT CLI** ofrece un entorno potente para el aprendizaje técnico de gestión remota, siempre que sea utilizado con **propósito educativo, ética y responsabilidad**. Su potencial pedagógico depende de la forma en que docentes y estudiantes lo apliquen dentro de marcos seguros y supervisados.

---