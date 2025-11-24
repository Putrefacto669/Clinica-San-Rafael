# correos.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import queue
import logging
from datetime import datetime
from database import run_mysql_query, run_mysql_non_query
from config import get_email_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class SistemaCorreosClinica:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Clínica San Rafael - Sistema de Correos")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f4f8')
        
        # Cola para comunicación entre hilos
        self.queue = queue.Queue()
        
        # Configuraciones
        self.config_bd = get_mysql_config()
        self.config_correo = get_email_config()
        
        self.crear_base_datos()
        self.crear_interfaz()
        self.verificar_cola()
        
    def verificar_cola(self):
        """Verificar si hay mensajes en la cola desde el hilo principal"""
        try:
            while True:
                mensaje = self.queue.get_nowait()
                if mensaje['tipo'] == 'log':
                    self._log(mensaje['texto'])
                elif mensaje['tipo'] == 'estado_boton':
                    self.btn_enviar.config(state=mensaje['estado'], text=mensaje['texto'])
                elif mensaje['tipo'] == 'mensaje_exito':
                    messagebox.showinfo("Éxito", mensaje['texto'])
                    self.limpiar_formulario()
                elif mensaje['tipo'] == 'mensaje_error':
                    messagebox.showerror("Error", mensaje['texto'])
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.verificar_cola)
    
    def log(self, mensaje):
        """Agregar mensaje al área de logs de forma segura"""
        self.queue.put({'tipo': 'log', 'texto': mensaje})
    
    def _log(self, mensaje):
        """Método interno para agregar mensaje al área de logs"""
        self.text_logs.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_logs.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.text_logs.config(state=tk.DISABLED)
        self.text_logs.see(tk.END)
        self.root.update_idletasks()
        
    def crear_base_datos(self):
        """Crear la base de datos y tabla si no existen"""
        try:
            # Crear base de datos
            run_mysql_non_query("CREATE DATABASE IF NOT EXISTS clinica_correos")
            run_mysql_non_query("USE clinica_correos")
            
            # Crear tabla
            run_mysql_non_query('''
                CREATE TABLE IF NOT EXISTS correos_enviados (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    paciente VARCHAR(100) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    telefono VARCHAR(20),
                    asunto VARCHAR(255) NOT NULL,
                    mensaje TEXT NOT NULL,
                    tipo VARCHAR(50),
                    usuario VARCHAR(50) DEFAULT 'sistema_desktop',
                    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estado VARCHAR(20) DEFAULT 'enviado'
                )
            ''')
            print("✅ Base de datos creada/verificada")
            
        except Exception as e:
            print(f"❌ Error creando BD: {e}")

    def crear_interfaz(self):
        """Crear la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="🏥 Clínica San Rafael - Sistema de Correos", 
                         font=('Arial', 16, 'bold'), fg='#2a9d8f', bg='#f0f4f8')
        titulo.pack(pady=(0, 20))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="📧 Enviar Correo Médico", padding="15")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Campos del formulario
        self.crear_campos_formulario(form_frame)
        
        # Plantillas rápidas
        self.crear_plantillas(form_frame)
        
        # Área de mensaje
        self.crear_area_mensaje(form_frame)
        
        # Botones
        self.crear_botones(form_frame)
        
        # Área de logs
        self.crear_area_logs(main_frame)
    
    def crear_campos_formulario(self, parent):
        """Crear campos del formulario"""
        # Nombre del paciente
        ttk.Label(parent, text="👤 Nombre del Paciente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(parent, width=40, font=('Arial', 10))
        self.entry_nombre.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Email del paciente
        ttk.Label(parent, text="📧 Email del Paciente:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_email = ttk.Entry(parent, width=40, font=('Arial', 10))
        self.entry_email.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Teléfono
        ttk.Label(parent, text="📞 Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_telefono = ttk.Entry(parent, width=40, font=('Arial', 10))
        self.entry_telefono.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Tipo de comunicación
        ttk.Label(parent, text="🎯 Tipo de Comunicación:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_tipo = ttk.Combobox(parent, values=[
            "Recordatorio de Cita",
            "Resultados de Exámenes", 
            "Seguimiento Médico",
            "Comunicación General",
            "Comunicación Urgente"
        ], width=37, font=('Arial', 10))
        self.combo_tipo.grid(row=3, column=1, pady=5, padx=(10, 0))
        self.combo_tipo.set("Recordatorio de Cita")
        
        # Asunto
        ttk.Label(parent, text="📝 Asunto:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_asunto = ttk.Entry(parent, width=40, font=('Arial', 10))
        self.entry_asunto.grid(row=4, column=1, pady=5, padx=(10, 0))
    
    def crear_plantillas(self, parent):
        """Crear botones de plantillas rápidas"""
        ttk.Label(parent, text="📋 Plantillas Rápidas:").grid(row=5, column=0, sticky=tk.W, pady=10)
        
        frame_plantillas = ttk.Frame(parent)
        frame_plantillas.grid(row=5, column=1, pady=10, padx=(10, 0), sticky=tk.W)
        
        plantillas = [
            ("📅 Recordatorio", self.cargar_plantilla_recordatorio),
            ("🔬 Resultados", self.cargar_plantilla_resultados),
            ("👨‍⚕️ Seguimiento", self.cargar_plantilla_seguimiento),
            ("🚨 Urgente", self.cargar_plantilla_urgente)
        ]
        
        for i, (texto, comando) in enumerate(plantillas):
            btn = ttk.Button(frame_plantillas, text=texto, command=comando, width=12)
            btn.grid(row=0, column=i, padx=2)
    
    def crear_area_mensaje(self, parent):
        """Crear área de mensaje"""
        ttk.Label(parent, text="💬 Mensaje:").grid(row=6, column=0, sticky=tk.NW, pady=5)
        
        self.text_mensaje = scrolledtext.ScrolledText(parent, width=50, height=8, font=('Arial', 10))
        self.text_mensaje.grid(row=6, column=1, pady=5, padx=(10, 0))
    
    def crear_botones(self, parent):
        """Crear botones de acción"""
        frame_botones = ttk.Frame(parent)
        frame_botones.grid(row=7, column=0, columnspan=2, pady=20)
        
        self.btn_enviar = ttk.Button(frame_botones, text="📤 Enviar Correo", 
                                   command=self.enviar_correo)
        self.btn_enviar.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="🧹 Limpiar", 
                  command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="📊 Ver Historial", 
                  command=self.ver_historial).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="⚙️ Configurar", 
                  command=self.configurar_correo).pack(side=tk.LEFT, padx=5)
    
    def crear_area_logs(self, parent):
        """Crear área de logs"""
        log_frame = ttk.LabelFrame(parent, text="📋 Logs del Sistema", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_logs = scrolledtext.ScrolledText(log_frame, height=8, font=('Consolas', 9))
        self.text_logs.pack(fill=tk.BOTH, expand=True)
        self.text_logs.config(state=tk.DISABLED)
        
        # Log inicial
        self._log("✅ Sistema de correos iniciado")
        self._log("📍 Conectado a base de datos MySQL")

    # Plantillas predefinidas
    def cargar_plantilla_recordatorio(self):
        """Cargar plantilla de recordatorio"""
        nombre = self.entry_nombre.get() or "[Nombre del Paciente]"
        self.entry_asunto.delete(0, tk.END)
        self.entry_asunto.insert(0, "Recordatorio de Cita Médica - Clínica San Rafael")
        
        mensaje = f"""Estimado/a {nombre},

Le recordamos su cita médica programada en nuestra clínica.

Por favor:
• Llegue 15 minutos antes
• Traiga su documento de identificación
• Traiga estudios médicos previos si los tiene

Si necesita reprogramar, contáctenos al +505 2278-9000.

Saludos cordiales,
Equipo Médico - Clínica San Rafael"""
        
        self.text_mensaje.delete(1.0, tk.END)
        self.text_mensaje.insert(1.0, mensaje)
        self.log("📅 Plantilla de recordatorio cargada")
    
    def cargar_plantilla_resultados(self):
        """Cargar plantilla de resultados"""
        nombre = self.entry_nombre.get() or "[Nombre del Paciente]"
        self.entry_asunto.delete(0, tk.END)
        self.entry_asunto.insert(0, "Resultados de Exámenes Disponibles - Clínica San Rafael")
        
        mensaje = f"""Estimado/a {nombre},

Tenemos los resultados de sus exámenes médicos listos para ser revisados.

Pode:
• Recogerlos en recepción
• Solicitar cita para revisión con su médico
• Consultar por nuestro portal en línea

Para mayor información, contáctenos.

Atentamente,
Laboratorio Clínico - Clínica San Rafael"""
        
        self.text_mensaje.delete(1.0, tk.END)
        self.text_mensaje.insert(1.0, mensaje)
        self.log("🔬 Plantilla de resultados cargada")
    
    def cargar_plantilla_seguimiento(self):
        """Cargar plantilla de seguimiento"""
        nombre = self.entry_nombre.get() or "[Nombre del Paciente]"
        self.entry_asunto.delete(0, tk.END)
        self.entry_asunto.insert(0, "Seguimiento Médico - Clínica San Rafael")
        
        mensaje = f"""Estimado/a {nombre},

Como parte de su seguimiento médico, le solicitamos que:

1. Programe una cita de control
2. Realice los exámenes indicados
3. Siga las recomendaciones del tratamiento

Estamos para apoyarle en su proceso de salud.

Cordialmente,
Equipo de Seguimiento - Clínica San Rafael"""
        
        self.text_mensaje.delete(1.0, tk.END)
        self.text_mensaje.insert(1.0, mensaje)
        self.log("👨‍⚕️ Plantilla de seguimiento cargada")
    
    def cargar_plantilla_urgente(self):
        """Cargar plantilla de comunicación urgente"""
        nombre = self.entry_nombre.get() or "[Nombre del Paciente]"
        self.entry_asunto.delete(0, tk.END)
        self.entry_asunto.insert(0, "URGENTE: Comunicación Médica Importante - Clínica San Rafael")
        
        mensaje = f"""Estimado/a {nombre},

Tenemos información médica importante que requiere su atención inmediata.

Por favor contáctenos lo antes posible al +505 2278-9000.

Esto es de carácter urgente.

Atentamente,
Departamento Médico - Clínica San Rafael"""
        
        self.text_mensaje.delete(1.0, tk.END)
        self.text_mensaje.insert(1.0, mensaje)
        self.log("🚨 Plantilla urgente cargada")
    
    def validar_formulario(self):
        """Validar campos del formulario"""
        if not self.entry_nombre.get().strip():
            messagebox.showerror("Error", "❌ Ingrese el nombre del paciente")
            return False
        
        if not self.entry_email.get().strip():
            messagebox.showerror("Error", "❌ Ingrese el email del paciente")
            return False
        
        if not self.entry_asunto.get().strip():
            messagebox.showerror("Error", "❌ Ingrese el asunto del correo")
            return False
        
        mensaje = self.text_mensaje.get(1.0, tk.END).strip()
        if not mensaje or len(mensaje) < 10:
            messagebox.showerror("Error", "❌ El mensaje debe tener al menos 10 caracteres")
            return False
        
        return True
    
    def guardar_en_bd(self, datos):
        """Guardar correo en base de datos"""
        try:
            run_mysql_non_query('''
                INSERT INTO correos_enviados 
                (paciente, email, telefono, asunto, mensaje, tipo, usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                datos['nombre'],
                datos['email'],
                datos.get('telefono', ''),
                datos['asunto'],
                datos['mensaje'],
                datos.get('tipo', 'general'),
                'sistema_desktop'
            ))
            
            self.log("💾 Correo guardado en base de datos")
            return True
            
        except Exception as e:
            self.log(f"❌ Error guardando en BD: {e}")
            return False
    
    def enviar_correo_real(self, datos):
        """Función REAL para enviar correo"""
        try:
            self.log(f"📧 Conectando a {self.config_correo['smtp_server']}...")
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.config_correo['email']
            msg['To'] = datos['email']
            msg['Subject'] = datos['asunto']
            
            # Cuerpo del mensaje
            cuerpo = f"""
            {datos['mensaje']}
            
            ---
            Clínica San Rafael
            Teléfono: +505 2278-9000
            Email: {self.config_correo['email']}
            """
            
            msg.attach(MIMEText(cuerpo, 'plain'))
            
            # Conectar y enviar
            server = smtplib.SMTP(self.config_correo['smtp_server'], self.config_correo['port'])
            server.starttls()  # Habilitar seguridad
            server.login(self.config_correo['email'], self.config_correo['password'])
            server.send_message(msg)
            server.quit()
            
            self.log(f"✅ Correo enviado exitosamente a {datos['email']}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            self.log("❌ Error de autenticación. Verifica usuario y contraseña")
            self.queue.put({
                'tipo': 'mensaje_error', 
                'texto': "❌ Error de autenticación.\n\nVerifica:\n• Tu email y contraseña\n• Que hayas habilitado 'Contraseñas de aplicación' en Gmail\n• Que no estés usando la contraseña normal de Gmail"
            })
            return False
            
        except Exception as e:
            self.log(f"❌ Error enviando correo: {e}")
            self.queue.put({
                'tipo': 'mensaje_error', 
                'texto': f"❌ No se pudo enviar el correo:\n{str(e)}"
            })
            return False
    
    def enviar_correo(self):
        """Manejar envío de correo"""
        if not self.validar_formulario():
            return
        
        # Confirmación
        confirmacion = messagebox.askyesno(
            "Confirmar envío",
            f"¿Enviar correo a:\n\n{self.entry_nombre.get()}\n{self.entry_email.get()}\n\nAsunto: {self.entry_asunto.get()}"
        )
        
        if not confirmacion:
            return
        
        # Deshabilitar botón durante envío
        self.btn_enviar.config(state=tk.DISABLED, text="⏳ Enviando...")
        
        # Datos del correo
        datos = {
            'nombre': self.entry_nombre.get(),
            'email': self.entry_email.get(),
            'telefono': self.entry_telefono.get(),
            'asunto': self.entry_asunto.get(),
            'mensaje': self.text_mensaje.get(1.0, tk.END).strip(),
            'tipo': self.combo_tipo.get()
        }
        
        # Ejecutar en hilo separado
        threading.Thread(target=self.proceso_envio, args=(datos,), daemon=True).start()
    
    def proceso_envio(self, datos):
        """Proceso de envío en hilo separado"""
        try:
            # 1. Guardar en base de datos
            if self.guardar_en_bd(datos):
                self.log("💾 Registro guardado en MySQL")
            
            # 2. Enviar correo REAL
            if self.enviar_correo_real(datos):
                self.queue.put({
                    'tipo': 'mensaje_exito', 
                    'texto': f"✅ Correo enviado a {datos['nombre']}"
                })
            else:
                self.queue.put({
                    'tipo': 'mensaje_error', 
                    'texto': "❌ No se pudo enviar el correo"
                })
                
        except Exception as e:
            self.log(f"❌ Error en proceso: {e}")
            self.queue.put({
                'tipo': 'mensaje_error', 
                'texto': f"❌ Error: {str(e)}"
            })
        
        finally:
            # Rehabilitar botón
            self.queue.put({
                'tipo': 'estado_boton',
                'estado': tk.NORMAL,
                'texto': "📤 Enviar Correo"
            })
    
    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_asunto.delete(0, tk.END)
        self.text_mensaje.delete(1.0, tk.END)
        self.combo_tipo.set("Recordatorio de Cita")
        self.log("🧹 Formulario limpiado")

    def configurar_correo(self):
        """Ventana para configurar credenciales de correo"""
        # Implementación simplificada
        messagebox.showinfo("Configuración", "Configure sus credenciales en config.py")

    def ver_historial(self):
        """Mostrar historial de correos enviados"""
        try:
            resultados = run_mysql_query('''
                SELECT paciente, email, asunto, fecha_envio, estado 
                FROM correos_enviados 
                ORDER BY fecha_envio DESC 
                LIMIT 20
            ''')
            
            if not resultados:
                messagebox.showinfo("Historial", "No hay correos en el historial")
                return
            
            # Crear ventana de historial
            ventana_historial = tk.Toplevel(self.root)
            ventana_historial.title("📊 Historial de Correos")
            ventana_historial.geometry("800x400")
            
            # Treeview para mostrar datos
            tree = ttk.Treeview(ventana_historial, columns=('Paciente', 'Email', 'Asunto', 'Fecha', 'Estado'), show='headings')
            for col in ('Paciente', 'Email', 'Asunto', 'Fecha', 'Estado'):
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            for resultado in resultados:
                tree.insert('', tk.END, values=resultado)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(ventana_historial, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.log("📊 Historial mostrado")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error accediendo al historial: {e}")

# Función para integrar en el sistema principal
def abrir_sistema_correos():
    """Abrir el sistema de correos como ventana independiente"""
    try:
        root = tk.Toplevel()
        app = SistemaCorreosClinica(root)
    except Exception as e:
        messagebox.showerror("Error", f"❌ No se pudo abrir el sistema de correos: {e}")
