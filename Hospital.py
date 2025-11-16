# importaciones de Bibliotecas 
import datetime
from datetime import datetime as dt, timedelta, date
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import pyodbc
from tkcalendar import DateEntry
import time
import os
import random
import hashlib
import threading
import pyttsx3
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure
import pandas as pd
import webbrowser
import os
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import mysql.connector
import logging
import queue
import tkinter as tk

# Modo Oscuro - VERSIÓN CORREGIDA
theme_manager = None
class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.theme_button = None
        self.control_frame = None
        

        
        # Temas mejorados con mejores contrastes
        self.themes = {
            "light": {
                "bg_primary": "#E3F2FD",
                "bg_secondary": "#FFFFFF", 
                "bg_tertiary": "#F8F9FA",
                "text_primary": "#2C3E50",
                "text_secondary": "#5D6D7E",
                "accent_color": "#0A64A4",
                "success_color": "#27AE60",
                "warning_color": "#E67E22",
                "error_color": "#E74C3C",
                "border_color": "#BDC3C7",
                "treeview_bg": "#FFFFFF",
                "treeview_fg": "#2C3E50",
                "treeview_selected": "#90CAF9",
                "button_bg": "#0A64A4",
                "button_fg": "white"
            },
            "dark": {
                "bg_primary": "#1A1A1A",
                "bg_secondary": "#2D2D2D",
                "bg_tertiary": "#3A3A3A", 
                "text_primary": "#ECF0F1",
                "text_secondary": "#BDC3C7",
                "accent_color": "#3498DB",
                "success_color": "#2ECC71",
                "warning_color": "#F39C12",
                "error_color": "#E74C3C",
                "border_color": "#5D6D7E",
                "treeview_bg": "#2D2D2D",
                "treeview_fg": "#ECF0F1",
                "treeview_selected": "#2980B9",
                "button_bg": "#3498DB",
                "button_fg": "white"
            }
        }
    
    def create_theme_button(self):
        """Crear botón de tema de forma directa y confiable"""
        try:
            # Crear frame de controles globales si no existe
            if not self.control_frame:
                self.control_frame = ttk.Frame(self.root)
                self.control_frame.place(relx=0.98, rely=0.02, anchor="ne")
            
            # Crear botón con estado actual
            button_text = "🌙 Modo Oscuro" if self.current_theme == "light" else "☀️ Modo Claro"
            self.theme_button = ttk.Button(
                self.control_frame,
                text=button_text,
                command=self.toggle_theme,
                width=15
            )
            self.theme_button.pack(side='right', padx=5)
            
            print("✅ Botón de tema creado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error creando botón de tema: {e}")
            # Fallback: crear botón directamente en root
            try:
                self.theme_button = ttk.Button(
                    self.root,
                    text="🌙 Tema",
                    command=self.toggle_theme
                )
                self.theme_button.place(relx=0.98, rely=0.02, anchor="ne")
                print("✅ Botón de tema creado en fallback")
                return True
            except Exception as fallback_error:
                print(f"❌ Fallback también falló: {fallback_error}")
                return False
    
    def toggle_theme(self):
        """Cambiar entre temas de forma segura"""
        try:
            # Cambiar tema
            self.current_theme = "dark" if self.current_theme == "light" else "light"
            print(f"🔄 Cambiando a tema: {self.current_theme}")
            
            # Aplicar tema
            self.apply_theme()
            
            # Actualizar texto del botón
            if self.theme_button:
                new_text = "🌙 Modo Oscuro" if self.current_theme == "light" else "☀️ Modo Claro"
                self.theme_button.configure(text=new_text)
                
        except Exception as e:
            print(f"❌ Error cambiando tema: {e}")
    
    def apply_theme(self):
        """Aplicar el tema actual de forma robusta"""
        try:
            theme = self.themes[self.current_theme]
            style = ttk.Style()
            
            # Usar tema 'clam' que es más personalizable
            style.theme_use("clam")
            
            # Configurar estilos ttk
            self._configure_ttk_styles(style, theme)
            
            # Aplicar a ventana principal
            self.root.configure(bg=theme["bg_primary"])
            
            # Aplicar recursivamente a todos los widgets
            self._apply_to_all_widgets(self.root, theme)
            
            print(f"✅ Tema {self.current_theme} aplicado correctamente")
            
        except Exception as e:
            print(f"❌ Error aplicando tema: {e}")
    
    def _configure_ttk_styles(self, style, theme):
        """Configurar estilos ttk de forma centralizada"""
        # Frame
        style.configure("TFrame", 
                       background=theme["bg_primary"],
                       borderwidth=0)
        
        # Label
        style.configure("TLabel",
                       background=theme["bg_primary"],
                       foreground=theme["text_primary"],
                       font=("Segoe UI", 10))
        
        # Button
        style.configure("TButton",
                       background=theme["button_bg"],
                       foreground=theme["button_fg"],
                       focuscolor="none",
                       borderwidth=1,
                       relief="flat")
        style.map("TButton",
                 background=[("active", theme["accent_color"]),
                           ("pressed", theme["accent_color"])])
        
        # Entry
        style.configure("TEntry",
                       fieldbackground=theme["bg_secondary"],
                       foreground=theme["text_primary"],
                       borderwidth=1,
                       relief="solid")
        
        # Combobox
        style.configure("TCombobox",
                       fieldbackground=theme["bg_secondary"],
                       foreground=theme["text_primary"],
                       background=theme["bg_secondary"])
        
        # Notebook
        style.configure("TNotebook",
                       background=theme["bg_primary"],
                       borderwidth=0)
        style.configure("TNotebook.Tab",
                       background=theme["bg_tertiary"],
                       foreground=theme["text_secondary"],
                       padding=[20, 5])
        style.map("TNotebook.Tab",
                 background=[("selected", theme["accent_color"])],
                 foreground=[("selected", "white")])
        
        # Treeview
        style.configure("Treeview",
                       background=theme["treeview_bg"],
                       foreground=theme["treeview_fg"],
                       fieldbackground=theme["treeview_bg"],
                       borderwidth=0,
                       relief="flat")
        style.map("Treeview",
                 background=[("selected", theme["treeview_selected"])])
        
        # Scrollbar
        style.configure("Vertical.TScrollbar",
                       background=theme["bg_tertiary"],
                       troughcolor=theme["bg_primary"],
                       borderwidth=0,
                       relief="flat")
    
    def _apply_to_all_widgets(self, widget, theme):
        """Aplicar tema recursivamente a todos los widgets tkinter"""
        try:
            widget_type = type(widget).__name__
            
            # Aplicar según el tipo de widget
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=theme["bg_primary"])
                
            elif isinstance(widget, tk.Label):
                if widget.cget('bg') not in ['SystemButtonFace', '']:
                    widget.configure(bg=theme["bg_primary"], fg=theme["text_primary"])
                    
            elif isinstance(widget, tk.Button):
                widget.configure(
                    bg=theme["button_bg"],
                    fg=theme["button_fg"],
                    activebackground=theme["accent_color"],
                    activeforeground="white",
                    relief="flat"
                )
                
            elif isinstance(widget, (tk.Entry, tk.Text, tk.Spinbox)):
                widget.configure(
                    bg=theme["bg_secondary"],
                    fg=theme["text_primary"],
                    insertbackground=theme["text_primary"],
                    selectbackground=theme["accent_color"],
                    relief="solid"
                )
                
            elif isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(
                    bg=theme["bg_secondary"],
                    fg=theme["text_primary"],
                    insertbackground=theme["text_primary"]
                )
            
            # Aplicar recursivamente a hijos
            for child in widget.winfo_children():
                self._apply_to_all_widgets(child, theme)
                
        except (tk.TclError, AttributeError) as e:
            # Ignorar errores de widgets que no se pueden configurar
            pass
    
    def initialize(self):
        """Inicialización completa del sistema de temas"""
        print("🎨 Inicializando sistema de temas...")
        
        # 1. Aplicar tema inicial
        self.apply_theme()
        
        # 2. Crear botón de tema
        success = self.create_theme_button()
        
        if success:
            print("✅ Sistema de temas inicializado correctamente")
        else:
            print("⚠️ Sistema de temas inicializado con advertencias")
        
        return success

# SISTEMA PARA ENVIAR CORREO ELECTRONICO 
# ---------------------------
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
        
        # Configuración de la base de datos
        self.config_bd = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'clinica_correos'
        }
        
        # Configuración de correo (REEMPLAZA CON TUS CREDENCIALES REALES)
        self.config_correo = {
            'smtp_server': 'smtp.gmail.com',
            'port': 587,
            'email': 'lopezurbina2018@gmail.com',  # Cambiar por tu email
            'password': 'uynt mkho qwbf xtyp'   # Cambiar por tu contraseña de aplicación
        }
        
        self.crear_base_datos()
        self.crear_interfaz()
        
        # Verificar la cola periódicamente
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
        """Método interno para agregar mensaje al área de logs (solo desde hilo principal)"""
        self.text_logs.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_logs.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.text_logs.config(state=tk.DISABLED)
        self.text_logs.see(tk.END)
        self.root.update_idletasks()
        
    def crear_base_datos(self):
        """Crear la base de datos y tabla si no existen"""
        try:
            # Conectar sin especificar base de datos primero
            conexion = mysql.connector.connect(
                host=self.config_bd['host'],
                port=self.config_bd['port'],
                user=self.config_bd['user'],
                password=self.config_bd['password']
            )
            cursor = conexion.cursor()
            
            # Crear base de datos
            cursor.execute("CREATE DATABASE IF NOT EXISTS clinica_correos")
            cursor.execute("USE clinica_correos")
            
            # Crear tabla
            cursor.execute('''
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
            
            conexion.commit()
            cursor.close()
            conexion.close()
            print("✅ Base de datos creada/verificada")
            
        except mysql.connector.Error as e:
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

Puede:
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
    
    def configurar_correo(self):
        """Ventana para configurar credenciales de correo"""
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configurar Correo")
        config_window.geometry("500x300")
        config_window.resizable(False, False)
        
        ttk.Label(config_window, text="Configuración de Correo", font=('Arial', 12, 'bold')).pack(pady=10)
        
        frame = ttk.Frame(config_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos de configuración
        ttk.Label(frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_email = ttk.Entry(frame, width=30)
        entry_email.grid(row=0, column=1, pady=5, padx=5)
        entry_email.insert(0, self.config_correo['email'])
        
        ttk.Label(frame, text="Contraseña App:").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_password = ttk.Entry(frame, width=30, show="*")
        entry_password.grid(row=1, column=1, pady=5, padx=5)
        entry_password.insert(0, self.config_correo['password'])
        
        ttk.Label(frame, text="Servidor SMTP:").grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_smtp = ttk.Entry(frame, width=30)
        entry_smtp.grid(row=2, column=1, pady=5, padx=5)
        entry_smtp.insert(0, self.config_correo['smtp_server'])
        
        ttk.Label(frame, text="Puerto:").grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_port = ttk.Entry(frame, width=30)
        entry_port.grid(row=3, column=1, pady=5, padx=5)
        entry_port.insert(0, str(self.config_correo['port']))
        
        def guardar_configuracion():
            self.config_correo['email'] = entry_email.get()
            self.config_correo['password'] = entry_password.get()
            self.config_correo['smtp_server'] = entry_smtp.get()
            self.config_correo['port'] = int(entry_port.get())
            
            messagebox.showinfo("Éxito", "✅ Configuración guardada")
            config_window.destroy()
            self.log("⚙️ Configuración de correo actualizada")
        
        ttk.Button(frame, text="💾 Guardar", command=guardar_configuracion).grid(row=4, column=1, pady=20, sticky=tk.E)
    
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
            conexion = mysql.connector.connect(**self.config_bd)
            cursor = conexion.cursor()
            
            cursor.execute('''
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
            
            conexion.commit()
            cursor.close()
            conexion.close()
            
            self.log("💾 Correo guardado en base de datos")
            return True
            
        except mysql.connector.Error as e:
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
        
        # Ejecutar en hilo separado para no bloquiar la interfaz
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
    
    def ver_historial(self):
        """Mostrar historial de correos enviados"""
        try:
            conexion = mysql.connector.connect(**self.config_bd)
            cursor = conexion.cursor()
            
            cursor.execute('''
                SELECT paciente, email, asunto, fecha_envio, estado 
                FROM correos_enviados 
                ORDER BY fecha_envio DESC 
                LIMIT 20
            ''')
            
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()
            
            # Crear ventana de historial
            ventana_historial = tk.Toplevel(self.root)
            ventana_historial.title("📊 Historial de Correos")
            ventana_historial.geometry("800x400")
            
            # Treeview para mostrar datos
            tree = ttk.Treeview(ventana_historial, columns=('Paciente', 'Email', 'Asunto', 'Fecha', 'Estado'), show='headings')
            tree.heading('Paciente', text='Paciente')
            tree.heading('Email', text='Email')
            tree.heading('Asunto', text='Asunto')
            tree.heading('Fecha', text='Fecha')
            tree.heading('Estado', text='Estado')
            
            for col in ('Paciente', 'Email', 'Asunto', 'Fecha', 'Estado'):
                tree.column(col, width=150)
            
            for resultado in resultados:
                tree.insert('', tk.END, values=resultado)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(ventana_historial, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.log("📊 Historial mostrado")
            
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"❌ Error accediendo al historial: {e}")

# Función para integrar en tu sistema principal
def abrir_sistema_correos():
    """Abrir el sistema de correos como ventana independiente"""
    try:
        root = tk.Toplevel()
        app = SistemaCorreosClinica(root)
    except Exception as e:
        messagebox.showerror("Error", f"❌ No se pudo abrir el sistema de correos: {e}")


# SISTEMA DE PERMISOS Y ROLES (ACTUALIZADO)
# ---------------------------
class SistemaPermisos:
    def __init__(self):
        self.permisos_por_rol = {
            'Administrador': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'usuarios', 'reportes', 'configuracion', 'citas'],
                'acciones': ['crear', 'leer', 'actualizar', 'eliminar', 'exportar', 'configurar', 'visualizar'],
                'descripcion': 'Acceso completo al sistema incluyendo reportes'
            },
            'Médico': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'reportes', 'citas'],  # ✅ Reportes incluido
                'acciones': ['crear', 'leer', 'actualizar', 'exportar', 'visualizar'],
                'descripcion': 'Acceso a consultas, gestión de citas y reportes'
            },
            'Enfermero': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'citas', 'reportes'],  # ✅ Reportes incluido
                'acciones': ['crear', 'leer', 'actualizar', 'exportar', 'visualizar'],
                'descripcion': 'Gestión de medicamentos, citas y reportes básicos'
            },
            'Recepcionista': {
                'modulos': ['inventario', 'movimientos', 'citas', 'reportes'],  # ✅ Reportes incluido
                'acciones': ['crear', 'leer', 'actualizar', 'exportar', 'visualizar'],
                'descripcion': 'Gestión de citas y consulta básica con reportes'
            }
        }

    def tiene_permiso(self, rol, modulo, accion=None):
        """Verificar si un rol tiene permiso para un módulo y acción"""
        if rol not in self.permisos_por_rol:
            return False

        permisos = self.permisos_por_rol[rol]

        if modulo not in permisos['modulos']:
            return False

        if accion and accion not in permisos['acciones']:
            return False

        return True

    def obtener_modulos_visibles(self, rol):
        """Obtener lista de módulos visibles para un rol"""
        if rol in self.permisos_por_rol:
            return self.permisos_por_rol[rol]['modulos']
        return []

    def obtener_descripcion_rol(self, rol):
        """Obtener descripción del rol"""
        if rol in self.permisos_por_rol:
            return self.permisos_por_rol[rol]['descripcion']
        return "Rol desconocido"
    # ============================================================
# FUNCIONES DE CITAS FLEXIBLES (DEBEN IR AL INICIO)
# ============================================================

def crear_tabla_citas_flexibles():
    """Crear tabla para citas flexibles (si no existe)"""
    try:
        run_non_query("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CitasFlexibles' AND xtype='U')
        CREATE TABLE CitasFlexibles (
            IdCita INT IDENTITY PRIMARY KEY,
            Paciente NVARCHAR(100) NOT NULL,
            Doctor NVARCHAR(100) NOT NULL,
            Especialidad NVARCHAR(100) NOT NULL,
            FechaCita DATETIME NOT NULL,
            Observaciones NVARCHAR(255) NULL,
            Estado NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
            UsuarioCreacion NVARCHAR(100) NOT NULL,
            FechaCreacion DATETIME NOT NULL DEFAULT GETDATE()
        );
        """)
        print("✅ Tabla CitasFlexibles creada/verificada")
    except Exception as e:
        print(f"Error creando tabla flexible: {e}")

def generar_intervalos_horarios(hora_inicio="08:00", hora_fin="17:30", intervalo_minutos=15):
    """Genera lista de strings con horarios (HH:MM)"""
    horarios = []
    h0 = dt.strptime(hora_inicio, "%H:%M")
    hf = dt.strptime(hora_fin, "%H:%M")
    cur = h0
    while cur <= hf:
        horarios.append(cur.strftime("%H:%M"))
        cur += timedelta(minutes=intervalo_minutos)
    return horarios

def limpiar_formulario_cita():
    """Limpiar formulario de citas"""
    # Estas variables se definirán después, pero la función puede existir
    pass

def cargar_citas_flexibles():
    """Cargar citas desde la tabla flexible"""
    # Esta función se implementará después de definir tree_citas
    pass

def agendar_cita_flexible():
    """Agendar cita sin depender de IDs de base de datos"""
    if not verificar_permiso('citas', 'crear'):
        mostrar_error_permiso()
        return
    # Implementación completa más adelante
    pass

def editar_cita_flexible():
    """Editar cita flexible"""
    if not verificar_permiso('citas', 'actualizar'):
        mostrar_error_permiso()
        return
    pass

def cancelar_cita_flexible():
    """Cancelar cita flexible"""
    if not verificar_permiso('citas', 'eliminar'):
        mostrar_error_permiso()
        return
    pass

def buscar_citas_flexibles():
    """Buscar citas flexibles"""
    pass

def exportar_citas_csv():
    """Exportar citas a CSV"""
    pass
# ---------------------------
# SISTEMA DE VOZ PARA EL ASISTENTE
# ---------------------------
class AsistenteVoz:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.configurar_voz()
        self.hablando = False
        
    def configurar_voz(self):
        """Configurar propiedades de la voz"""
        voices = self.engine.getProperty('voices')
        
        # Intentar usar voz en español si está disponible
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
            elif 'english' in voice.name.lower() and 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
        
        self.engine.setProperty('rate', 150)    # Velocidad de habla
        self.engine.setProperty('volume', 0.8)  # Volumen (0.0 a 1.0)
    
    def hablar(self, texto):
        """Reproducir texto en voz (en hilo separado)"""
        def hablar_hilo():
            try:
                self.hablando = True
                self.engine.say(texto)
                self.engine.runAndWait()
                self.hablando = False
            except Exception as e:
                print(f"Error en síntesis de voz: {e}")
                self.hablando = False
        
        if not self.hablando:
            threading.Thread(target=hablar_hilo, daemon=True).start()

# Crear instancia global del asistente de voz
asistente_voz = AsistenteVoz()
# ---------------------------
# SISTEMA DE LOGIN CON PERMISOS
# ---------------------------
class SistemaLogin:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Clínica Popular San Rafael - Acceso al Sistema")
        self.login_window.geometry("450x550")
        self.login_window.configure(bg='#2C3E50')
        self.login_window.resizable(False, False)
        self.login_window.protocol("WM_DELETE_WINDOW", self.salir_sistema)

        # Sistema de permisos
        self.sistema_permisos = SistemaPermisos()

        # Centrar ventana
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (550 // 2)
        self.login_window.geometry(f"450x550+{x}+{y}")

        self.crear_interfaz_login()
        self.cargar_usuarios_db()

    def crear_interfaz_login(self):
        # Frame principal
        main_frame = tk.Frame(self.login_window, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Logo/Header
        header_frame = tk.Frame(main_frame, bg='#2C3E50')
        header_frame.pack(pady=(0, 30))

        tk.Label(
            header_frame,
            text="🏥",
            font=('Arial', 48),
            bg='#2C3E50',
            fg='#3498DB'
        ).pack()

        tk.Label(
            header_frame,
            text="Clínica San Rafael",
            font=('Arial', 20, 'bold'),
            bg='#2C3E50',
            fg='#ECF0F1'
        ).pack(pady=(10, 5))

        tk.Label(
            header_frame,
            text="Sistema de Gestión Médica",
            font=('Arial', 12),
            bg='#2C3E50',
            fg='#BDC3C7'
        ).pack()

        # Información de roles
        info_frame = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))

        tk.Label(
            info_frame,
            text="👥 Roles del Sistema:",
            font=('Arial', 10, 'bold'),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack(pady=(10, 5))

        roles_text = "• Admin: Acceso completo\n• Médico: Consultas y visualización\n• Enfermero: Gestión medicamentos\n• Recepcionista: Consulta básica"
        tk.Label(
            info_frame,
            text=roles_text,
            font=('Arial', 8),
            bg='#34495E',
            fg='#BDC3C7',
            justify='left'
        ).pack(pady=(0, 10))

        # Formulario de login
        form_frame = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
        form_frame.pack(fill='x', pady=20, padx=10)

        # Usuario
        tk.Label(
            form_frame,
            text="👤 Usuario:",
            font=('Arial', 11, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        ).grid(row=0, column=0, sticky='w', padx=15, pady=(20, 10))

        self.entry_usuario = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=20,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.entry_usuario.grid(row=0, column=1, padx=15, pady=(20, 10))
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())

        # Contraseña
        tk.Label(
            form_frame,
            text="🔒 Contraseña:",
            font=('Arial', 11, 'bold'),
            fg='#ECF0F1',
            bg='#34495E'
        ).grid(row=1, column=0, sticky='w', padx=15, pady=10)

        self.entry_password = tk.Entry(
            form_frame,
            font=('Arial', 11),
            width=20,
            show='•',
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.entry_password.grid(row=1, column=1, padx=15, pady=10)
        self.entry_password.bind('<Return>', lambda e: self.verificar_login())

        # Botón mostrar/ocultar contraseña
        self.btn_toggle_pass = tk.Button(
            form_frame,
            text="👁️",
            font=('Arial', 9),
            command=self.toggle_password,
            bg='#3498DB',
            fg='white',
            width=3,
            relief='flat'
        )
        self.btn_toggle_pass.grid(row=1, column=2, padx=(5, 15), pady=10)

        # Botones
        btn_frame = tk.Frame(form_frame, bg='#34495E')
        btn_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.btn_login = tk.Button(
            btn_frame,
            text="🚀 INICIAR SESIÓN",
            font=('Arial', 12, 'bold'),
            command=self.verificar_login,
            bg='#27AE60',
            fg='white',
            width=15,
            height=1,
            relief='flat'
        )
        self.btn_login.pack(pady=5)

        tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            font=('Arial', 9),
            command=self.limpiar_formulario,
            bg='#E74C3C',
            fg='white',
            relief='flat'
        ).pack(pady=5)

        # Información de sesión
        self.info_frame = tk.Frame(main_frame, bg='#2C3E50')
        self.info_frame.pack(fill='x', pady=10)

        self.lbl_info = tk.Label(
            self.info_frame,
            text="",
            font=('Arial', 9),
            bg='#2C3E50',
            fg='#BDC3C7'
        )
        self.lbl_info.pack()

        # Estado del sistema
        estado_frame = tk.Frame(main_frame, bg='#2C3E50')
        estado_frame.pack(fill='x', pady=5)

        self.lbl_estado = tk.Label(
            estado_frame,
            text="● Sistema listo",
            font=('Arial', 8),
            bg='#2C3E50',
            fg='#27AE60'
        )
        self.lbl_estado.pack()

        self.entry_usuario.focus()

    def hash_password(self, password):
        """Encriptar contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def cargar_usuarios_db(self):
        """Cargar usuarios desde la base de datos"""
        try:
            
            self.usuarios = {}
            query = "SELECT Nombre, Password, Rol, Estado FROM Usuarios WHERE Estado = 'Activo'"
            rows = run_query(query)

            for row in rows:
                nombre, password, rol, estado = row
                self.usuarios[nombre.lower()] = {
                    'password': password,
                    'rol': rol,
                    'estado': estado
                }

            self.lbl_info.config(text=f"✅ {len(self.usuarios)} usuarios activos cargados")
        except Exception as e:
            self.lbl_info.config(text="⚠️ Error cargando usuarios")
    
    def toggle_password(self):
        """Mostrar/ocultar contraseña"""
        if self.entry_password.cget('show') == '•':
            self.entry_password.config(show='')
            self.btn_toggle_pass.config(text='🙈', bg='#E74C3C')
        else:
            self.entry_password.config(show='•')
            self.btn_toggle_pass.config(text='👁️', bg='#3498DB')

    def limpiar_formulario(self):
        """Limpiar campos del formulario"""
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_usuario.focus()
        self.lbl_estado.config(text="● Formulario limpiado", fg='#3498DB')

    def verificar_login(self):
        """Verificar credenciales del usuario"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not usuario or not password:
            self.mostrar_error("Por favor, complete todos los campos")
            return

        # Verificar en base de datos
        usuario_key = usuario.lower()
        if usuario_key not in self.usuarios:
            self.mostrar_error("Usuario no encontrado")
            return

        user_data = self.usuarios[usuario_key]

        # Verificar contraseña (comparar hash)
        password_hash = self.hash_password(password)
        if user_data['password'] != password_hash:
            self.mostrar_error("Contraseña incorrecta")
            return

        # Verificar estado
        if user_data['estado'] != 'Activo':
            self.mostrar_error("Usuario inactivo. Contacte al administrador.")
            return

        # Login exitoso
        self.login_exitoso(usuario, user_data['rol'])

    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error con animación"""
        self.lbl_estado.config(text=f"⚠️ {mensaje}", fg='#E74C3C')

        # Animación de error
        original_bg = self.btn_login.cget('bg')
        self.btn_login.config(bg='#E74C3C')
        self.login_window.after(300, lambda: self.btn_login.config(bg=original_bg))

    def login_exitoso(self, usuario, rol):
        """Procedimiento de login exitoso"""
        self.lbl_estado.config(text=f"✅ ¡Acceso concedido! Rol: {rol}", fg='#27AE60')
        self.btn_login.config(state='disabled', text="⏳ CARGANDO...")

        # Mostrar información del rol
        descripcion = self.sistema_permisos.obtener_descripcion_rol(rol)
        self.lbl_info.config(text=f"Rol: {rol} - {descripcion}")

        # Animación de éxito
        def animar_exito():
            colores = ['#27AE60', '#2ECC71', '#27AE60']
            for color in colores:
                self.btn_login.config(bg=color)
                self.login_window.update()
                time.sleep(0.2)

            # Guardar información de sesión
            self.usuario_actual = usuario
            self.rol_actual = rol

            # Cerrar ventana de login y abrir sistema principal
            self.login_window.after(1000, self.iniciar_sistema_principal)

        threading.Thread(target=animar_exito, daemon=True).start()

    def iniciar_sistema_principal(self):
        """Iniciar el sistema principal"""
        self.login_window.destroy()

        # Mostrar animación de inicio del sistema principal
        mostrar_animacion_inicio()

        # Guardar información del usuario en variables globales
        global USUARIO_ACTUAL, ROL_ACTUAL, SISTEMA_PERMISOS
        USUARIO_ACTUAL = self.usuario_actual
        ROL_ACTUAL = self.rol_actual
        SISTEMA_PERMISOS = self.sistema_permisos

    def salir_sistema(self):
        """Salir completamente del sistema"""
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir del sistema?"):
            self.login_window.quit()
            self.login_window.destroy()
# Variables globales para la sesión
USUARIO_ACTUAL = None
ROL_ACTUAL = None
SISTEMA_PERMISOS = None
modulo_reportes = None
frame_grafica_actual = None
def mostrar_animacion_inicio():
    """Muestra una animación de inicio moderna aleatoria"""
    animaciones_modernas.mostrar_animacion_aleatoria()
# ---------------------------
# FUNCIONES DE CONTROL DE ACCESO
# ---------------------------
def verificar_permiso(modulo, accion=None):
    """Verificar si el usuario actual tiene permiso"""
    global ROL_ACTUAL, SISTEMA_PERMISOS
    if not ROL_ACTUAL or not SISTEMA_PERMISOS:
        return False
    return SISTEMA_PERMISOS.tiene_permiso(ROL_ACTUAL, modulo, accion)

def mostrar_error_permiso():
    """Mostrar mensaje de error de permisos"""
    messagebox.showerror(
        "Acceso Denegado",
        "❌ No tiene permisos para realizar esta acción.\n\n"
        f"Usuario: {USUARIO_ACTUAL}\n"
        f"Rol: {ROL_ACTUAL}\n\n"
        "Contacte al administrador del sistema."
    )

def configurar_interfaz_por_rol():
    """Configurar la interfaz según los permisos del rol"""
    global ROL_ACTUAL, SISTEMA_PERMISOS, notebook

    if not ROL_ACTUAL or not SISTEMA_PERMISOS:
        return

    modulos_permitidos = SISTEMA_PERMISOS.obtener_modulos_visibles(ROL_ACTUAL)

    # Diccionario de pestañas y sus módulos correspondientes (ACTUALIZADO)
    tabs_modulos = {
         "📦 Inventario": "inventario",
        "⚠️ Alertas": "alertas", 
        "📊 Movimientos": "movimientos",
        "👥 Usuarios": "usuarios",
        "📅 Citas": "citas",
        "📈 Reportes": "reportes"  # NUEVA PESTAÑA
    }

    # Ocultar pestañas no permitidas
    for tab_text, modulo in tabs_modulos.items():
        if modulo not in modulos_permitidos:
            # Encontrar y ocultar la pestaña
            for tab_id in notebook.tabs():
                if notebook.tab(tab_id, "text") == tab_text:
                    notebook.forget(tab_id)
                    break

# ---------------------------
# MODIFICACIONES EN LAS FUNCIONES EXISTENTES CON CONTROL DE PERMISOS
# ---------------------------
# 1. INVENTARIO - FUNCIONES CON PERMISOS
def agregar_producto_seguro():
    if not verificar_permiso('inventario', 'crear'):
        mostrar_error_permiso()
        return

    try:
        nombre = entry_nombre.get().strip()
        stock = entry_stock.get().strip()
        fecha_venc = fecha_vencimiento.get_date()

        if not nombre or not stock:
            messagebox.showwarning("Datos incompletos", "Por favor complete nombre y stock")
            return

        if run_non_query("INSERT INTO Productos (Nombre, Stock, FechaVencimiento) VALUES (?, ?, ?)",
                        (nombre, int(stock), fecha_venc)):
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            limpiar_formulario_inv()
            cargar_inventario()
            registrar_movimiento_seguro(nombre, 'ENTRADA', int(stock))
    except ValueError:
        messagebox.showerror("Error", "El stock debe ser un número válido")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto:\n{str(e)}")

def editar_producto_seguro():
    if not verificar_permiso('inventario', 'actualizar'):
        mostrar_error_permiso()
        return

    item = tree_inv.selection()
    if not item:
        messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para editar")
        return

    try:
        valores = tree_inv.item(item[0])["values"]
        if not valores:
            return

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, valores[2])

        btn_agregar.config(state="disabled")
        if not hasattr(editar_producto_seguro, 'btn_actualizar'):
            editar_producto_seguro.btn_actualizar = ttk.Button(frame_form_inv, text="✅ Actualizar",
                                                       command=lambda: actualizar_producto_seguro(valores[0]))
            editar_producto_seguro.btn_actualizar.grid(row=0, column=7, padx=5, pady=2)
            editar_producto_seguro.btn_cancelar = ttk.Button(frame_form_inv, text="❌ Cancelar",
                                                     command=cancelar_edicion)
            editar_producto_seguro.btn_cancelar.grid(row=0, column=8, padx=5, pady=2)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el producto:\n{str(e)}")

def eliminar_producto_seguro():
    if not verificar_permiso('inventario', 'eliminar'):
        mostrar_error_permiso()
        return

    item = tree_inv.selection()
    if not item:
        messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para eliminar")
        return

    try:
        valores = tree_inv.item(item[0])["values"]
        if not valores:
            return

        id_producto = int(valores[0])
        nombre_producto = valores[1]
        stock_producto = valores[2]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {nombre_producto}?"):
            if run_non_query("DELETE FROM Productos WHERE Id=?", (id_producto,)):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                cargar_inventario()
                fecha_actual = datetime.date.today()
                registrar_movimiento_seguro(nombre_producto, 'BAJA', stock_producto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{str(e)}")

def actualizar_producto_seguro(id_producto):
    try:
        nombre = entry_nombre.get().strip()
        stock = entry_stock.get().strip()
        fecha_venc = fecha_vencimiento.get_date()

        if not nombre or not stock:
            messagebox.showwarning("Datos incompletos", "Por favor complete nombre y stock")
            return

        id_numero = int(id_producto)

        if run_non_query("UPDATE Productos SET Nombre=?, Stock=?, FechaVencimiento=? WHERE Id=?",
                        (nombre, int(stock), fecha_venc, id_numero)):
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            cancelar_edicion()
            cargar_inventario()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{str(e)}")

def registrar_movimiento_seguro(producto, tipo, cantidad):
    try:
        fecha_actual = datetime.date.today()
        run_non_query("INSERT INTO Movimientos (Producto, Tipo, Cantidad, Usuario, Fecha) VALUES (?, ?, ?, ?, ?)",
                     (producto, tipo, cantidad, USUARIO_ACTUAL, fecha_actual))
    except Exception as e:
        print(f"Error al registrar movimiento: {str(e)}")

# 2. ALERTAS - FUNCIONES CON PERMISOS
def reponer_stock_seguro():
    if not verificar_permiso('alertas', 'actualizar'):
        mostrar_error_permiso()
        return

    item = tree_alert.selection()
    if not item:
        messagebox.showwarning("Selección requerida", "Por favor seleccione un producto para reponer")
        return

    try:
        valores = tree_alert.item(item[0])["values"]
        if not valores:
            return

        ventana_reponer = tk.Toplevel(root)
        ventana_reponer.title("Reponer Stock")
        ventana_reponer.geometry("300x150")
        ventana_reponer.transient(root)
        ventana_reponer.grab_set()

        ttk.Label(ventana_reponer, text=f"Producto: {valores[1]}").pack(pady=5)
        ttk.Label(ventana_reponer, text=f"Stock actual: {valores[2]}").pack(pady=5)
        ttk.Label(ventana_reponer, text="Cantidad a reponer:").pack(pady=5)

        entry_cantidad = ttk.Entry(ventana_reponer, width=10)
        entry_cantidad.pack(pady=5)
        entry_cantidad.focus()

        def confirmar_reposicion():
            try:
                cantidad = int(entry_cantidad.get())
                if cantidad <= 0:
                    messagebox.showwarning("Error", "La cantidad debe ser mayor a 0")
                    return

                nuevo_stock = valores[2] + cantidad
                if run_non_query("UPDATE Productos SET Stock=? WHERE Id=?", (nuevo_stock, valores[0])):
                    registrar_movimiento_seguro(valores[1], 'REPOSICIÓN', cantidad)
                    messagebox.showinfo("Éxito", f"Stock repuesto. Nuevo stock: {nuevo_stock}")
                    ventana_reponer.destroy()
                    cargar_alertas()
                    cargar_inventario()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

        ttk.Button(ventana_reponer, text="✅ Confirmar", command=confirmar_reposicion).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reponer el stock:\n{str(e)}")

def exportar_alertas_seguro():
    if not verificar_permiso('alertas', 'exportar'):
        mostrar_error_permiso()
        return

    try:
        filename = f"alertas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"REPORTE DE ALERTAS - Clínica San Rafael\n")
            f.write(f"Generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("="*60 + "\n\n")

            for child in tree_alert.get_children():
                valores = tree_alert.item(child)["values"]
                f.write(f"● Producto: {valores[1]}\n")
                f.write(f"  Stock: {valores[2]} | Vencimiento: {valores[3]}\n")
                f.write(f"  Alerta: {valores[4]} | Gravedad: {valores[5]}\n")
                f.write("-" * 40 + "\n")

        messagebox.showinfo("Exportación Exitosa", f"Alertas exportadas a '{filename}'")
        os.startfile(filename)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron exportar las alertas:\n{str(e)}")

# 3. MOVIMIENTOS - FUNCIONES CON PERMISOS
def exportar_movimientos_seguro():
    if not verificar_permiso('movimientos', 'exportar'):
        mostrar_error_permiso()
        return

    try:
        filename = f"movimientos_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("ID,Producto,Tipo,Cantidad,Usuario,Fecha\n")
            for child in tree_mov.get_children():
                valores = tree_mov.item(child)["values"]
                f.write(",".join(str(v) for v in valores) + "\n")

        messagebox.showinfo("Exportación Exitosa", f"Movimientos exportados a '{filename}'")
        os.startfile(filename)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron exportar los movimientos:\n{str(e)}")

# 4. USUARIOS - SOLO ADMINISTRADOR
def agregar_usuario_seguro():
    if not verificar_permiso('usuarios', 'crear'):
        mostrar_error_permiso()
        return

    try:
        nombre = entry_nombre_usr.get().strip()
        rol = combo_rol.get().strip()

        if not nombre:
            messagebox.showwarning("Datos incompletos", "Por favor ingrese el nombre del usuario")
            return

        if not rol:
            messagebox.showwarning("Datos incompletos", "Por favor seleccione un rol")
            return

        # Verificar si el usuario ya existe
        existing = run_query("SELECT COUNT(*) FROM Usuarios WHERE LOWER(Nombre) = LOWER(?)", (nombre,))
        if existing and existing[0][0] > 0:
            messagebox.showwarning("Usuario existente", f"El usuario '{nombre}' ya existe en el sistema")
            return

        # Generar contraseña por defecto (hash del nombre)
        password_hash = hashlib.sha256(nombre.encode()).hexdigest()

        if run_non_query("INSERT INTO Usuarios (Nombre, Password, Rol, Estado) VALUES (?, ?, ?, 'Activo')",
                        (nombre, password_hash, rol)):
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' agregado correctamente\nContraseña inicial: mismo que el usuario")
            limpiar_formulario_usr()
            cargar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el usuario:\n{str(e)}")

def eliminar_usuario_seguro():
    if not verificar_permiso('usuarios', 'eliminar'):
        mostrar_error_permiso()
        return

    item = tree_usr.selection()
    if not item:
        messagebox.showwarning("Selección requerida", "Por favor seleccione un usuario para eliminar")
        return

    try:
        valores = tree_usr.item(item[0])["values"]
        if not valores or len(valores) < 2:
            return

        id_usuario = int(valores[0])
        nombre_usuario = valores[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario {nombre_usuario}?"):
            if run_non_query("DELETE FROM Usuarios WHERE Id=?", (id_usuario,)):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                cargar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el usuario:\n{str(e)}")

def cambiar_estado_seguro():
    if not verificar_permiso('usuarios', 'actualizar'):
        mostrar_error_permiso()
        return

    item = tree_usr.selection()
    if not item:
        messagebox.showwarning("Selección requerida", "Por favor seleccione un usuario")
        return

    try:
        valores = tree_usr.item(item[0])["values"]
        if not valores or len(valores) < 4:
            return

        id_usuario = int(valores[0])
        nombre_usuario = valores[1]
        estado_actual = valores[3]

        nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"

        if run_non_query("UPDATE Usuarios SET Estado=? WHERE Id=?", (nuevo_estado, id_usuario)):
            cargar_usuarios()
            messagebox.showinfo("Estado actualizado", f"Usuario {nombre_usuario} ahora está {nuevo_estado}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cambiar el estado:\n{str(e)}")

# 5. CITAS - FUNCIONES CON PERMISOS (NUEVAS)
def agendar_cita_seguro():
    if not verificar_permiso('citas', 'crear'):
        mostrar_error_permiso()
        return
    agendar_cita_flexible()

def editar_cita_seguro():
    if not verificar_permiso('citas', 'actualizar'):
        mostrar_error_permiso()
        return
    editar_cita_flexible()

def cancelar_cita_seguro():
    if not verificar_permiso('citas', 'eliminar'):
        mostrar_error_permiso()
        return
    cancelar_cita_flexible()

def exportar_citas_csv_seguro():
    if not verificar_permiso('citas', 'exportar'):
        mostrar_error_permiso()
        return
    exportar_citas_csv()
# ---------------------------
# CONFIGURACIÓN DE BOTONES SEGÚN PERMISOS
# ---------------------------
def configurar_botones_por_permisos():
    """Configurar estado de botones según permisos"""

    # Inventario
    if not verificar_permiso('inventario', 'crear'):
        btn_agregar.config(state='disabled')
    if not verificar_permiso('inventario', 'eliminar'):
        # Deshabilitar botón de eliminar en inventario
        for widget in frame_form_inv.winfo_children():
            if isinstance(widget, ttk.Button) and 'Eliminar' in widget.cget('text'):
                widget.config(state='disabled')

    # Alertas
    if not verificar_permiso('alertas', 'actualizar'):
        # Deshabilitar botón de reponer stock
        for widget in frame_controles_alert.winfo_children():
            if isinstance(widget, ttk.Button) and 'Reponer' in widget.cget('text'):
                widget.config(state='disabled')

    # Movimientos - exportar
    if not verificar_permiso('movimientos', 'exportar'):
        # Deshabilitar botón de exportar en movimientos
        for widget in frame_controles_mov.winfo_children():
            if isinstance(widget, ttk.Button) and 'Exportar' in widget.cget('text'):
                widget.config(state='disabled')

    # Usuarios
    if not verificar_permiso('usuarios', 'crear'):
        for widget in frame_controles_usr.winfo_children():
            if isinstance(widget, ttk.Button) and 'Agregar' in widget.cget('text'):
                widget.config(state='disabled')

    if not verificar_permiso('usuarios', 'eliminar'):
        for widget in frame_controles_usr.winfo_children():
            if isinstance(widget, ttk.Button) and 'Eliminar' in widget.cget('text'):
                widget.config(state='disabled')

    if not verificar_permiso('usuarios', 'actualizar'):
        for widget in frame_controles_usr.winfo_children():
            if isinstance(widget, ttk.Button) and 'Activar/Inactivar' in widget.cget('text'):
                widget.config(state='disabled')

    # CITAS - permisos (NUEVO)
    if not verificar_permiso('citas', 'crear'):
        btn_agendar_cita.config(state='disabled')
    if not verificar_permiso('citas', 'actualizar'):
        btn_editar_cita.config(state='disabled') 
    if not verificar_permiso('citas', 'eliminar'):
        btn_cancelar_cita.config(state='disabled')
    if not verificar_permiso('citas', 'exportar'):
        # Deshabilitar botón de exportar en citas
        for widget in frame_controles_citas.winfo_children():
            if isinstance(widget, ttk.Button) and 'Exportar' in widget.cget('text'):
                widget.config(state='disabled')

class ModuloReportes:
    def __init__(self):
        self.style_moderno = {
            'bg_color': '#1a1a1a',
            'text_color': '#ffffff',
            'accent_color': '#00ff88',
            'grid_color': '#333333'
        }
        plt.style.use('dark_background')
        self.configurar_estilo_moderno()
    
    def configurar_estilo_moderno(self):
        """Configura el estilo moderno para las gráficas"""
        sns.set_style("darkgrid")
        plt.rcParams['figure.facecolor'] = self.style_moderno['bg_color']
        plt.rcParams['axes.facecolor'] = self.style_moderno['bg_color']
        plt.rcParams['axes.edgecolor'] = self.style_moderno['grid_color']
        plt.rcParams['axes.labelcolor'] = self.style_moderno['text_color']
        plt.rcParams['text.color'] = self.style_moderno['text_color']
        plt.rcParams['xtick.color'] = self.style_moderno['text_color']
        plt.rcParams['ytick.color'] = self.style_moderno['text_color']
    
    def crear_grafica_stock(self, frame_parent):
        """Crear gráfica de distribución de stock - CORREGIDA"""
        try:
            # Obtener datos
            query = """
                SELECT 
                    CASE 
                        WHEN Stock < 5 THEN 'Crítico (<5)'
                        WHEN Stock BETWEEN 5 AND 10 THEN 'Bajo (5-10)'
                        WHEN Stock BETWEEN 11 AND 30 THEN 'Normal (11-30)'
                        ELSE 'Alto (>30)'
                    END as Nivel,
                    COUNT(*) as Cantidad
                FROM Productos 
                GROUP BY 
                    CASE 
                        WHEN Stock < 5 THEN 'Crítico (<5)'
                        WHEN Stock BETWEEN 5 AND 10 THEN 'Bajo (5-10)'
                        WHEN Stock BETWEEN 11 AND 30 THEN 'Normal (11-30)'
                        ELSE 'Alto (>30)'
                    END
                ORDER BY Cantidad DESC
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "stock")
            
            niveles = [d[0] for d in datos]
            cantidades = [d[1] for d in datos]
            
            # Crear figura
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)
            
            # Colores según nivel de stock
            colores = ['#ff4444', '#ffaa00', '#44ff44', '#4444ff']
            bars = ax.bar(niveles, cantidades, color=colores[:len(niveles)], alpha=0.8)
            
            # Personalizar
            ax.set_title('📊 Distribución de Niveles de Stock', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Cantidad de Productos', fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Agregar valores en las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            # Rotar etiquetas si son largas
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Ajustar diseño
            fig.tight_layout()
            
            # Embedder en tkinter
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
            
        except Exception as e:
            print(f"Error creando gráfica stock: {e}")
            return self.crear_mensaje_error(frame_parent)
    
    def crear_grafica_vencimientos(self, frame_parent):
        """Crear gráfica de productos por vencimiento"""
        try:
            query = """
                SELECT 
                    CASE 
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) < 0 THEN 'Vencido'
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) BETWEEN 0 AND 30 THEN 'Próximo a Vencer (0-30 días)'
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) BETWEEN 31 AND 90 THEN 'Vence en 31-90 días'
                        ELSE 'Vence en más de 90 días'
                    END as Estado,
                    COUNT(*) as Cantidad
                FROM Productos 
                GROUP BY 
                    CASE 
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) < 0 THEN 'Vencido'
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) BETWEEN 0 AND 30 THEN 'Próximo a Vencer (0-30 días)'
                        WHEN DATEDIFF(day, GETDATE(), FechaVencimiento) BETWEEN 31 AND 90 THEN 'Vence en 31-90 días'
                        ELSE 'Vence en más de 90 días'
                    END
                ORDER BY Cantidad DESC
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "vencimientos")
            
            estados = [d[0] for d in datos]
            cantidades = [d[1] for d in datos]
            
            fig = Figure(figsize=(8, 5), dpi=100)
            ax = fig.add_subplot(111)
            
            colores = ['#ff4444', '#ffaa00', '#44ff44', '#4444ff']
            bars = ax.bar(estados, cantidades, color=colores[:len(estados)], alpha=0.8)
            
            ax.set_title('📅 Productos por Estado de Vencimiento', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Cantidad de Productos', fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
        except Exception as e:
            print(f"Error creando gráfica vencimientos: {e}")
            return self.crear_mensaje_error(frame_parent)
    
    def crear_grafica_movimientos(self, frame_parent):
        """Crear gráfica de movimientos por tipo"""
        try:
            query = """
                SELECT Tipo, COUNT(*) as Cantidad, SUM(Cantidad) as Total
                FROM Movimientos 
                WHERE Fecha >= DATEADD(day, -30, GETDATE())
                GROUP BY Tipo
                ORDER BY Cantidad DESC
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "movimientos")
            
            tipos = [d[0] for d in datos]
            cantidades = [d[1] for d in datos]
            totales = [d[2] for d in datos]
            
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Gráfica de barras doble
            x = range(len(tipos))
            width = 0.35
            
            bars1 = ax.bar([i - width/2 for i in x], cantidades, width, label='N° Movimientos', alpha=0.8, color='#00ff88')
            bars2 = ax.bar([i + width/2 for i in x], totales, width, label='Total Unidades', alpha=0.8, color='#0088ff')
            
            ax.set_xlabel('Tipo de Movimiento')
            ax.set_ylabel('Cantidad')
            ax.set_title('📈 Movimientos de Inventario (Últimos 30 días)', fontsize=14, fontweight='bold', pad=20)
            ax.set_xticks(x)
            ax.set_xticklabels(tipos, rotation=45)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Agregar valores
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=8)
            
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
            
        except Exception as e:
            print(f"Error creando gráfica movimientos: {e}")
            return self.crear_mensaje_error(frame_parent)
    
    def crear_grafica_citas(self, frame_parent):
        """Crear gráfica de citas por estado y especialidad"""
        try:
            query = """
                SELECT 
                    e.Nombre as Especialidad,
                    c.Estado,
                    COUNT(*) as Cantidad
                FROM Citas c
                JOIN Doctores d ON c.IdDoctor = d.IdDoctor
                LEFT JOIN Especialidades e ON d.EspecialidadId = e.IdEspecialidad
                WHERE c.FechaCita >= DATEADD(day, -30, GETDATE())
                GROUP BY e.Nombre, c.Estado
                ORDER BY Especialidad, Estado
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "citas")
            
            # Procesar datos para gráfica apilada
            df_data = []
            for esp, estado, cant in datos:
                df_data.append({'Especialidad': esp or 'Sin Especialidad', 'Estado': estado, 'Cantidad': cant})
            
            df = pd.DataFrame(df_data)
            pivot_df = df.pivot_table(index='Especialidad', columns='Estado', values='Cantidad', fill_value=0)
            
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Gráfica de barras apiladas
            colores_estado = {'Pendiente': '#ffaa00', 'Confirmada': '#00ff88', 'Cancelada': '#ff4444', 'Completada': '#0088ff'}
            colores = [colores_estado.get(col, '#666666') for col in pivot_df.columns]
            
            pivot_df.plot(kind='bar', stacked=True, ax=ax, color=colores, alpha=0.8)
            
            ax.set_title('📅 Citas por Especialidad y Estado (Últimos 30 días)', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Número de Citas')
            ax.set_xlabel('Especialidad')
            ax.legend(title='Estado', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
            
        except Exception as e:
            print(f"Error creando gráfica citas: {e}")
            return self.crear_mensaje_error(frame_parent)
    
    def crear_grafica_tendencia_mensual(self, frame_parent):
        """Crear gráfica de tendencia mensual de movimientos"""
        try:
            query = """
                SELECT 
                    FORMAT(Fecha, 'yyyy-MM') as Mes,
                    Tipo,
                    COUNT(*) as Cantidad
                FROM Movimientos 
                WHERE Fecha >= DATEADD(month, -6, GETDATE())
                GROUP BY FORMAT(Fecha, 'yyyy-MM'), Tipo
                ORDER BY Mes, Tipo
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "tendencias")
            
            # Procesar datos
            df_data = []
            for mes, tipo, cant in datos:
                df_data.append({'Mes': mes, 'Tipo': tipo, 'Cantidad': cant})
            
            df = pd.DataFrame(df_data)
            pivot_df = df.pivot_table(index='Mes', columns='Tipo', values='Cantidad', fill_value=0)
            
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Gráfica de líneas
            pivot_df.plot(kind='line', marker='o', ax=ax, linewidth=2.5, markersize=8)
            
            ax.set_title('📈 Tendencia Mensual de Movimientos (Últimos 6 meses)', fontsize=14, fontweight='bold', pad=20)
            ax.set_ylabel('Número de Movimientos')
            ax.set_xlabel('Mes')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3)
            
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
            
        except Exception as e:
            print(f"Error creando gráfica tendencia: {e}")
            return self.crear_mensaje_error(frame_parent)
    
    def crear_grafica_top_productos(self, frame_parent):
        """Crear gráfica de top 10 productos más movidos"""
        try:
            query = """
                SELECT TOP 10 
                    Producto,
                    COUNT(*) as Movimientos,
                    SUM(CASE WHEN Tipo = 'ENTRADA' THEN Cantidad ELSE -Cantidad END) as Neto
                FROM Movimientos 
                WHERE Fecha >= DATEADD(day, -30, GETDATE())
                GROUP BY Producto
                ORDER BY Movimientos DESC
            """
            datos = run_query(query)
            
            if not datos:
                return self.crear_mensaje_sin_datos(frame_parent, "productos populares")
            
            productos = [d[0] for d in datos]
            movimientos = [d[1] for d in datos]
            netos = [d[2] for d in datos]
            
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            # Gráfica de barras horizontales
            y_pos = range(len(productos))
            bars = ax.barh(y_pos, movimientos, alpha=0.8, color='#00ff88')
            
            ax.set_yticks(y_pos)
            ax.set_yticklabels(productos)
            ax.set_xlabel('Número de Movimientos')
            ax.set_title('🏆 Top 10 Productos Más Movidos (Últimos 30 días)', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            
            # Agregar valores netos
            for i, (bar, neto) in enumerate(zip(bars, netos)):
                width = bar.get_width()
                color = '#ff4444' if neto < 0 else '#44ff44'
                ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                       f'Neto: {neto:+d}', va='center', color=color, fontweight='bold')
            
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, frame_parent)
            canvas.draw()
            return canvas.get_tk_widget()
            
        except Exception as e:
            print(f"Error creando gráfica top productos: {e}")
            return self.crear_mensaje_error(frame_parent)
        
    def crear_mensaje_sin_datos(self, parent, tipo):
        """Crear mensaje cuando no hay datos"""
        frame = tk.Frame(parent, bg='#2C3E50')
        lbl = tk.Label(frame, text=f"📊 No hay datos suficientes para {tipo}", 
                      font=('Arial', 12), bg='#2C3E50', fg='#BDC3C7')
        lbl.pack(expand=True, pady=50)
        return frame
    
    def crear_mensaje_error(self, parent):
        """Crear mensaje de error"""
        frame = tk.Frame(parent, bg='#2C3E50')
        lbl = tk.Label(frame, text="❌ Error al generar el reporte", 
                      font=('Arial', 12), bg='#2C3E50', fg='#E74C3C')
        lbl.pack(expand=True, pady=50)
        return frame

# ---------------------------
# PESTAÑA DE REPORTES GRÁFICOS
# ---------------------------
def crear_pestana_reportes():
    """Crear la pestaña de reportes gráficos - VERSIÓN CORREGIDA"""
    global notebook, modulo_reportes, frame_grafica_actual
    
    try:
        print("🔧 DEBUG: Intentando crear pestaña de reportes...")
        
        # Verificar que el notebook existe
        if notebook is None:
            print("❌ ERROR: Notebook no está definido")
            return None
            
        # Verificar permisos - IMPORTANTE
        if not verificar_permiso('reportes', 'visualizar'):
            print("❌ PERMISO DENEGADO: Usuario sin permisos para reportes")
            print(f"   Rol actual: {ROL_ACTUAL}")
            print(f"   Módulos permitidos: {SISTEMA_PERMISOS.obtener_modulos_visibles(ROL_ACTUAL)}")
            return None
            
        print("✅ DEBUG: Permisos OK, creando pestaña...")
        
        # Crear frame de reportes
        frame_reportes = ttk.Frame(notebook)
        notebook.add(frame_reportes, text="📈 Reportes")
        
        print("✅ DEBUG: Frame de reportes creado exitosamente")
        
        # Inicializar módulo de reportes
        modulo_reportes = ModuloReportes()
        
        # Frame de controles
        frame_controles_reportes = ttk.Frame(frame_reportes)
        frame_controles_reportes.pack(fill="x", padx=10, pady=10)
        
        # Botones de reportes
        reportes_disponibles = [
            ("📊 Stock", "stock"),
            ("📅 Vencimientos", "vencimientos"), 
            ("📈 Movimientos", "movimientos"),
            ("👥 Citas", "citas"),
            ("📈 Tendencia", "tendencia"),
            ("🏆 Top Productos", "top_productos")
        ]
        
        for i, (texto, tipo) in enumerate(reportes_disponibles):
            btn = ttk.Button(frame_controles_reportes, text=texto,
                            command=lambda t=tipo: mostrar_reporte(t))
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # Frame para gráficas
        frame_grafica_actual = ttk.Frame(frame_reportes)
        frame_grafica_actual.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mostrar reporte inicial
        frame_reportes.after(500, lambda: mostrar_reporte("stock"))
        
        print("✅ DEBUG: Pestaña de reportes COMPLETADA")
        return frame_reportes
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return None
    
def mostrar_reporte(tipo_reporte):
    """Mostrar el reporte seleccionado - VERSIÓN CORREGIDA"""
    global frame_grafica_actual, modulo_reportes
    
    try:
        # Limpiar frame actual
        for widget in frame_grafica_actual.winfo_children():
            widget.destroy()
        
        # Mostrar loading
        lbl_loading = tk.Label(frame_grafica_actual, text="🔄 Generando reporte...", 
                              font=('Arial', 14), bg='#E3F2FD')
        lbl_loading.pack(expand=True)
        frame_grafica_actual.update()
        
        # Generar gráfica según tipo
        widget_grafica = None
        if tipo_reporte == "stock":
            widget_grafica = modulo_reportes.crear_grafica_stock(frame_grafica_actual)
        elif tipo_reporte == "vencimientos":
            widget_grafica = modulo_reportes.crear_grafica_vencimientos(frame_grafica_actual)
        elif tipo_reporte == "movimientos":
            widget_grafica = modulo_reportes.crear_grafica_movimientos(frame_grafica_actual)
        elif tipo_reporte == "citas":
            widget_grafica = modulo_reportes.crear_grafica_citas(frame_grafica_actual)
        elif tipo_reporte == "tendencia":
            widget_grafica = modulo_reportes.crear_grafica_tendencia_mensual(frame_grafica_actual)
        elif tipo_reporte == "top_productos":
            widget_grafica = modulo_reportes.crear_grafica_top_productos(frame_grafica_actual)
        
        # Remover loading y mostrar gráfica
        lbl_loading.destroy()
        if widget_grafica:
            widget_grafica.pack(fill="both", expand=True)
        else:
            # Mostrar mensaje de error
            lbl_error = tk.Label(frame_grafica_actual, text="❌ No se pudo generar el reporte", 
                               font=('Arial', 12), bg='#E3F2FD', fg='red')
            lbl_error.pack(expand=True)
            
    except Exception as e:
        print(f"❌ Error mostrando reporte {tipo_reporte}: {e}")
        # Limpiar y mostrar error
        for widget in frame_grafica_actual.winfo_children():
            widget.destroy()
        
        lbl_error = tk.Label(frame_grafica_actual, 
                           text=f"❌ Error generando reporte:\n{str(e)}", 
                           font=('Arial', 10), bg='#E3F2FD', fg='red', justify='left')
        lbl_error.pack(expand=True)
# ---------------------------
# INTEGRACIÓN CON EL SISTEMA EXISTENTE
# ---------------------------

# Variables globales
modulo_reportes = None
frame_grafica_actual = None   
# ---------------------------
# FUNCIÓN DE INICIALIZACIÓN ACTUALIZADA
# ---------------------------
def inicializar_aplicacion():
    """Cargar datos iniciales al abrir la aplicación"""
    cargar_inventario()
    cargar_usuarios()
    cargar_movimientos()
    cargar_alertas()
    crear_barra_estado()

    # Configurar interfaz según rol
    configurar_interfaz_por_rol()
    configurar_botones_por_permisos()

# INICIALIZACIÓN DEL MÓDULO DE CITAS
    try:
        crear_tablas_citas()
        insertar_datos_ejemplo_citas()
    
        
        if not hasattr(root, "btn_asistente_creado"):
            btn_asistente = tk.Button(root, text="💬 Asistente", command=abrir_asistente, 
                                    bg="#0A64A4", fg="white", relief="flat", font=("Arial", 10, "bold"),
                                    cursor="hand2")
            btn_asistente.place(relx=0.93, rely=0.92, anchor="center")
            root.btn_asistente_creado = True
            
    except Exception as e:
        print(f"Error inicializando módulo de citas: {e}")
    
    # INICIALIZAR MÓDULO DE REPORTES (NUEVO)
    try:
        crear_pestana_reportes()
        print("✅ Módulo de reportes gráficos inicializado")
    except Exception as e:
        print(f"❌ Error inicializando módulo de reportes: {e}")
    try:
        print("🔄 Intentando crear pestaña de reportes...")
        crear_pestana_reportes()
        print("✅ Pestaña de reportes creada")
    except Exception as e:
        print(f"❌ Error creando reportes: {e}")
        # Mostrar mensaje de error específico
        import traceback
        traceback.print_exc()


def initialize_theme_system(root_window):
    
    try:
        global theme_manager
        # Crear theme_manager con la ventana root
        theme_manager = ThemeManager(root_window)
        
        # Inicializar el sistema de temas
        success = theme_manager.initialize()
        
        if success:
            print("✅ Sistema de temas inicializado correctamente")
            return True
        else:
            print("⚠️ Sistema de temas inicializado con advertencias")
            return True  # Continuar aunque haya advertencias
            
    except Exception as e:
        print(f"❌ Error crítico inicializando temas: {e}")
        return False
# CONFIGURACIÓN DE INICIO (ACTUALIZADA)
# ---------------------------
root = tk.Tk()
root.title("Clínica Popular San Rafael - Sistema de Gestión")
root.geometry("1000x650")
# === INICIALIZAR SISTEMA DE TEMAS PRIMERO ===
theme_initialized = initialize_theme_system(root)

if not theme_initialized:
    print("⚠️ Continuando sin sistema de temas completo")

root.withdraw()
root.configure(bg="#E3F2FD")
root.withdraw()

# ---------------------------
# CONFIGURACIÓN DE ESTILOS
# ---------------------------
style = ttk.Style()
style.theme_use("clam")
# Fondo general
root.configure(bg="#E3F2FD")
# Estilos generales
style.configure("TFrame", background="#E3F2FD")
style.configure("TLabel", background="#E3F2FD", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8,
                relief="flat", background="#0A64A4", foreground="white")
style.map("TButton", background=[("active", "#1565C0")])
# Treeview moderno
style.configure("Treeview", background="white", foreground="black",
                rowheight=28, fieldbackground="white", font=("Segoe UI", 9))
style.map("Treeview", background=[("selected", "#90CAF9")])
# Notebook tabs
style.configure("TNotebook", background="#E3F2FD", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"),
                padding=[14, 6], background="#BBDEFB", foreground="black")
style.map("TNotebook.Tab",
          background=[("selected", "#0A64A4")],
          foreground=[("selected", "white")])
# Barra de progreso personalizada
style.configure("ECG.Horizontal.TProgressbar",
               troughcolor='black',
               background='#00FF66',
               bordercolor='#00CC55',
               lightcolor='#00FF66',
               darkcolor='#00CC55')
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------------------
# ANIMACIONES DE CARGA DINÁMICAS VARIADAS UWU
# ---------------------------
class AnimacionesModernas:
    def __init__(self):
        self.animaciones = [
            self.animacion_neuromedica,
            self.animacion_particulas_medicas,
            self.animacion_holograma,
            self.animacion_circuitos,
            self.animacion_dna
        ]
        self.current_animation = None
    
    def mostrar_animacion_aleatoria(self):
        """Selecciona y muestra una animación aleatoria moderna"""
        if self.current_animation and self.current_animation.winfo_exists():
            self.current_animation.destroy()
        
        animacion = random.choice(self.animaciones)
        animacion()

    # ---------------------------
    # 1. ANIMACIÓN NEUROMÉDICA MEJORADA
    # ---------------------------
    def animacion_neuromedica(self):
        splash = self.crear_splash_window(600, 400, '#000814')
        canvas = tk.Canvas(splash, bg='#000814', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Títulos optimizados
        self.crear_texto_centrado(canvas, 300, 80, "CLÍNICA SAN RAFAEL", 
                                 ("Segoe UI", 24, "bold"), "#00F5FF")
        self.crear_texto_centrado(canvas, 300, 115, "Sistema Neuro-Médico v4.0", 
                                 ("Segoe UI", 10), "#8EACCD")
        
        # Red neuronal optimizada
        nodos = self.crear_red_neuronal(8, 300, 200, 150)
        conexiones = self.crear_conexiones_neuronales(nodos, 0.4)
        
        def animar_red(frame=0):
            canvas.delete("neurona")
            
            # Conexiones con mejor rendimiento
            for (x1, y1), (x2, y2) in conexiones:
                alpha = abs(math.sin(frame * 0.1)) * 0.7 + 0.3
                color = self.interpolar_color("#00F5FF", "#FF006E", alpha)
                canvas.create_line(x1, y1, x2, y2, fill=color, width=2, tags="neurona")
            
            # Nodos optimizados
            for x, y in nodos:
                tamaño = 6 + math.sin(frame * 0.2 + x) * 2
                self.crear_nodo_neuronal(canvas, x, y, tamaño, frame)
            
            # Texto de carga
            self.actualizar_texto_carga(canvas, frame, 300, 350)
            
            if frame < 60:
                splash.after(50, lambda: animar_red(frame + 1))
            else:
                self.finalizar_animacion(splash)
        
        animar_red()

    def crear_red_neuronal(self, num_nodos, centro_x, centro_y, radio):
        """Crea una red neuronal de forma más eficiente"""
        return [
            (centro_x + radio * math.cos((i / num_nodos) * 2 * math.pi),
             centro_y + radio * math.sin((i / num_nodos) * 2 * math.pi))
            for i in range(num_nodos)
        ]

    def crear_conexiones_neuronales(self, nodos, probabilidad):
        """Crea conexiones entre nodos de forma optimizada"""
        conexiones = []
        for i in range(len(nodos)):
            for j in range(i + 1, len(nodos)):
                if random.random() < probabilidad:
                    conexiones.append((nodos[i], nodos[j]))
        return conexiones

    def crear_nodo_neuronal(self, canvas, x, y, tamaño, frame):
        """Crea un nodo neuronal con efectos visuales"""
        canvas.create_oval(x-tamaño, y-tamaño, x+tamaño, y+tamaño, 
                         fill="#00F5FF", outline="", tags="neurona")
        
        # Efecto de aura optimizado
        for i in range(2):  # Reducido de 3 a 2 para mejor rendimiento
            radio = tamaño + (i + 1) * 3
            alpha = 0.4 - i * 0.2
            canvas.create_oval(x-radio, y-radio, x+radio, y+radio,
                             outline=self.interpolar_color("#00F5FF", "#000814", alpha),
                             width=1, tags="neurona")

    # ---------------------------
    # 2. ANIMACIÓN DE PARTÍCULAS MEJORADA
    # ---------------------------
    def animacion_particulas_medicas(self):
        splash = self.crear_splash_window(600, 400, '#0A0E29')
        canvas = tk.Canvas(splash, bg='#0A0E29', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Títulos
        self.crear_texto_centrado(canvas, 300, 60, "🏥 CLÍNICA SAN RAFAEL", 
                                 ("Segoe UI", 20, "bold"), "#FFFFFF")
        self.crear_texto_centrado(canvas, 300, 90, "Sistema de Gestión Médica Inteligente", 
                                 ("Segoe UI", 10), "#A0AEC0")
        
        # Símbolo médico central
        centro_x, centro_y = 300, 200
        self.crear_simbolo_medico(canvas, centro_x, centro_y)
        
        # Partículas optimizadas
        particulas = self.crear_particulas(40, centro_x, centro_y)  # Reducido de 50 a 40
        
        def animar_particulas(frame=0):
            canvas.delete("particula")
            
            for p in particulas:
                self.actualizar_particula(canvas, p, frame, centro_x, centro_y)
            
            # Barra de progreso mejorada
            self.actualizar_barra_progreso(canvas, frame, 60, 150, 320, 450, 340)
            
            if frame < 60:
                splash.after(50, lambda: animar_particulas(frame + 1))
            else:
                self.finalizar_animacion(splash)
        
        animar_particulas()

    def crear_particulas(self, cantidad, centro_x, centro_y):
        """Crea partículas de forma más eficiente"""
        colores = ["#4FD1C7", "#4299E1", "#9F7AEA", "#F56565"]
        return [
            {
                'angle': random.uniform(0, 2 * math.pi),
                'distance': random.uniform(80, 180),  # Reducido rango
                'speed': random.uniform(0.5, 1.5),    # Velocidad más consistente
                'size': random.uniform(2, 4),         # Tamaño más uniforme
                'color': random.choice(colores),
                'phase': random.uniform(0, 2 * math.pi)
            }
            for _ in range(cantidad)
        ]

    def actualizar_particula(self, canvas, particula, frame, centro_x, centro_y):
        """Actualiza y dibuja una partícula individual"""
        current_distance = particula['distance'] + math.sin(frame * 0.1 + particula['phase']) * 15
        x = centro_x + current_distance * math.cos(particula['angle'] + frame * 0.02 * particula['speed'])
        y = centro_y + current_distance * math.sin(particula['angle'] + frame * 0.02 * particula['speed'])
        
        # Partícula principal
        canvas.create_oval(x-particula['size'], y-particula['size'], 
                          x+particula['size'], y+particula['size'],
                          fill=particula['color'], outline="", tags="particula")
        
        # Estela simplificada (mejor rendimiento)
        for i in range(1, 3):  # Reducido de 4 a 3
            trail_factor = i * 4
            trail_x = centro_x + (current_distance - trail_factor) * math.cos(
                particula['angle'] + (frame - i) * 0.02 * particula['speed'])
            trail_y = centro_y + (current_distance - trail_factor) * math.sin(
                particula['angle'] + (frame - i) * 0.02 * particula['speed'])
            
            canvas.create_oval(trail_x-1, trail_y-1, trail_x+1, trail_y+1,
                             fill=particula['color'], outline="", tags="particula")

    def crear_simbolo_medico(self, canvas, centro_x, centro_y):
        """Crea el símbolo médico central"""
        canvas.create_oval(centro_x-60, centro_y-60, centro_x+60, centro_y+60,
                          outline="#4FD1C7", width=3, tags="simbolo")
        canvas.create_rectangle(centro_x-15, centro_y-40, centro_x+15, centro_y+40,
                               fill="#4FD1C7", outline="", tags="simbolo")
        canvas.create_rectangle(centro_x-40, centro_y-15, centro_x+40, centro_y+15,
                               fill="#4FD1C7", outline="", tags="simbolo")

    # ---------------------------
    # 3. ANIMACIÓN HOLOGRAMA MEJORADA
    # ---------------------------
    def animacion_holograma(self):
        splash = self.crear_splash_window(700, 500, '#000000')
        canvas = tk.Canvas(splash, bg='#000000', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Títulos
        self.crear_texto_centrado(canvas, 350, 50, "CLÍNICA SAN RAFAEL", 
                                 ("Segoe UI", 28, "bold"), "#00FF88")
        self.crear_texto_centrado(canvas, 350, 85, "TECNOLOGÍA HOLO-MÉDICA", 
                                 ("Segoe UI", 12), "#88FFDD")
        
        # Base del holograma
        base_y = 400
        self.crear_base_holograma(canvas, base_y)
        
        # Puntos del holograma
        puntos_holograma = self.crear_puntos_holograma(12, 350, 250, 120, 80)
        
        def animar_holograma(frame=0):
            canvas.delete("holograma")
            
            # Proyección holográfica optimizada
            self.dibujar_proyeccion_holograma(canvas, puntos_holograma, frame)
            
            # Líneas de escaneo
            self.dibujar_lineas_escaneo(canvas, frame, base_y)
            
            # Diagnósticos
            self.mostrar_diagnosticos(canvas, frame)
            
            if frame < 80:
                splash.after(40, lambda: animar_holograma(frame + 1))
            else:
                self.crear_texto_centrado(canvas, 350, 450, "✅ SISTEMA LISTO", 
                                         ("Segoe UI", 14, "bold"), "#00FF88", "holograma")
                splash.after(800, lambda: self.finalizar_animacion(splash))
        
        animar_holograma()

    def crear_base_holograma(self, canvas, base_y):
        """Crea la base del holograma"""
        canvas.create_rectangle(250, base_y, 450, base_y + 20, 
                              fill="#333333", outline="")
        canvas.create_oval(240, base_y + 10, 260, base_y + 30, fill="#00FF88", outline="")
        canvas.create_oval(440, base_y + 10, 460, base_y + 30, fill="#00FF88", outline="")

    def crear_puntos_holograma(self, num_puntos, centro_x, centro_y, radio_x, radio_y):
        """Crea los puntos para la proyección del holograma"""
        return [
            (centro_x + radio_x * math.cos((i / num_puntos) * 2 * math.pi),
             centro_y + radio_y * math.sin((i / num_puntos) * 2 * math.pi))
            for i in range(num_puntos)
        ]

    def dibujar_proyeccion_holograma(self, canvas, puntos, frame):
        """Dibuja la proyección holográfica"""
        for i in range(len(puntos)):
            x1, y1 = puntos[i]
            x2, y2 = puntos[(i + 1) % len(puntos)]
            
            # Efecto de escaneo
            scan_pos = (frame * 2) % (len(puntos) * 2)
            alpha = 1.0 if abs(i * 2 - scan_pos) < 2 else 0.3
            
            canvas.create_line(x1, y1, x2, y2, 
                             fill=self.interpolar_color("#00FF88", "#000000", 1-alpha),
                             width=2, tags="holograma")
            
            # Puntos de conexión
            canvas.create_oval(x1-3, y1-3, x1+3, y1+3, 
                             fill="#00FF88", outline="", tags="holograma")

    def dibujar_lineas_escaneo(self, canvas, frame, base_y):
        """Dibuja las líneas de escaneo vertical"""
        for i in range(8):
            x = 250 + i * 25
            height = 150 + math.sin(frame * 0.2 + i) * 30
            canvas.create_line(x, base_y, x, base_y - height,
                             fill=self.interpolar_color("#00FF88", "#000000", 0.7),
                             width=1, tags="holograma")

    def mostrar_diagnosticos(self, canvas, frame):
        """Muestra los textos de diagnóstico"""
        diagnoticos = [
            "✓ Sistema cardiovascular: ESTABLE",
            "✓ Base de datos: CONECTADA", 
            "✓ Módulo de inventario: ACTIVO",
            "✓ Sistema de citas: SINCRONIZADO",
            "✓ Red hospitalaria: OPTIMA"
        ]
        
        for i, texto in enumerate(diagnoticos):
            y_pos = 320 + i * 20
            if frame > i * 10:
                self.crear_texto_centrado(canvas, 350, y_pos, texto, 
                                         ("Consolas", 9), "#00FF88", "holograma")

    # ---------------------------
    # 4. ANIMACIÓN CIRCUITOS MÉDICOS (FALTANTE)
    # ---------------------------
    def animacion_circuitos(self):
        splash = self.crear_splash_window(650, 450, '#0F1419')
        canvas = tk.Canvas(splash, bg='#0F1419', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Título
        self.crear_texto_centrado(canvas, 325, 40, "⚡ SISTEMA MÉDICO DIGITAL", 
                                 ("Segoe UI", 18, "bold"), "#60A5FA")
        self.crear_texto_centrado(canvas, 325, 70, "Red Neuronal Hospitalaria v3.0", 
                                 ("Segoe UI", 10), "#9CA3AF")
        
        # Crear nodos de circuito
        nodos = self.crear_nodos_circuito(5, 8, 50, 120, 80, 60)
        conexiones = self.crear_conexiones_circuito(nodos, 0.1)
        
        def animar_circuitos(frame=0):
            canvas.delete("circuito")
            
            # Dibujar conexiones con pulsos
            for (x1, y1), (x2, y2) in conexiones:
                self.dibujar_pulso_datos(canvas, x1, y1, x2, y2, frame)
            
            # Dibujar nodos
            for x, y, id_nodo in nodos:
                self.dibujar_nodo_circuito(canvas, x, y, id_nodo, frame)
            
            # Panel de estado
            self.dibujar_panel_estado(canvas, frame)
            
            if frame < 60:
                splash.after(50, lambda: animar_circuitos(frame + 1))
            else:
                self.finalizar_animacion(splash)
        
        animar_circuitos()

    def crear_nodos_circuito(self, filas, columnas, inicio_x, inicio_y, espacio_x, espacio_y):
        """Crea los nodos del circuito"""
        nodos = []
        for row in range(filas):
            for col in range(columnas):
                x = inicio_x + col * espacio_x
                y = inicio_y + row * espacio_y
                nodos.append((x, y, f"nodo_{row}_{col}"))
        return nodos

    def crear_conexiones_circuito(self, nodos, probabilidad):
        """Crea conexiones entre nodos del circuito"""
        conexiones = []
        for i, (x1, y1, id1) in enumerate(nodos):
            for j, (x2, y2, id2) in enumerate(nodos[i+1:], i+1):
                if random.random() < probabilidad and abs(x1-x2) + abs(y1-y2) < 150:
                    conexiones.append(((x1, y1), (x2, y2)))
        return conexiones

    def dibujar_pulso_datos(self, canvas, x1, y1, x2, y2, frame):
        """Dibuja el pulso de datos entre nodos"""
        progress = (frame * 0.1) % 1
        pulse_x = x1 + (x2 - x1) * progress
        pulse_y = y1 + (y2 - y1) * progress
        
        # Línea base
        canvas.create_line(x1, y1, x2, y2, fill="#1F2937", width=1, tags="circuito")
        
        # Pulso de datos
        canvas.create_oval(pulse_x-3, pulse_y-3, pulse_x+3, pulse_y+3,
                         fill="#60A5FA", outline="", tags="circuito")

    def dibujar_nodo_circuito(self, canvas, x, y, id_nodo, frame):
        """Dibuja un nodo del circuito"""
        # Nodo base
        canvas.create_oval(x-4, y-4, x+4, y+4, fill="#374151", outline="", tags="circuito")
        
        # Actividad del nodo
        actividad = math.sin(frame * 0.2 + hash(id_nodo) * 0.1)
        if actividad > 0.5:
            canvas.create_oval(x-6, y-6, x+6, y+6, fill="#60A5FA", outline="", tags="circuito")

    def dibujar_panel_estado(self, canvas, frame):
        """Dibuja el panel de estado del sistema"""
        canvas.create_rectangle(50, 350, 600, 420, fill="#111827", outline="#374151", tags="circuito")
        
        modulos = [
            ("🏥 Módulo Principal", frame > 10),
            ("💊 Gestión de Inventario", frame > 20),
            ("📅 Sistema de Citas", frame > 30),
            ("👥 Control de Usuarios", frame > 40),
            ("⚠️ Monitor de Alertas", frame > 50)
        ]
        
        for i, (modulo, activo) in enumerate(modulos):
            x_pos = 80 + i * 110
            color = "#10B981" if activo else "#6B7280"
            icon = "✓" if activo else "⌛"
            canvas.create_text(x_pos, 370, text=f"{icon} {modulo}", 
                             font=("Segoe UI", 8), fill=color, tags="circuito")
        
        # Barra de progreso
        progreso = min(100, (frame / 60) * 100)
        canvas.create_rectangle(100, 390, 550, 400, outline="#374151", width=1, tags="circuito")
        canvas.create_rectangle(100, 390, 100 + (450 * progreso / 100), 400, 
                              fill="#60A5FA", outline="", tags="circuito")
        canvas.create_text(325, 410, text=f"Optimizando rendimiento... {progreso:.0f}%", 
                         font=("Segoe UI", 9), fill="#9CA3AF", tags="circuito")

    # ---------------------------
    # 5. ANIMACIÓN ADN MÉDICO (FALTANTE)
    # ---------------------------
    def animacion_dna(self):
        splash = self.crear_splash_window(600, 500, '#0A0F1C')
        canvas = tk.Canvas(splash, bg='#0A0F1C', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Título
        self.crear_texto_centrado(canvas, 300, 50, "🧬 CLÍNICA SAN RAFAEL", 
                                 ("Segoe UI", 22, "bold"), "#10B981")
        self.crear_texto_centrado(canvas, 300, 80, "Sistema Genómico de Gestión Médica", 
                                 ("Segoe UI", 11), "#6EE7B7")
        
        def animar_adn(frame=0):
            canvas.delete("adn")
            
            # Dibujar hélices de ADN
            self.dibujar_helice_adn(canvas, 300, 250, 100, 200, 16, frame)
            
            # Información genética
            self.mostrar_informacion_genetica(canvas, frame)
            
            # Texto de análisis
            self.mostrar_analisis_adn(canvas, frame)
            
            if frame < 60:
                splash.after(50, lambda: animar_adn(frame + 1))
            else:
                self.crear_texto_centrado(canvas, 300, 450, "✅ ANÁLISIS GENÉTICO COMPLETADO", 
                                         ("Segoe UI", 12, "bold"), "#10B981", "adn")
                splash.after(1000, lambda: self.finalizar_animacion(splash))
        
        animar_adn()

    def dibujar_helice_adn(self, canvas, centro_x, centro_y, radio, altura, segmentos, frame):
        """Dibuja la hélice de ADN animada"""
        for i in range(segmentos):
            t = i / segmentos
            y = centro_y - altura/2 + t * altura
            angle = t * 4 * math.pi + frame * 0.1
            
            # Puntos de las dos hélices
            x1 = centro_x + radio * math.cos(angle)
            x2 = centro_x + radio * math.cos(angle + math.pi)
            
            # Colores interpolados
            color1 = self.interpolar_color("#10B981", "#3B82F6", math.sin(angle)*0.5+0.5)
            color2 = self.interpolar_color("#3B82F6", "#10B981", math.sin(angle)*0.5+0.5)
            
            # Nodos de las hélices
            canvas.create_oval(x1-5, y-5, x1+5, y+5, fill=color1, outline="", tags="adn")
            canvas.create_oval(x2-5, y-5, x2+5, y+5, fill=color2, outline="", tags="adn")
            
            # Conexiones
            if i < segmentos - 1:
                next_y = centro_y - altura/2 + (i + 1) / segmentos * altura
                next_angle = (i + 1) / segmentos * 4 * math.pi + frame * 0.1
                
                next_x1 = centro_x + radio * math.cos(next_angle)
                next_x2 = centro_x + radio * math.cos(next_angle + math.pi)
                
                # Líneas de la hélice
                canvas.create_line(x1, y, next_x1, next_y, fill=color1, width=2, tags="adn")
                canvas.create_line(x2, y, next_x2, next_y, fill=color2, width=2, tags="adn")
                
                # Conexiones transversales
                if i % 2 == 0:
                    canvas.create_line(x1, y, x2, y, fill="#6EE7B7", width=1, tags="adn")

    def mostrar_informacion_genetica(self, canvas, frame):
        """Muestra información genética simulada"""
        info_y = 400
        secuencias = [
            "ACTG" * 5,
            "TCGA" * 4,
            "GATC" * 6
        ]
        
        for i, secuencia in enumerate(secuencias):
            desplazamiento = (frame * 2) % len(secuencia)
            secuencia_animada = secuencia[desplazamiento:] + secuencia[:desplazamiento]
            canvas.create_text(300, info_y + i * 20, text=secuencia_animada,
                             font=("Consolas", 10), fill="#6EE7B7", tags="adn")

    def mostrar_analisis_adn(self, canvas, frame):
        """Muestra el texto de análisis del ADN"""
        analisis = [
            "Analizando patrones genéticos...",
            "Sincronizando datos médicos...", 
            "Optimizando tratamientos...",
            f"Progreso: {(frame/60*100):.0f}%"
        ]
        
        for i, texto in enumerate(analisis):
            if frame > i * 15:
                canvas.create_text(300, 350 + i * 25, text=texto,
                                 font=("Segoe UI", 10), fill="#93C5FD", tags="adn")

    # ---------------------------
    # FUNCIONES AUXILIARES MEJORADAS
    # ---------------------------
    def crear_splash_window(self, ancho, alto, color_bg):
        """Crea una ventana splash optimizada"""
        splash = tk.Toplevel(root)
        splash.overrideredirect(True)
        splash.geometry(f"{ancho}x{alto}")
        splash.configure(bg=color_bg)
        splash.attributes('-topmost', True)
        self.centrar_ventana(splash, ancho, alto)
        self.current_animation = splash
        return splash

    def crear_texto_centrado(self, canvas, x, y, texto, font, color, tag=None):
        """Crea texto centrado de forma optimizada"""
        tags = (tag,) if tag else ()
        canvas.create_text(x, y, text=texto, font=font, fill=color, tags=tags)

    def actualizar_texto_carga(self, canvas, frame, x, y):
        """Actualiza el texto de carga animado"""
        puntos = "." * (frame % 4)
        canvas.delete("carga")
        self.crear_texto_centrado(canvas, x, y, f"Inicializando sistema{puntos}", 
                                 ("Segoe UI", 11), "#8EACCD", "carga")

    def actualizar_barra_progreso(self, canvas, frame, total_frames, x1, y1, x2, y2):
        """Actualiza la barra de progreso"""
        progreso = min(100, (frame / total_frames) * 100)
        canvas.delete("progreso")
        
        # Marco de la barra
        canvas.create_rectangle(x1, y1, x2, y2, outline="#4A5568", width=1, tags="progreso")
        
        # Barra de progreso
        ancho_barra = x2 - x1
        progreso_actual = x1 + (ancho_barra * progreso / 100)
        canvas.create_rectangle(x1, y1, progreso_actual, y2, 
                              fill="#4FD1C7", outline="", tags="progreso")
        
        # Texto de progreso
        self.crear_texto_centrado(canvas, (x1 + x2) // 2, y2 + 20, 
                                 f"{progreso:.0f}% • Inicializando módulos...", 
                                 ("Segoe UI", 10), "#A0AEC0", "progreso")

    def interpolar_color(self, color1, color2, factor):
        """Interpola entre dos colores hex de forma más eficiente"""
        factor = max(0, min(1, factor))
        
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def centrar_ventana(self, ventana, ancho, alto):
        """Centra la ventana en la pantalla"""
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def finalizar_animacion(self, splash):
        """Finaliza la animación y abre la ventana principal"""
        splash.destroy()
        if hasattr(self, 'mostrar_ventana_principal'):
            self.mostrar_ventana_principal()
        elif 'mostrar_ventana_principal' in globals():
            mostrar_ventana_principal()
# Crear instancia global de animaciones
animaciones_modernas = AnimacionesModernas()


# ---------------------------
# VENTANA PRINCIPAL
# ---------------------------
def mostrar_ventana_principal():
    root.deiconify()
    # Efecto de fade in
    alpha = 0.0
    while alpha < 1.0:
        root.attributes('-alpha', alpha)
        root.update()
        alpha += 0.05
        time.sleep(0.01)
    root.attributes('-alpha', 1.0)
    inicializar_aplicacion()
# ---------------------------
# CONEXIÓN A BASE DE DATOS xd
# ---------------------------
def run_query(query, params=()):
    conn = None
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=DESKTOP-9U57LTA;"
            "DATABASE=ClinicaDB;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo ejecutar la consulta:\n{str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def run_non_query(query, params=()):
    conn = None
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=DESKTOP-9U57LTA;"
            "DATABASE=ClinicaDB;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        cursor = conn.cursor()
        print(f"Ejecutando: {query}")  # Debug
        print(f"Parámetros: {params}")  # Debug
        cursor.execute(query, params)
        conn.commit()
        return True
    except pyodbc.Error as e:
        error_msg = f"No se pudo ejecutar la operación:\n{str(e)}"
        print(f"Error SQL: {e}")  # Debug detallado
        messagebox.showerror("Error de Base de Datos", error_msg)
        return False
    finally:
        if conn:
            conn.close()

# ---------------------------
# CONEXIÓN PHPMyAdmin (MySQL) PARA CORREOS
# ---------------------------
def conectar_phpmyadmin():
    """Conectar a la base de datos MySQL (phpMyAdmin)"""
    try:
        conn = pyodbc.connect(
            "DRIVER={mysql-connector-odbc-9.5.0-winx64};"  # o el driver que tengas instalado
            "SERVER=localhost;"
            "DATABASE=correos_clinica;"  # Nueva base de datos para correos
            "USER=root;"                 # Tu usuario MySQL
            "PASSWORD="";"      # Tu contraseña MySQL
            "PORT=3306;"
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a phpMyAdmin: {e}")
        return None

def run_query_phpmyadmin(query, params=()):
    """Ejecutar consultas en phpMyAdmin"""
    conn = None
    try:
        conn = conectar_phpmyadmin()
        if conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        return []
    except Exception as e:
        print(f"Error en consulta phpMyAdmin: {e}")
        return []
    finally:
        if conn:
            conn.close()

def run_non_query_phpmyadmin(query, params=()):
    """Ejecutar operaciones sin retorno en phpMyAdmin"""
    conn = None
    try:
        conn = conectar_phpmyadmin()
        if conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        return False
    except Exception as e:
        print(f"Error en operación phpMyAdmin: {e}")
        return False
    finally:
        if conn:
            conn.close()
# ---------------------------
# SISTEMA DE CORREOS ELECTRÓNICOS
# ---------------------------

def abrir_formulario_correos():
    """Abrir formulario HTML para enviar correos"""
    if not verificar_permiso('citas', 'crear'):
        mostrar_error_permiso()
        return
    
    try:
        # Ruta a tu archivo HTML
        ruta_html = "example.html"  
        
        if os.path.exists(ruta_html):
            # Abrir en navegador
            webbrowser.open(f'file://{os.path.abspath(ruta_html)}')
            
            messagebox.showinfo(
                "Correos", 
                "📧 Formulario de correos abierto en tu navegador.\n\nComplete los datos para enviar el correo."
            )
            
        else:
            messagebox.showerror("Error", 
                f"No se encontró: {ruta_html}\n"
                f"Busca en: {os.path.abspath('.')}"
            )
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir:\n{str(e)}")

def enviar_correo_paciente(nombre, correo_destinatario, mensaje, asunto=""):
    """Enviar correo REAL y guardar en BD"""
    try:
        # 1. CONFIGURACIÓN (USA TUS CREDENCIALES REALES)
        remitente = "lopezurbina2018@gmail.com"
        password = "uynt mkho qwbf xtyp"  # ⚠️ CAMBIA ESTO

        # 2. CREAR MENSAJE
        msg = MIMEMultipart()
        msg["Subject"] = asunto or "Clínica San Rafael"
        msg["From"] = remitente
        msg["To"] = correo_destinatario

        cuerpo_html = f"""
        <html>
        <body>
            <h2>Clínica San Rafael</h2>
            <p>Estimado/a {nombre},</p>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px;">
                {mensaje.replace(chr(10), '<br>')}
            </div>
            <p>Saludos cordiales,<br>Equipo Médico</p>
        </body>
        </html>
        """

        msg.attach(MIMEText(cuerpo_html, "html"))

        # 3. ENVIAR CORREO REAL
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.send_message(msg)

        print(f"✅ CORREO REAL ENVIADO: {nombre} -> {correo_destinatario}")

        # 4. GUARDAR EN BD
        guardar_correo_simple(nombre, correo_destinatario, mensaje, asunto)

        return True

    except Exception as e:
        print(f"❌ ERROR ENVÍO REAL: {e}")
        guardar_respaldo_archivo(nombre, correo_destinatario, mensaje, asunto)
        return False
def guardar_respaldo_archivo(paciente, email, mensaje, asunto):
    """Respaldo en archivo si falla BD"""
    try:
        with open('correos_respaldo.txt', 'a', encoding='utf-8') as f:
            f.write(f"{datetime.datetime.now()} | {paciente} | {email} | {asunto}\\n")
        print("✅ Guardado en archivo de respaldo")
        return True
    except Exception as e:
        print(f"❌ Error incluso en respaldo: {e}")
        return False
def guardar_correo_db(paciente, email, mensaje):
    """
    Guardar correo en base de datos phpMyAdmin
    """
    try:
        # Conexión a phpMyAdmin (MySQL)
        conn = pyodbc.connect(
            "DRIVER={mysql-connector-odbc-9.5.0-winx64};"
            "SERVER=localhost;"
            "DATABASE=correos_clinica;"
            "USER=root;"
            "PASSWORD="";"
            "PORT=3306;"
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CorreosEnviados 
            (Paciente, EmailDestinatario, Asunto, Mensaje, UsuarioEnvio, Estado)
            VALUES (?, ?, ?, ?, ?, 'Enviado')
        """, (paciente, email, "Información sobre cita médica", mensaje, USUARIO_ACTUAL))
        
        conn.commit()
        conn.close()
        print("✅ Correo guardado en base de datos")
        return True
        
    except Exception as e:
        print(f"❌ Error guardando en BD: {e}")
        return False
def guardar_correo_simple(paciente, email, mensaje, asunto=""):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='',  # vacío si no tienes contraseña
            database='correos_clinica'
        )
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CorreosEnviados (Paciente, Email, Mensaje, Asunto) VALUES (%s, %s, %s, %s)",
            (paciente, email, mensaje, asunto)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error BD: {e}")
        return False

# ---------------------------
# FUNCIONES AUXILIARES
# ---------------------------
def formatear_fecha(fecha):
    """Función auxiliar para formatear fechas consistentemente"""
    if not fecha:
        return "N/A"
    try:
        if isinstance(fecha, (datetime.date, datetime.datetime)):
            return fecha.strftime("%d/%m/%Y")
        elif isinstance(fecha, str):
            return datetime.datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
        else:
            return str(fecha)
    except (ValueError, AttributeError):
        return "Fecha inválida"
    


# ============================================================
# 1. INVENTARIO GENERAL - FUNCIONALIDAD COMPLETA
# ============================================================
frame_inv = ttk.Frame(notebook)
notebook.add(frame_inv, text="📦 Inventario")
frame_controles_inv = ttk.Frame(frame_inv)
frame_controles_inv.pack(fill="x", padx=5, pady=5)
frame_form_inv = ttk.Frame(frame_inv)
frame_form_inv.pack(fill="x", padx=5, pady=5)
tree_inv = ttk.Treeview(frame_inv, columns=("ID", "Nombre", "Stock", "Vencimiento"), show="headings")
for col in ("ID", "Nombre", "Stock", "Vencimiento"):
    tree_inv.heading(col, text=col)
    tree_inv.column(col, width=200)
tree_inv.pack(fill="both", expand=True, padx=5, pady=5)
# Formulario para agregar/editar productos
ttk.Label(frame_form_inv, text="Nombre:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_nombre = ttk.Entry(frame_form_inv, width=20)
entry_nombre.grid(row=0, column=1, padx=5, pady=2)
ttk.Label(frame_form_inv, text="Stock:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
entry_stock = ttk.Entry(frame_form_inv, width=10)
entry_stock.grid(row=0, column=3, padx=5, pady=2)
ttk.Label(frame_form_inv, text="Vencimiento:").grid(row=0, column=4, padx=5, pady=2, sticky="w")
fecha_vencimiento = DateEntry(frame_form_inv, date_pattern='yyyy-mm-dd')
fecha_vencimiento.grid(row=0, column=5, padx=5, pady=2)

def cargar_inventario():
    try:
        tree_inv.delete(*tree_inv.get_children())
        rows = run_query("SELECT Id, Nombre, Stock, FechaVencimiento FROM Productos ORDER BY Nombre")
        for r in rows:
            fecha_formateada = formatear_fecha(r[3])
            # CORREGIDO: Asegurar que el ID sea número
            tree_inv.insert("", "end", values=(int(r[0]), r[1], r[2], fecha_formateada))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el inventario:\n{str(e)}")

def buscar_producto():
    try:
        tree_inv.delete(*tree_inv.get_children())
        nombre = entry_buscar.get().strip()
        if not nombre:
            cargar_inventario()
            return

        rows = run_query("SELECT Id, Nombre, Stock, FechaVencimiento FROM Productos WHERE Nombre LIKE ? ORDER BY Nombre",
                        ('%' + nombre + '%',))
        for r in rows:
            fecha_formateada = formatear_fecha(r[3])
            tree_inv.insert("", "end", values=(r[0], r[1], r[2], fecha_formateada))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar la búsqueda:\n{str(e)}")

def limpiar_formulario_inv():
    entry_nombre.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    fecha_vencimiento.set_date(datetime.date.today())

def cancelar_edicion():
    limpiar_formulario_inv()
    btn_agregar.config(state="normal")
    if hasattr(editar_producto_seguro, 'btn_actualizar'):
        editar_producto_seguro.btn_actualizar.destroy()
        editar_producto_seguro.btn_cancelar.destroy()
        del editar_producto_seguro.btn_actualizar
        del editar_producto_seguro.btn_cancelar

# Controles de inventario
ttk.Label(frame_controles_inv, text="Buscar producto:").grid(row=0, column=0, padx=5, pady=5)
entry_buscar = ttk.Entry(frame_controles_inv, width=30)
entry_buscar.grid(row=0, column=1, padx=5, pady=5)
entry_buscar.bind('<Return>', lambda e: buscar_producto())
ttk.Button(frame_controles_inv, text="🔍 Buscar", command=buscar_producto).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame_controles_inv, text="🔄 Actualizar", command=cargar_inventario).grid(row=0, column=3, padx=5, pady=5)
btn_agregar = ttk.Button(frame_form_inv, text="➕ Agregar", command=agregar_producto_seguro)
btn_agregar.grid(row=0, column=6, padx=5, pady=2)
ttk.Button(frame_form_inv, text="✏️ Editar", command=editar_producto_seguro).grid(row=0, column=9, padx=5, pady=2)
ttk.Button(frame_form_inv, text="🗑️ Eliminar", command=eliminar_producto_seguro).grid(row=0, column=10, padx=5, pady=2)

# ============================================================
# 2. ALERTAS - DETECCIÓN AUTOMÁTICA Y ACCIONES
# ============================================================
frame_alert = ttk.Frame(notebook)
notebook.add(frame_alert, text="⚠️ Alertas")
frame_controles_alert = ttk.Frame(frame_alert)
frame_controles_alert.pack(fill="x", padx=5, pady=5)
tree_alert = ttk.Treeview(frame_alert, columns=("ID", "Nombre", "Stock", "Vencimiento", "Alerta", "Gravedad"), show="headings")
for col in ("ID", "Nombre", "Stock", "Vencimiento", "Alerta", "Gravedad"):
    tree_alert.heading(col, text=col)
    tree_alert.column(col, width=120)
tree_alert.pack(fill="both", expand=True, padx=5, pady=5)

def cargar_alertas():
    try:
        tree_alert.delete(*tree_alert.get_children())
        hoy = datetime.date.today()
        rows = run_query("SELECT Id, Nombre, Stock, FechaVencimiento FROM Productos")

        alertas_encontradas = False

        for r in rows:
            id_, nombre, stock, fecha = r
            alertas = []
            gravedad = "BAJA"

            if stock < 5:
                alertas.append(f"STOCK CRÍTICO: {stock} unidades")
                gravedad = "ALTA"
            elif stock < 10:
                alertas.append(f"Stock bajo: {stock} unidades")
                gravedad = "MEDIA"

            if fecha:
                if isinstance(fecha, datetime.date):
                    fecha_dt = fecha
                else:
                    try:
                        fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d").date()
                    except:
                        fecha_dt = None

                if fecha_dt:
                    dias_restantes = (fecha_dt - hoy).days
                    if dias_restantes <= 0:
                        alertas.append(f"VENCIDO")
                        gravedad = "ALTA"
                    elif dias_restantes <= 7:
                        alertas.append(f"Vence en {dias_restantes} días")
                        gravedad = "ALTA"
                    elif dias_restantes <= 30:
                        alertas.append(f"Vence en {dias_restantes} días")
                        if gravedad != "ALTA":
                            gravedad = "MEDIA"

            if alertas:
                alertas_encontradas = True
                fecha_str = formatear_fecha(fecha_dt)
                tree_alert.insert("", "end", values=(id_, nombre, stock, fecha_str, ", ".join(alertas), gravedad),
                                tags=(gravedad,))

        tree_alert.tag_configure("ALTA", background="#ffcccc")
        tree_alert.tag_configure("MEDIA", background="#fff0cc")
        tree_alert.tag_configure("BAJA", background="#e6f7ff")

        if not alertas_encontradas:
            messagebox.showinfo("Alertas", "✅ No hay alertas en este momento. Todo está en orden.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las alertas:\n{str(e)}")

ttk.Button(frame_controles_alert, text="🔄 Ver Alertas", command=cargar_alertas).pack(side="left", padx=5)
ttk.Button(frame_controles_alert, text="📦 Reponer Stock", command=reponer_stock_seguro).pack(side="left", padx=5)
ttk.Button(frame_controles_alert, text="💾 Exportar Alertas", command=exportar_alertas_seguro).pack(side="left", padx=5)

# ============================================================
# 3. MOVIMIENTOS - FILTROS AVANZADOS
# ============================================================
frame_mov = ttk.Frame(notebook)
notebook.add(frame_mov, text="📊 Movimientos")
frame_filtros_mov = ttk.Frame(frame_mov)
frame_filtros_mov.pack(fill="x", padx=5, pady=5)
frame_controles_mov = ttk.Frame(frame_mov)
frame_controles_mov.pack(fill="x", padx=5, pady=5)
tree_mov = ttk.Treeview(frame_mov, columns=("ID", "Producto", "Tipo", "Cantidad", "Usuario", "Fecha"), show="headings")
for col in ("ID", "Producto", "Tipo", "Cantidad", "Usuario", "Fecha"):
    tree_mov.heading(col, text=col)
    tree_mov.column(col, width=140)
tree_mov.pack(fill="both", expand=True, padx=5, pady=5)
# Filtros avanzados
ttk.Label(frame_filtros_mov, text="Fecha inicio:").grid(row=0, column=0, padx=5, pady=2)
fecha_inicio = DateEntry(frame_filtros_mov, date_pattern='yyyy-mm-dd')
fecha_inicio.grid(row=0, column=1, padx=5, pady=2)
ttk.Label(frame_filtros_mov, text="Fecha fin:").grid(row=0, column=2, padx=5, pady=2)
fecha_fin = DateEntry(frame_filtros_mov, date_pattern='yyyy-mm-dd')
fecha_fin.grid(row=0, column=3, padx=5, pady=2)
ttk.Label(frame_filtros_mov, text="Tipo:").grid(row=0, column=4, padx=5, pady=2)
combo_tipo = ttk.Combobox(frame_filtros_mov, values=["", "ENTRADA", "SALIDA", "REPOSICIÓN", "BAJA"], width=10)
combo_tipo.grid(row=0, column=5, padx=5, pady=2)
ttk.Label(frame_filtros_mov, text="Producto:").grid(row=0, column=6, padx=5, pady=2)
entry_producto_mov = ttk.Entry(frame_filtros_mov, width=15)
entry_producto_mov.grid(row=0, column=7, padx=5, pady=2)

def cargar_movimientos():
    try:
        tree_mov.delete(*tree_mov.get_children())
        rows = run_query("SELECT Id, Producto, Tipo, Cantidad, Usuario, Fecha FROM Movimientos ORDER BY Fecha DESC")
        for r in rows:
            if r[5]:
                fecha_formateada = r[5].strftime("%d/%m/%Y") if hasattr(r[5], 'strftime') else str(r[5])
            else:
                fecha_formateada = "N/A"
            tree_mov.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], fecha_formateada))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los movimientos:\n{str(e)}")

def filtrar_movimientos():
    try:
        fecha_ini = fecha_inicio.get_date()
        fecha_f = fecha_fin.get_date()
        tipo = combo_tipo.get().strip()
        producto = entry_producto_mov.get().strip()

        if fecha_ini > fecha_f:
            messagebox.showwarning("Fechas inválidas", "La fecha de inicio no puede ser mayor que la fecha fin")
            return

        query = "SELECT Id, Producto, Tipo, Cantidad, Usuario, Fecha FROM Movimientos WHERE 1=1"
        params = []

        if fecha_ini and fecha_f:
            query += " AND Fecha BETWEEN ? AND ?"
            params.extend([fecha_ini, fecha_f])

        if tipo:
            query += " AND Tipo = ?"
            params.append(tipo)

        if producto:
            query += " AND Producto LIKE ?"
            params.append(f'%{producto}%')

        query += " ORDER BY Fecha DESC"

        tree_mov.delete(*tree_mov.get_children())
        rows = run_query(query, params)

        if not rows:
            messagebox.showinfo("Resultados", "No se encontraron movimientos con los filtros aplicados")
            return

        for r in rows:
            if r[5]:
                fecha_formateada = r[5].strftime("%d/%m/%Y") if hasattr(r[5], 'strftime') else str(r[5])
            else:
                fecha_formateada = "N/A"
            tree_mov.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], fecha_formateada))

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron filtrar los movimientos:\n{str(e)}")

def limpiar_filtros():
    fecha_inicio.set_date(datetime.date.today() - datetime.timedelta(days=30))
    fecha_fin.set_date(datetime.date.today())
    combo_tipo.set("")
    entry_producto_mov.delete(0, tk.END)
    cargar_movimientos()

# Configurar fechas por defecto (últimos 30 días)
fecha_inicio.set_date(datetime.date.today() - datetime.timedelta(days=30))
fecha_fin.set_date(datetime.date.today())
ttk.Button(frame_controles_mov, text="🔄 Actualizar", command=cargar_movimientos).pack(side="left", padx=5)
ttk.Button(frame_controles_mov, text="🔍 Filtrar", command=filtrar_movimientos).pack(side="left", padx=5)
ttk.Button(frame_controles_mov, text="🧹 Limpiar Filtros", command=limpiar_filtros).pack(side="left", padx=5)
ttk.Button(frame_controles_mov, text="💾 Exportar CSV", command=exportar_movimientos_seguro).pack(side="left", padx=5)

# ============================================================
# 4. USUARIOS - GESTIÓN COMPLETA (CORREGIDA)
# ============================================================
frame_usr = ttk.Frame(notebook)
notebook.add(frame_usr, text="👥 Usuarios")
frame_form_usr = ttk.Frame(frame_usr)
frame_form_usr.pack(fill="x", padx=5, pady=5)
frame_controles_usr = ttk.Frame(frame_usr)
frame_controles_usr.pack(fill="x", padx=5, pady=5)
tree_usr = ttk.Treeview(frame_usr, columns=("ID", "Nombre", "Rol", "Estado"), show="headings")
for col in ("ID", "Nombre", "Rol", "Estado"):
    tree_usr.heading(col, text=col)
    tree_usr.column(col, width=200)
tree_usr.pack(fill="both", expand=True, padx=5, pady=5)
# Formulario usuarios
ttk.Label(frame_form_usr, text="Nombre:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_nombre_usr = ttk.Entry(frame_form_usr, width=20)
entry_nombre_usr.grid(row=0, column=1, padx=5, pady=2)
ttk.Label(frame_form_usr, text="Rol:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
combo_rol = ttk.Combobox(frame_form_usr, values=["Administrador", "Médico", "Enfermero", "Recepcionista"], width=15)
combo_rol.grid(row=0, column=3, padx=5, pady=2)

def cargar_usuarios():
    try:
        tree_usr.delete(*tree_usr.get_children())
        rows = run_query("SELECT Id, Nombre, Rol, Estado FROM Usuarios ORDER BY Nombre")
        for r in rows:
            # CORREGIDO: Asegurar que el ID sea un número
            tree_usr.insert("", "end", values=(int(r[0]), r[1], r[2], r[3]))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{str(e)}")

def limpiar_formulario_usr():
    entry_nombre_usr.delete(0, tk.END)
    combo_rol.set("")

ttk.Button(frame_controles_usr, text="🔄 Actualizar", command=cargar_usuarios).pack(side="left", padx=5)
ttk.Button(frame_controles_usr, text="➕ Agregar", command=agregar_usuario_seguro).pack(side="left", padx=5)
ttk.Button(frame_controles_usr, text="🔄 Activar/Inactivar", command=cambiar_estado_seguro).pack(side="left", padx=5)
ttk.Button(frame_controles_usr, text="🗑️ Eliminar", command=eliminar_usuario_seguro).pack(side="left", padx=5)

# ============================================================
# 5. CITAS - MÓDULO COMPLETO CON ASISTENTE VIRTUAL
# ============================================================

# ---------------------------
# MÓDULO DE CITAS Y ASISTENTE VIRTUAL
# ---------------------------

# --- CREAR TABLAS (si no existen) ---
def crear_tablas_citas():
    """
    Ejecuta sentencias SQL para crear las tablas necesarias para el módulo de citas.
    Úsalo en desarrollo/inicialización para asegurarse de que las tablas estén presentes.
    """
    try:
        # Especialidades
        run_non_query("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Especialidades' AND xtype='U')
        CREATE TABLE Especialidades (
            IdEspecialidad INT IDENTITY PRIMARY KEY,
            Nombre NVARCHAR(100) NOT NULL UNIQUE
        );
        """)

        # Doctores
        run_non_query("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Doctores' AND xtype='U')
        CREATE TABLE Doctores (
            IdDoctor INT IDENTITY PRIMARY KEY,
            Nombre NVARCHAR(100) NOT NULL,
            EspecialidadId INT NULL,
            FOREIGN KEY (EspecialidadId) REFERENCES Especialidades(IdEspecialidad)
        );
        """)

        # Pacientes
        run_non_query("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pacientes' AND xtype='U')
        CREATE TABLE Pacientes (
            IdPaciente INT IDENTITY PRIMARY KEY,
            Nombre NVARCHAR(100) NOT NULL,
            Cedula NVARCHAR(50) NULL,
            Telefono NVARCHAR(50) NULL,
            Correo NVARCHAR(150) NULL
        );
        """)

        # Citas
        run_non_query("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Citas' AND xtype='U')
        CREATE TABLE Citas (
            IdCita INT IDENTITY PRIMARY KEY,
            IdPaciente INT NOT NULL,
            IdDoctor INT NOT NULL,
            FechaCita DATETIME NOT NULL,
            Estado NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
            Observaciones NVARCHAR(255) NULL,
            FOREIGN KEY (IdPaciente) REFERENCES Pacientes(IdPaciente),
            FOREIGN KEY (IdDoctor) REFERENCES Doctores(IdDoctor)
        );
        """)
    except Exception as e:
        print(f"Error creando tablas de citas: {e}")

# --- CARGA DE DATOS (ESPECIALIDADES, DOCTORES, PACIENTES) ---
def cargar_especialidades_local():
    """Devuelve lista de tuplas (Id, Nombre) de Especialidades"""
    try:
        rows = run_query("SELECT IdEspecialidad, Nombre FROM Especialidades ORDER BY Nombre")
        return [(r[0], r[1]) for r in rows]
    except Exception as e:
        print(f"Error cargar_especialidades_local: {e}")
        return []

def cargar_doctores_local():
    """Devuelve lista de tuplas (Id, Nombre, EspecialidadId) de Doctores"""
    try:
        rows = run_query("SELECT IdDoctor, Nombre, EspecialidadId FROM Doctores ORDER BY Nombre")
        return [(r[0], r[1], r[2]) for r in rows]
    except Exception as e:
        print(f"Error cargar_doctores_local: {e}")
        return []

def cargar_pacientes_local():
    """Devuelve lista de tuplas (Id, Nombre) de Pacientes"""
    try:
        rows = run_query("SELECT IdPaciente, Nombre FROM Pacientes ORDER BY Nombre")
        return [(r[0], r[1]) for r in rows]
    except Exception as e:
        print(f"Error cargar_pacientes_local: {e}")
        return []

# --- UTILIDADES INTERNAS ---
def generar_intervalos_horarios(hora_inicio="08:00", hora_fin="17:30", intervalo_minutos=15):
    """Genera lista de strings con horarios (HH:MM)"""
    horarios = []
    h0 = datetime.datetime.strptime(hora_inicio, "%H:%M")
    hf = datetime.datetime.strptime(hora_fin, "%H:%M")
    cur = h0
    while cur <= hf:
        horarios.append(cur.strftime("%H:%M"))
        cur += datetime.timedelta(minutes=intervalo_minutos)
    return horarios

def validar_conflicto_cita(id_doctor, fecha_hora, id_cita_excluir=None):
    """
    Verifica si el doctor ya tiene una cita en la misma fecha_hora.
    Si id_cita_excluir se provee, lo omite (útil al editar).
    """
    try:
        if id_cita_excluir:
            rows = run_query("SELECT IdCita FROM Citas WHERE IdDoctor=? AND FechaCita=? AND IdCita<>?", (id_doctor, fecha_hora, id_cita_excluir))
        else:
            rows = run_query("SELECT IdCita FROM Citas WHERE IdDoctor=? AND FechaCita=?", (id_doctor, fecha_hora))
        return len(rows) > 0
    except Exception as e:
        print(f"Error validar_conflicto_cita: {e}")
        return False

# ---------------------------
# UI: Pestaña de CITAS
# ---------------------------
# ============================================================
# 5. CITAS - MÓDULO FLEXIBLE
# ============================================================

frame_citas = ttk.Frame(notebook)
notebook.add(frame_citas, text="📅 Citas")

# Subframes
frame_form_citas = ttk.Frame(frame_citas)
frame_form_citas.pack(fill="x", padx=5, pady=6)

frame_controles_citas = ttk.Frame(frame_citas)
frame_controles_citas.pack(fill="x", padx=5, pady=4)

frame_tree_citas = ttk.Frame(frame_citas)
frame_tree_citas.pack(fill="both", expand=True, padx=5, pady=4)

# Formulario simplificado
ttk.Label(frame_form_citas, text="👤 Paciente:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
entry_paciente = ttk.Entry(frame_form_citas, width=30)
entry_paciente.grid(row=0, column=1, padx=5, pady=4)

ttk.Label(frame_form_citas, text="👨‍⚕️ Doctor:").grid(row=0, column=2, padx=5, pady=4, sticky="w")
entry_doctor = ttk.Entry(frame_form_citas, width=25)
entry_doctor.grid(row=0, column=3, padx=5, pady=4)

ttk.Label(frame_form_citas, text="🎯 Especialidad:").grid(row=1, column=0, padx=5, pady=4, sticky="w")
combo_especialidad = ttk.Combobox(frame_form_citas, width=30, values=[
    "Medicina General", "Pediatría", "Cardiología", "Dermatología", 
    "Ginecología", "Traumatología", "Oftalmología", "Neurología"
])
combo_especialidad.grid(row=1, column=1, padx=5, pady=4)
combo_especialidad.set("Medicina General")

ttk.Label(frame_form_citas, text="📅 Fecha:").grid(row=1, column=2, padx=5, pady=4, sticky="w")
date_cita = DateEntry(frame_form_citas, date_pattern='yyyy-mm-dd')
date_cita.grid(row=1, column=3, padx=5, pady=4)

ttk.Label(frame_form_citas, text="⏰ Hora:").grid(row=2, column=0, padx=5, pady=4, sticky="w")
combo_hora = ttk.Combobox(frame_form_citas, values=generar_intervalos_horarios(), width=10)
combo_hora.grid(row=2, column=1, padx=5, pady=4)
combo_hora.set("08:00")

ttk.Label(frame_form_citas, text="📝 Observaciones:").grid(row=2, column=2, padx=5, pady=4, sticky="w")
entry_observaciones = ttk.Entry(frame_form_citas, width=40)
entry_observaciones.grid(row=2, column=3, padx=5, pady=4)

# Botones de acción
btn_agendar_cita = ttk.Button(frame_form_citas, text="➕ Agendar Cita", width=15, command=agendar_cita_seguro)
btn_agendar_cita.grid(row=3, column=1, padx=5, pady=8)

btn_editar_cita = ttk.Button(frame_form_citas, text="✏️ Editar Cita", width=15, command=editar_cita_seguro)
btn_editar_cita.grid(row=3, column=2, padx=5, pady=8)

btn_cancelar_cita = ttk.Button(frame_form_citas, text="❌ Cancelar Cita", width=15, command=cancelar_cita_seguro)
btn_cancelar_cita.grid(row=3, column=3, padx=5, pady=8)

# Controles
ttk.Label(frame_controles_citas, text="Buscar:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
entry_buscar_cita = ttk.Entry(frame_controles_citas, width=25)
entry_buscar_cita.grid(row=0, column=1, padx=5, pady=4)

ttk.Button(frame_controles_citas, text="🔍 Buscar", command=buscar_citas_flexibles).grid(row=0, column=2, padx=5, pady=4)
ttk.Button(frame_controles_citas, text="🔄 Actualizar", command=cargar_citas_flexibles).grid(row=0, column=3, padx=5, pady=4)
ttk.Button(frame_controles_citas, text="💾 Exportar CSV", command=exportar_citas_csv_seguro).grid(row=0, column=4, padx=5, pady=4)
ttk.Button(frame_controles_citas, text="📧 Sistema de Correos",command=abrir_sistema_correos).grid(row=0, column=6, padx=5, pady=4)

# Treeview
tree_citas = ttk.Treeview(frame_tree_citas, columns=("ID", "Paciente", "Doctor", "Especialidad", "FechaHora", "Estado", "Observaciones"), show="headings")
for col, width in [("ID",80), ("Paciente",220), ("Doctor",180), ("Especialidad",140), ("FechaHora",160), ("Estado",100), ("Observaciones",220)]:
    tree_citas.heading(col, text=col)
    tree_citas.column(col, width=width)
tree_citas.pack(fill="both", expand=True)

def generar_intervalos_horarios(hora_inicio="08:00", hora_fin="17:30", intervalo_minutos=15):
    """Genera lista de strings con horarios (HH:MM)"""
    horarios = []
    h0 = dt.strptime(hora_inicio, "%H:%M")
    hf = dt.strptime(hora_fin, "%H:%M")
    cur = h0
    while cur <= hf:
        horarios.append(cur.strftime("%H:%M"))
        cur += timedelta(minutes=intervalo_minutos)
    return horarios

# --- FUNCIONES FLEXIBLES PARA CITAS ---
def agendar_cita_flexible():
    """Agendar cita sin depender de IDs de base de datos - VERSIÓN CORREGIDA"""
    if not verificar_permiso('citas', 'crear'):
        mostrar_error_permiso()
        return

    try:
        paciente = entry_paciente.get().strip()
        doctor = entry_doctor.get().strip()
        especialidad = combo_especialidad.get().strip()
        fecha = date_cita.get_date()
        hora = combo_hora.get().strip()
        observaciones = entry_observaciones.get().strip()

        # Validaciones básicas MÁS ESTRICTAS
        if not paciente:
            messagebox.showwarning("Datos incompletos", "Por favor ingrese el nombre del paciente")
            entry_paciente.focus()
            return

        if not doctor:
            messagebox.showwarning("Datos incompletos", "Por favor ingrese el nombre del doctor")
            entry_doctor.focus()
            return

        if not especialidad:
            messagebox.showwarning("Datos incompletos", "Por favor seleccione una especialidad")
            combo_especialidad.focus()
            return

        if not hora:
            messagebox.showwarning("Datos incompletos", "Por favor seleccione una hora")
            combo_hora.focus()
            return

        # Combinar fecha y hora CON VALIDACIÓN
        try:
            from datetime import datetime as dt
            fecha_hora = dt.combine(fecha, dt.strptime(hora, "%H:%M").time())
            print(f"✅ Fecha y hora combinadas: {fecha_hora}")
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de hora inválido. Use HH:MM (ej: 14:30)\nError: {ve}")
            combo_hora.focus()
            return

        # Verificar que la fecha no sea en el pasado
        if fecha_hora < dt.now():
            messagebox.showwarning("Fecha inválida", "No se pueden agendar citas en fechas pasadas")
            date_cita.focus()
            return

        # DEBUG: Mostrar datos que se van a insertar
        print(f"DEBUG - Insertando cita:")
        print(f"  Paciente: {paciente}")
        print(f"  Doctor: {doctor}")
        print(f"  Especialidad: {especialidad}")
        print(f"  FechaHora: {fecha_hora}")
        print(f"  Observaciones: {observaciones}")
        print(f"  Usuario: {USUARIO_ACTUAL}")

        # Insertar en base de datos CON MANEJO MEJORADO DE ERRORES
        query = """
        INSERT INTO CitasFlexibles 
        (Paciente, Doctor, Especialidad, FechaCita, Observaciones, Estado, UsuarioCreacion) 
        VALUES (?, ?, ?, ?, ?, 'Pendiente', ?)
        """
        
        params = (paciente, doctor, especialidad, fecha_hora, observaciones, USUARIO_ACTUAL)
        
        print(f"DEBUG - Query: {query}")
        print(f"DEBUG - Params: {params}")
        
        if run_non_query(query, params):
            messagebox.showinfo("Éxito", f"✅ Cita agendada para {paciente} con {doctor}")
            limpiar_formulario_cita()
            cargar_citas_flexibles()
        else:
            messagebox.showerror("Error", "No se pudo agendar la cita. Verifique los datos.")

    except Exception as e:
        error_msg = f"No se pudo agendar la cita:\n{str(e)}"
        print(f"❌ ERROR en agendar_cita_flexible: {e}")
        messagebox.showerror("Error", error_msg)

def cargar_citas_flexibles():
    """Cargar citas desde la tabla flexible"""
    try:
        tree_citas.delete(*tree_citas.get_children())
        rows = run_query("""
            SELECT IdCita, Paciente, Doctor, Especialidad, FechaCita, Estado, Observaciones
            FROM CitasFlexibles 
            ORDER BY FechaCita DESC
        """)
        
        for r in rows:
            fecha_str = r[4].strftime("%d/%m/%Y %H:%M") if hasattr(r[4], 'strftime') else str(r[4])
            tree_citas.insert("", "end", values=(
                r[0], r[1], r[2], r[3], fecha_str, r[5], r[6] if r[6] else ""
            ))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las citas:\n{str(e)}")

def editar_cita_flexible():
    """Editar cita flexible"""
    if not verificar_permiso('citas', 'actualizar'):
        mostrar_error_permiso()
        return

    item = tree_citas.selection()
    if not item:
        messagebox.showwarning("Seleccionar", "Seleccione una cita para editar")
        return

    try:
        valores = tree_citas.item(item[0])["values"]
        if not valores:
            return

        # Llenar formulario con datos actuales
        entry_paciente.delete(0, tk.END)
        entry_paciente.insert(0, valores[1])
        
        entry_doctor.delete(0, tk.END)
        entry_doctor.insert(0, valores[2])
        
        combo_especialidad.set(valores[3])
        
        # Parsear fecha y hora
        try:
            fecha_hora = dt.strptime(valores[4], "%d/%m/%Y %H:%M")
            date_cita.set_date(fecha_hora.date())
            combo_hora.set(fecha_hora.strftime("%H:%M"))
        except:
            pass
        
        entry_observaciones.delete(0, tk.END)
        entry_observaciones.insert(0, valores[6] if valores[6] else "")

        # Cambiar botón a modo edición
        def confirmar_edicion():
            try:
                id_cita = int(valores[0])
                nuevo_paciente = entry_paciente.get().strip()
                nuevo_doctor = entry_doctor.get().strip()
                nueva_especialidad = combo_especialidad.get().strip()
                nueva_fecha = date_cita.get_date()
                nueva_hora = combo_hora.get().strip()
                nuevas_observaciones = entry_observaciones.get().strip()

                if not nuevo_paciente or not nuevo_doctor:
                    messagebox.showwarning("Datos incompletos", "Complete paciente y doctor")
                    return

                nueva_fecha_hora = dt.combine(nueva_fecha, dt.strptime(nueva_hora, "%H:%M").time())

                # Actualizar en base de datos
                query = """
                UPDATE CitasFlexibles 
                SET Paciente=?, Doctor=?, Especialidad=?, FechaCita=?, Observaciones=?
                WHERE IdCita=?
                """
                
                if run_non_query(query, (nuevo_paciente, nuevo_doctor, nueva_especialidad, 
                                       nueva_fecha_hora, nuevas_observaciones, id_cita)):
                    messagebox.showinfo("Éxito", "Cita actualizada correctamente")
                    cargar_citas_flexibles()
                    limpiar_formulario_cita()
                    # Restaurar botón normal
                    btn_agendar_cita.config(text="➕ Agendar Cita", command=agendar_cita_flexible)
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la cita")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la cita:\n{str(e)}")

        btn_agendar_cita.config(text="💾 Guardar Cambios", command=confirmar_edicion)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la cita para editar:\n{str(e)}")

def cancelar_cita_flexible():
    """Cancelar cita flexible"""
    if not verificar_permiso('citas', 'eliminar'):
        mostrar_error_permiso()
        return

    item = tree_citas.selection()
    if not item:
        messagebox.showwarning("Seleccionar", "Seleccione una cita para cancelar")
        return

    try:
        valores = tree_citas.item(item[0])["values"]
        id_cita = int(valores[0])
        paciente = valores[1]

        if messagebox.askyesno("Confirmar", f"¿Cancelar la cita de {paciente}?"):
            if run_non_query("UPDATE CitasFlexibles SET Estado='Cancelada' WHERE IdCita=?", (id_cita,)):
                messagebox.showinfo("Éxito", "Cita cancelada correctamente")
                cargar_citas_flexibles()
            else:
                messagebox.showerror("Error", "No se pudo cancelar la cita")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cancelar la cita:\n{str(e)}")

def buscar_citas_flexibles():
    """Buscar citas flexibles"""
    try:
        texto_busqueda = entry_buscar_cita.get().strip()
        if not texto_busqueda:
            cargar_citas_flexibles()
            return

        tree_citas.delete(*tree_citas.get_children())
        rows = run_query("""
            SELECT IdCita, Paciente, Doctor, Especialidad, FechaCita, Estado, Observaciones
            FROM CitasFlexibles 
            WHERE Paciente LIKE ? OR Doctor LIKE ? OR Especialidad LIKE ?
            ORDER BY FechaCita DESC
        """, (f'%{texto_busqueda}%', f'%{texto_busqueda}%', f'%{texto_busqueda}%'))
        
        for r in rows:
            fecha_str = r[4].strftime("%d/%m/%Y %H:%M") if hasattr(r[4], 'strftime') else str(r[4])
            tree_citas.insert("", "end", values=(
                r[0], r[1], r[2], r[3], fecha_str, r[5], r[6] if r[6] else ""
            ))
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo buscar:\n{str(e)}")

def limpiar_formulario_cita():
    """Limpiar formulario de citas"""
    entry_paciente.delete(0, tk.END)
    entry_doctor.delete(0, tk.END)
    combo_especialidad.set("Medicina General")
    date_cita.set_date(date.today())
    combo_hora.set("08:00")
    entry_observaciones.delete(0, tk.END)
def exportar_citas_csv():
    try:
        filename = f"citas_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("ID,Paciente,Doctor,Especialidad,FechaHora,Estado,Observaciones\n")
            for child in tree_citas.get_children():
                vals = tree_citas.item(child)["values"]
                # Escape comas en observaciones
                obs = (vals[6] or "").replace(",", " ")
                f.write(",".join([str(vals[0]), str(vals[1]), str(vals[2]), str(vals[3]), str(vals[4]), str(vals[5]), obs]) + "\n")
        messagebox.showinfo("Exportado", f"Citas exportadas a {filename}")
        os.startfile(filename)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

# ---------------------------
# ASISTENTE VIRTUAL (BÁSICO) - VENTANA DE CHAT
# ---------------------------
def abrir_asistente():
    try:
        ventana_chat = tk.Toplevel(root)
        ventana_chat.title("Asistente Virtual - Clínica San Rafael")
        ventana_chat.geometry("500x600")
        ventana_chat.resizable(False, False)
        ventana_chat.configure(bg='#2C3E50')

        # Frame principal
        main_frame = tk.Frame(ventana_chat, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header con controles de voz
        header_frame = tk.Frame(main_frame, bg='#34495E', relief='ridge', bd=2)
        header_frame.pack(fill='x', pady=(0, 10))

        tk.Label(header_frame, text="🎤 Asistente Virtual con Voz", 
                font=('Arial', 12, 'bold'), bg='#34495E', fg='white').pack(pady=5)

        # Controles de voz
        voice_frame = tk.Frame(header_frame, bg='#34495E')
        voice_frame.pack(pady=5)

        btn_silenciar = tk.Button(voice_frame, text="🔇 Silenciar Voz", 
                                 command=lambda: asistente_voz.engine.setProperty('volume', 0),
                                 bg='#E74C3C', fg='white', font=('Arial', 8))
        btn_silenciar.pack(side='left', padx=5)

        btn_activar = tk.Button(voice_frame, text="🔊 Activar Voz", 
                               command=lambda: asistente_voz.engine.setProperty('volume', 0.8),
                               bg='#27AE60', fg='white', font=('Arial', 8))
        btn_activar.pack(side='left', padx=5)

        # Historial de chat con scroll
        frame_historial = tk.Frame(main_frame, bg='#2C3E50')
        frame_historial.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(frame_historial)
        scrollbar.pack(side='right', fill='y')

        txt_historial = tk.Text(frame_historial, wrap='word', state='disabled', 
                               width=60, height=20, bg='#ECF0F1', fg='#2C3E50',
                               font=('Arial', 10), yscrollcommand=scrollbar.set)
        txt_historial.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=txt_historial.yview)

        # Frame de entrada
        frame_input = tk.Frame(main_frame, bg='#2C3E50')
        frame_input.pack(fill='x', pady=10)

        # Ejemplos rápidos
        ejemplos_frame = tk.Frame(main_frame, bg='#2C3E50')
        ejemplos_frame.pack(fill='x', pady=5)

        tk.Label(ejemplos_frame, text="💡 Ejemplos:", font=('Arial', 9, 'bold'), 
                bg='#2C3E50', fg='#BDC3C7').pack(anchor='w')

        ejemplos = [
            "📊 Inventario bajo",
            "📅 Citas del Dr. Pérez",
            "💊 Stock de Paracetamol",
            "👥 Usuarios activos"
        ]

        def crear_boton_ejemplo(texto):
            btn = tk.Button(ejemplos_frame, text=texto, 
                          command=lambda: insertar_ejemplo(texto),
                          bg='#3498DB', fg='white', font=('Arial', 8),
                          relief='flat', padx=10, pady=2)
            btn.pack(side='left', padx=2)

        for ejemplo in ejemplos:
            crear_boton_ejemplo(ejemplo)

        def insertar_ejemplo(texto):
            entry_msg.delete(0, tk.END)
            entry_msg.insert(0, texto)

        entry_msg = tk.Entry(frame_input, width=45, font=('Arial', 11),
                            bg='#ECF0F1', fg='#2C3E50', relief='solid', bd=1)
        entry_msg.pack(side='left', padx=(0, 10), pady=4, fill='x', expand=True)
        entry_msg.focus()

        def enviar_mensaje():
            mensaje = entry_msg.get().strip()
            if not mensaje:
                return
            
            entry_msg.delete(0, tk.END)
            
            # Mostrar mensaje del usuario
            mostrar_mensaje_usuario(mensaje)
            
            # Procesar y obtener respuesta
            respuesta = procesar_mensaje_asistente_mejorado(mensaje)
            
            # Mostrar respuesta del asistente
            mostrar_mensaje_asistente(respuesta)
            
            # Reproducir respuesta en voz
            asistente_voz.hablar(respuesta)

        def mostrar_mensaje_usuario(mensaje):
            txt_historial.config(state='normal')
            txt_historial.insert(tk.END, f"👤 Tú: {mensaje}\n", 'usuario')
            txt_historial.config(state='disabled')
            txt_historial.see(tk.END)

        def mostrar_mensaje_asistente(respuesta):
            txt_historial.config(state='normal')
            txt_historial.insert(tk.END, f"🤖 Asistente: {respuesta}\n\n", 'asistente')
            txt_historial.config(state='disabled')
            txt_historial.see(tk.END)

        # Configurar estilos de texto
        txt_historial.tag_configure('usuario', foreground='#2C3E50', 
                                   font=('Arial', 10, 'bold'))
        txt_historial.tag_configure('asistente', foreground='#27AE60', 
                                   font=('Arial', 10))

        btn_enviar = tk.Button(frame_input, text="Enviar 📤", command=enviar_mensaje,
                              bg='#27AE60', fg='white', font=('Arial', 10, 'bold'),
                              relief='flat', padx=15)
        btn_enviar.pack(side='right')

        # Atajos de teclado
        def on_enter(event):
            enviar_mensaje()
        entry_msg.bind('<Return>', on_enter)

        # Mensaje de bienvenida inicial
        bienvenida = """¡Hola! Soy tu asistente virtual con voz. 😊

Puedo ayudarte con:
• 📊 Consultas de inventario y stock
• 📅 Gestión de citas médicas  
• 💊 Información de medicamentos
• 👥 Datos de usuarios y doctores
• ⚠️ Alertas del sistema

¡Pregúntame lo que necesites!"""
        
        mostrar_mensaje_asistente(bienvenida)
        asistente_voz.hablar("¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el asistente:\n{e}")

# ---------------------------
# PROCESADOR MEJORADO DE MENSAJES
# ---------------------------
def procesar_mensaje_asistente_mejorado(mensaje_raw):
    """
    Procesamiento mejorado con más funcionalidades y ejemplos específicos
    """
    try:
        mensaje = mensaje_raw.lower().strip()
        
        # =============================================
        # 1. SALUDOS Y AYUDA GENERAL
        # =============================================
        saludos = ["hola", "buenos días", "buenas tardes", "buenas noches", "hi", "hey"]
        if any(saludo in mensaje for saludo in saludos) and len(mensaje.split()) <= 3:
            return "¡Hola! 😊 Soy tu asistente virtual. Puedo ayudarte con consultas de inventario, citas, medicamentos y más. ¿En qué te puedo ayudar?"

        if any(palabra in mensaje for palabra in ["ayuda", "qué puedes hacer", "funciones"]):
            return """Puedo ayudarte con:

📊 **INVENTARIO:**
• "¿Qué productos tienen stock bajo?"
• "Ver inventario completo"
• "Stock de [medicamento]"

📅 **CITAS:**
• "Citas del Dr. [nombre]"
• "Buscar citas de [paciente]"
• "Citas para hoy"

💊 **MEDICAMENTOS:**
• "Información de [medicamento]"
• "Productos que vencen pronto"
• "Medicamentos en stock"

👥 **USUARIOS:**
• "Usuarios activos"
• "Doctores disponibles"

⚠️ **ALERTAS:**
• "Alertas activas"
• "Stock crítico"

¡Pregúntame lo que necesites!"""

        # =============================================
        # 2. CONSULTAS DE INVENTARIO
        # =============================================
        if any(palabra in mensaje for palabra in ["inventario", "stock", "productos", "medicamentos"]):
            
            # Ejemplo: "inventario bajo", "stock bajo", "productos con poco stock"
            if "bajo" in mensaje or "poco" in mensaje or "crítico" in mensaje:
                productos_bajos = run_query("SELECT Nombre, Stock FROM Productos WHERE Stock < 10 ORDER BY Stock ASC")
                if productos_bajos:
                    respuesta = "📊 Productos con stock bajo:\n"
                    for producto, stock in productos_bajos:
                        respuesta += f"• {producto}: {stock} unidades\n"
                    return respuesta
                else:
                    return "✅ No hay productos con stock bajo. Todo está en orden."
            
            # Ejemplo: "inventario completo", "ver todo el stock"
            elif "completo" in mensaje or "todo" in mensaje:
                productos = run_query("SELECT Nombre, Stock FROM Productos ORDER BY Nombre")
                if productos:
                    respuesta = "📦 Inventario completo:\n"
                    for producto, stock in productos:
                        respuesta += f"• {producto}: {stock} unidades\n"
                    return respuesta
                else:
                    return "No hay productos en el inventario."
            
            # Ejemplo: "stock de paracetamol", "cuánto hay de amoxicilina"
            elif "stock de" in mensaje or "cuánto hay de" in mensaje:
                palabras = mensaje.split()
                for i, palabra in enumerate(palabras):
                    if palabra == "de" and i+1 < len(palabras):
                        medicamento = " ".join(palabras[i+1:])
                        resultado = run_query("SELECT Stock FROM Productos WHERE Nombre LIKE ?", (f'%{medicamento}%',))
                        if resultado:
                            return f"💊 {medicamento.capitalize()}: {resultado[0][0]} unidades en stock"
                        else:
                            return f"❌ No encontré el medicamento '{medicamento}'"
                
                return "Por favor, especifica de qué medicamento quieres consultar el stock. Ejemplo: 'stock de paracetamol'"

        # =============================================
        # 3. CONSULTAS DE CITAS
        # =============================================
        if any(palabra in mensaje for palabra in ["citas", "cita", "agendar", "doctor"]):
            
            # Ejemplo: "citas del dr. pérez", "citas doctor pérez"
            if any(palabra in mensaje for palabra in ["dr", "doctor", "dra"]):
                palabras = mensaje.replace("dr.", "dr").replace("dra.", "dra").split()
                doctor_nombre = None
                
                for i, palabra in enumerate(palabras):
                    if palabra in ["dr", "doctor", "dra"] and i+1 < len(palabras):
                        doctor_nombre = palabras[i+1].capitalize()
                        if i+2 < len(palabras) and len(palabras[i+2]) > 2:
                            doctor_nombre += " " + palabras[i+2].capitalize()
                        break
                
                if doctor_nombre:
                    rows = run_query("SELECT IdDoctor, Nombre FROM Doctores WHERE Nombre LIKE ?", (f'%{doctor_nombre}%',))
                    if rows:
                        id_doc = rows[0][0]
                        hoy = datetime.date.today()
                        fecha_ini = datetime.datetime.combine(hoy, datetime.time.min)
                        fecha_fin = datetime.datetime.combine(hoy, datetime.time.max)
                        
                        citas = run_query("""
                            SELECT p.Nombre, c.FechaCita, c.Estado 
                            FROM Citas c
                            JOIN Pacientes p ON c.IdPaciente = p.IdPaciente
                            WHERE c.IdDoctor = ? AND c.FechaCita BETWEEN ? AND ?
                            ORDER BY c.FechaCita
                        """, (id_doc, fecha_ini, fecha_fin))
                        
                        if citas:
                            respuesta = f"📅 Citas de {rows[0][1]} para hoy:\n"
                            for paciente, fecha, estado in citas:
                                hora = fecha.strftime("%H:%M")
                                respuesta += f"• {hora} - {paciente} ({estado})\n"
                            return respuesta
                        else:
                            return f"ℹ️ El Dr. {rows[0][1]} no tiene citas para hoy."
                    else:
                        return f"❌ No encontré al doctor '{doctor_nombre}'"
            
            # Ejemplo: "citas para hoy", "qué citas hay hoy"
            elif "hoy" in mensaje:
                hoy = datetime.date.today()
                fecha_ini = datetime.datetime.combine(hoy, datetime.time.min)
                fecha_fin = datetime.datetime.combine(hoy, datetime.time.max)
                
                citas = run_query("""
                    SELECT d.Nombre, p.Nombre, c.FechaCita 
                    FROM Citas c
                    JOIN Doctores d ON c.IdDoctor = d.IdDoctor
                    JOIN Pacientes p ON c.IdPaciente = p.IdPaciente
                    WHERE c.FechaCita BETWEEN ? AND ?
                    ORDER BY c.FechaCita
                """, (fecha_ini, fecha_fin))
                
                if citas:
                    respuesta = "📅 Citas para hoy:\n"
                    for doctor, paciente, fecha in citas:
                        hora = fecha.strftime("%H:%M")
                        respuesta += f"• {hora} - Dr. {doctor} con {paciente}\n"
                    return respuesta
                else:
                    return "✅ No hay citas programadas para hoy."

        # =============================================
        # 4. INFORMACIÓN DE MEDICAMENTOS
        # =============================================
        if any(palabra in mensaje for palabra in ["paracetamol", "amoxicilina", "ibuprofeno", "aspirina", "omeprazol"]):
            medicamentos = {
                "paracetamol": "💊 Paracetamol 500mg\n• Uso: Analgésico y antipirético\n• Dosis: 1-2 comprimidos cada 6-8 horas\n• Stock actual: Consultar con 'stock de paracetamol'",
                "amoxicilina": "💊 Amoxicilina 500mg\n• Uso: Antibiótico para infecciones bacterianas\n• Dosis: 1 comprimido cada 8 horas\n• Stock actual: Consultar con 'stock de amoxicilina'",
                "ibuprofeno": "💊 Ibuprofeno 400mg\n• Uso: Antiinflamatorio y analgésico\n• Dosis: 1 comprimido cada 8 horas\n• Stock actual: Consultar con 'stock de ibuprofeno'",
                "aspirina": "💊 Aspirina\n• Uso: Analgésico y antiagregante plaquetario\n• Dosis: Según prescripción médica\n• Stock actual: Consultar con 'stock de aspirina'",
                "omeprazol": "💊 Omeprazol 20mg\n• Uso: Protector gástrico\n• Dosis: 1 comprimido antes del desayuno\n• Stock actual: Consultar con 'stock de omeprazol'"
            }
            
            for med, info in medicamentos.items():
                if med in mensaje:
                    return info

        # =============================================
        # 5. CONSULTAS DE USUARIOS
        # =============================================
        if any(palabra in mensaje for palabra in ["usuarios", "doctores", "empleados"]):
            
            # Ejemplo: "usuarios activos", "cuántos usuarios hay"
            if "activos" in mensaje or "activo" in mensaje:
                usuarios = run_query("SELECT COUNT(*) FROM Usuarios WHERE Estado = 'Activo'")
                if usuarios:
                    return f"👥 Usuarios activos en el sistema: {usuarios[0][0]}"
            
            # Ejemplo: "doctores disponibles", "lista de doctores"
            elif "doctor" in mensaje or "doctores" in mensaje:
                doctores = run_query("SELECT d.Nombre, e.Nombre FROM Doctores d LEFT JOIN Especialidades e ON d.EspecialidadId = e.IdEspecialidad")
                if doctores:
                    respuesta = "👨‍⚕️ Doctores disponibles:\n"
                    for doctor, especialidad in doctores:
                        esp = especialidad if especialidad else "Sin especialidad"
                        respuesta += f"• {doctor} - {esp}\n"
                    return respuesta

        # =============================================
        # 6. ALERTAS DEL SISTEMA
        # =============================================
        if any(palabra in mensaje for palabra in ["alertas", "alerta", "problemas", "crítico"]):
            # Alertas de stock bajo
            stock_bajo = run_query("SELECT COUNT(*) FROM Productos WHERE Stock < 5")
            # Alertas de vencimiento (próximos 7 días)
            hoy = datetime.date.today()
            vencimiento = run_query("SELECT COUNT(*) FROM Productos WHERE FechaVencimiento BETWEEN ? AND ?", 
                                   (hoy, hoy + datetime.timedelta(days=7)))
            
            if stock_bajo[0][0] > 0 or vencimiento[0][0] > 0:
                respuesta = "⚠️ Alertas activas:\n"
                if stock_bajo[0][0] > 0:
                    respuesta += f"• {stock_bajo[0][0]} productos con stock crítico\n"
                if vencimiento[0][0] > 0:
                    respuesta += f"• {vencimiento[0][0]} productos próximos a vencer\n"
                respuesta += "\nRevisa la pestaña '⚠️ Alertas' para más detalles."
                return respuesta
            else:
                return "✅ No hay alertas activas. Todo está en orden."

        # =============================================
        # 7. RESPUESTA POR DEFECTO
        # =============================================
        return "🤔 No entendí completamente tu pregunta. Puedo ayudarte con:\n• Consultas de inventario\n• Gestión de citas\n• Información de medicamentos\n• Alertas del sistema\n\nPrueba con: 'stock bajo', 'citas de hoy' o 'ayuda'"

    except Exception as e:
        print(f"Error en procesamiento mejorado: {e}")
        return "❌ Ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo."

# --- DATOS DE EJEMPLO PARA CITAS ---
def insertar_datos_ejemplo_citas():
    """Insertar datos de ejemplo para testing"""
    try:
        # Verificar si ya existen datos
        existing_esp = run_query("SELECT COUNT(*) FROM Especialidades")
        if existing_esp and existing_esp[0][0] > 0:
            return
            
        # Insertar especialidades
        especialidades = ['Medicina General', 'Pediatría', 'Cardiología', 'Dermatología', 'Ginecología']
        for esp in especialidades:
            run_non_query("INSERT INTO Especialidades (Nombre) VALUES (?)", (esp,))
        
        # Insertar doctores
        doctores = [
            ('Dr. Carlos Rodríguez', 1),
            ('Dra. María González', 2), 
            ('Dr. Roberto Sánchez', 3),
            ('Dra. Laura Mendoza', 4),
            ('Dra. Ana López', 5)
        ]
        for doc, esp_id in doctores:
            run_non_query("INSERT INTO Doctores (Nombre, EspecialidadId) VALUES (?, ?)", (doc, esp_id))
            
        # Insertar algunos pacientes de ejemplo
        pacientes = [
            ('Juan Pérez', '12345678', '555-1234', 'juan@email.com'),
            ('María García', '87654321', '555-5678', 'maria@email.com'),
            ('Carlos López', '11223344', '555-9012', 'carlos@email.com')
        ]
        for pac in pacientes:
            run_non_query("INSERT INTO Pacientes (Nombre, Cedula, Telefono, Correo) VALUES (?, ?, ?, ?)", pac)
            
        print("Datos de ejemplo para citas insertados correctamente")
    except Exception as e:
        print(f"Error insertando datos ejemplo: {e}")
# ---------------------------
# INICIALIZACIÓN Y EJECUCIÓN
# ---------------------------
def crear_barra_estado():
    """Crea una barra de estado en la ventana principal"""
    global root
    barra_estado = tk.Frame(root, bg="#0A64A4", height=25)
    barra_estado.pack(side="bottom", fill="x")
    tk.Label(barra_estado, text=f"Usuario: {USUARIO_ACTUAL} | Rol: {ROL_ACTUAL}",
             bg="#0A64A4", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=10)

# ---------------------------
# INICIALIZACIÓN ACTUALIZADA CON MÓDULO DE CITAS
# ---------------------------
def inicializar_aplicacion_completa():
    """Cargar datos iniciales al abrir la aplicación - VERSIÓN COMPLETA"""
    
    # 1. Cargar módulos existentes
    cargar_inventario()
    cargar_usuarios()
    cargar_movimientos()
    cargar_alertas()
    crear_barra_estado()
    
    # 2. Configurar interfaz según rol
    configurar_interfaz_por_rol()
    configurar_botones_por_permisos()
    
    # 3. INICIALIZACIÓN DEL MÓDULO DE CITAS
    try:
        # Crear tablas necesarias (seguro-idempotente)
        crear_tablas_citas()
        cargar_citas_flexibles()
        
        # Insertar datos de ejemplo (opcional, para testing)
        insertar_datos_ejemplo_citas()
        
        # Cargar citas en Treeview
        cargar_citas_flexibles()
        
        # Añadir botón flotante del asistente
        if not hasattr(root, "btn_asistente_creado"):
            btn_asistente = tk.Button(root, text="💬 Asistente", command=abrir_asistente, 
                                    bg=theme_manager.themes[theme_manager.current_theme]["accent_color"], 
                                    fg="white", relief="flat", font=("Arial", 10, "bold"),
                                    cursor="hand2")
            btn_asistente.place(relx=0.93, rely=0.92, anchor="center")
            root.btn_asistente_creado = True
            
    except Exception as e:
        print(f"Error inicializando módulo de citas: {e}")
    
    # 4. INICIALIZAR REPORTES (después de que todo esté listo)
    try:
        crear_pestana_reportes()
        print("✅ Módulo de reportes inicializado")
    except Exception as e:
        print(f"❌ Error inicializando reportes: {e}")

# Reemplazar la función de inicialización anterior
inicializar_aplicacion = inicializar_aplicacion_completa

# ---------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------
if __name__ == "__main__":
    # Iniciar con el sistema de login
    app_login = SistemaLogin()
    app_login.login_window.mainloop()


