# 🏥 Clínica San Rafael - Sistema de Gestión Médica Integral

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema de gestión médica todo-en-uno** desarrollado en Python para clínicas, consultorios privados y sistemas de salud que requieren control, orden y eficiencia.

## ✨ Características Principales

### 🔐 Sistema de Login Seguro
- **Multirrol** (Administrador, Médico, Enfermero, Recepcionista)
- **Hash de contraseñas** con SHA-256
- **Control de accesos** por módulo y acción

### 🌙 Modo Claro/Oscuro Inteligente
- **Theme Manager** completo
- **Aplicación automática** a widgets, botones, tablas y formularios

### 📦 Gestión de Inventario Médico
- **Registro, edición y eliminación** de insumos
- **Control de stock** en tiempo real
- **Alertas automáticas** por bajo inventario o vencimiento

### ⚠️ Sistema de Alertas Inteligentes
- **Niveles visuales de prioridad**
- **Reportes exportables** en múltiples formatos

### 📊 Módulo de Movimientos
- **Entradas, bajas y reposiciones**
- **Auditoría completa** con trazabilidad

### 👥 Gestión de Usuarios Internos
- **Activación/desactivación** de cuentas
- **Asignación flexible** de roles y permisos

### 📅 Sistema de Citas Médicas
- **Interfaz intuitiva** de agenda
- **Intervalos automáticos** configurables
- **Detección de conflictos** de horarios

### 📧 Correo Automatizado
- **Envío directo** a pacientes
- **Plantillas automáticas** personalizables
- **Registro histórico** en base de datos

### 🎤 Asistente de Voz Integrado
- **pyttsx3** para mensajes guiados
- **Asistencia auditiva** en operaciones críticas

### 📈 Reportes y Estadísticas
- **Gráficos interactivos** con Matplotlib + Seaborn
- **Análisis de stock**, vencimientos y citas

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/Putrefacto669/clinica-san-rafael.git
cd clinica-san-rafael
Instalar dependencias
pip install pyttsx3 tkcalendar mysql-connector-python matplotlib seaborn pandas

3️⃣ Configurar base de datos MySQL
CREATE DATABASE clinica_san_rafael;

4️⃣ Ejecutar la aplicación
python Hospital.py

📁 Dependencias Principales
Módulo	Versión	Función
tkinter	Incluido	Interfaz gráfica principal
mysql-connector-python	Latest	Conexión con MySQL
matplotlib	3.5+	Generación de gráficos
seaborn	0.11+	Visualizaciones estadísticas
pandas	1.3+	Procesamiento de datos
pyttsx3	2.90+	Asistente de voz
tkcalendar	1.6.1	Selectores de fecha
🔧 Configuración
⚙️ Configuración de Correo
self.config_correo = {
    'smtp_server': 'smtp.gmail.com',
    'port': 587,
    'email': 'tu_correo@gmail.com',
    'password': 'tu_contraseña_de_aplicacion'
}


✅ Nota: Gmail requiere contraseña de aplicación.

🗄️ Configuración de Base de Datos

El sistema crea automáticamente las tablas necesarias al ejecutarse por primera vez.

👥 Roles del Sistema
Rol	Permisos	Módulos Accesibles
Administrador	Acceso total	Todos los módulos
Médico	Gestión clínica	Citas, Pacientes, Reportes
Enfermero	Soporte clínico	Inventario, Alertas, Medicamentos
Recepcionista	Gestión operativa	Citas, Pacientes, Consultas
🛡️ Seguridad

✅ Contraseñas cifradas con SHA-256
✅ Control de sesiones con expiración
✅ Validación de entrada contra inyecciones SQL
✅ Logging de auditoría para operaciones críticas
✅ Backup automático de base de datos

📊 Módulos Disponibles

Dashboard — Resumen ejecutivo y métricas

Gestión de Pacientes — Historial médico completo

Inventario Médico — Control de stock y vencimientos

Agenda de Citas — Calendarización flexible

Sistema de Alertas — Notificaciones inteligentes

Reportes — Análisis y estadísticas

Comunicaciones — Correo automatizado

Configuración — Personalización del sistema

🐛 Solución de Problemas
❌ Error de conexión a MySQL
# Verificar que el servicio esté activo
sudo systemctl status mysql

# Probar conexión manual
mysql -u root -p

❌ Problemas con Tkinter (Linux)
sudo apt install python3-tk

❌ Error de dependencias
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt

🤝 Contribuciones

¡Pull requests son bienvenidos! Para cambios importantes:

Haz un fork del proyecto

Crea una rama para tu feature:

git checkout -b feature/AmazingFeature


Realiza commits:

git commit -m "Add some AmazingFeature"


Súbela al repositorio:

git push origin feature/AmazingFeature


Abre un Pull Request

📜 Licencia

Distribuido bajo licencia MIT.
Consulta el archivo LICENSE para más información.

👨‍💻 Autor

Josu Urbina
GitHub: @Putrefacto669

⭐ Si este proyecto te ayuda, considera dejar una estrella en GitHub 💙
