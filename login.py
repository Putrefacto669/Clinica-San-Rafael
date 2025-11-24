# login.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import threading
import time
from database import run_query
from permisos import SistemaPermisos
from config import USUARIO_ACTUAL, ROL_ACTUAL, SISTEMA_PERMISOS

class SistemaLogin:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Clínica Popular San Rafael - Acceso al Sistema")
        self.login_window.geometry("450x550")
        self.login_window.configure(bg='#2C3E50')
        self.login_window.resizable(False, False)
        self.login_window.protocol("WM_DELETE_WINDOW", self.salir_sistema)

        self.sistema_permisos = SistemaPermisos()
        self.centrar_ventana()
        self.crear_interfaz_login()
        self.cargar_usuarios_db()

    def centrar_ventana(self):
        """Centrar ventana en la pantalla"""
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (550 // 2)
        self.login_window.geometry(f"450x550+{x}+{y}")

    def crear_interfaz_login(self):
        # Frame principal
        main_frame = tk.Frame(self.login_window, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Logo/Header
        header_frame = tk.Frame(main_frame, bg='#2C3E50')
        header_frame.pack(pady=(0, 30))

        tk.Label(header_frame, text="🏥", font=('Arial', 48), bg='#2C3E50', fg='#3498DB').pack()
        tk.Label(header_frame, text="Clínica San Rafael", font=('Arial', 20, 'bold'), 
                bg='#2C3E50', fg='#ECF0F1').pack(pady=(10, 5))
        tk.Label(header_frame, text="Sistema de Gestión Médica", font=('Arial', 12), 
                bg='#2C3E50', fg='#BDC3C7').pack()

        # Información de roles
        self.crear_info_roles(main_frame)
        # Formulario de login
        self.crear_formulario_login(main_frame)

    def crear_info_roles(self, parent):
        info_frame = tk.Frame(parent, bg='#34495E', relief='ridge', bd=1)
        info_frame.pack(fill='x', pady=(0, 20))

        tk.Label(info_frame, text="👥 Roles del Sistema:", font=('Arial', 10, 'bold'),
                bg='#34495E', fg='#ECF0F1').pack(pady=(10, 5))

        roles_text = "• Admin: Acceso completo\n• Médico: Consultas y visualización\n• Enfermero: Gestión medicamentos\n• Recepcionista: Consulta básica"
        tk.Label(info_frame, text=roles_text, font=('Arial', 8), bg='#34495E', 
                fg='#BDC3C7', justify='left').pack(pady=(0, 10))

    def crear_formulario_login(self, parent):
        form_frame = tk.Frame(parent, bg='#34495E', relief='ridge', bd=2)
        form_frame.pack(fill='x', pady=20, padx=10)

        # Usuario
        tk.Label(form_frame, text="👤 Usuario:", font=('Arial', 11, 'bold'),
                fg='#ECF0F1', bg='#34495E').grid(row=0, column=0, sticky='w', padx=15, pady=(20, 10))

        self.entry_usuario = tk.Entry(form_frame, font=('Arial', 11), width=20,
                                    bg='#ECF0F1', fg='#2C3E50')
        self.entry_usuario.grid(row=0, column=1, padx=15, pady=(20, 10))
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())

        # Contraseña
        tk.Label(form_frame, text="🔒 Contraseña:", font=('Arial', 11, 'bold'),
                fg='#ECF0F1', bg='#34495E').grid(row=1, column=0, sticky='w', padx=15, pady=10)

        self.entry_password = tk.Entry(form_frame, font=('Arial', 11), width=20, show='•',
                                     bg='#ECF0F1', fg='#2C3E50')
        self.entry_password.grid(row=1, column=1, padx=15, pady=10)
        self.entry_password.bind('<Return>', lambda e: self.verificar_login())

        # Botón mostrar/ocultar contraseña
        self.btn_toggle_pass = tk.Button(form_frame, text="👁️", font=('Arial', 9),
                                       command=self.toggle_password, bg='#3498DB', fg='white',
                                       width=3, relief='flat')
        self.btn_toggle_pass.grid(row=1, column=2, padx=(5, 15), pady=10)

        # Botones
        self.crear_botones_login(form_frame)
        # Información de sesión
        self.crear_info_sesion(parent)

    def crear_botones_login(self, parent):
        btn_frame = tk.Frame(parent, bg='#34495E')
        btn_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.btn_login = tk.Button(btn_frame, text="🚀 INICIAR SESIÓN", font=('Arial', 12, 'bold'),
                                 command=self.verificar_login, bg='#27AE60', fg='white',
                                 width=15, height=1, relief='flat')
        self.btn_login.pack(pady=5)

        tk.Button(btn_frame, text="🔄 Limpiar", font=('Arial', 9), command=self.limpiar_formulario,
                 bg='#E74C3C', fg='white', relief='flat').pack(pady=5)

    def crear_info_sesion(self, parent):
        self.info_frame = tk.Frame(parent, bg='#2C3E50')
        self.info_frame.pack(fill='x', pady=10)

        self.lbl_info = tk.Label(self.info_frame, text="", font=('Arial', 9),
                               bg='#2C3E50', fg='#BDC3C7')
        self.lbl_info.pack()

        # Estado del sistema
        estado_frame = tk.Frame(parent, bg='#2C3E50')
        estado_frame.pack(fill='x', pady=5)

        self.lbl_estado = tk.Label(estado_frame, text="● Sistema listo", font=('Arial', 8),
                                 bg='#2C3E50', fg='#27AE60')
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
        password_hash = self.hash_password(password)
        
        if user_data['password'] != password_hash:
            self.mostrar_error("Contraseña incorrecta")
            return

        if user_data['estado'] != 'Activo':
            self.mostrar_error("Usuario inactivo. Contacte al administrador.")
            return

        # Login exitoso
        self.login_exitoso(usuario, user_data['rol'])

    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error con animación"""
        self.lbl_estado.config(text=f"⚠️ {mensaje}", fg='#E74C3C')
        original_bg = self.btn_login.cget('bg')
        self.btn_login.config(bg='#E74C3C')
        self.login_window.after(300, lambda: self.btn_login.config(bg=original_bg))

    def login_exitoso(self, usuario, rol):
        """Procedimiento de login exitoso"""
        self.lbl_estado.config(text=f"✅ ¡Acceso concedido! Rol: {rol}", fg='#27AE60')
        self.btn_login.config(state='disabled', text="⏳ CARGANDO...")

        descripcion = self.sistema_permisos.obtener_descripcion_rol(rol)
        self.lbl_info.config(text=f"Rol: {rol} - {descripcion}")

        def animar_exito():
            colores = ['#27AE60', '#2ECC71', '#27AE60']
            for color in colores:
                self.btn_login.config(bg=color)
                self.login_window.update()
                time.sleep(0.2)

            # Guardar información de sesión
            global USUARIO_ACTUAL, ROL_ACTUAL, SISTEMA_PERMISOS
            USUARIO_ACTUAL = usuario
            ROL_ACTUAL = rol
            SISTEMA_PERMISOS = self.sistema_permisos

            # Cerrar ventana de login y abrir sistema principal
            self.login_window.after(1000, self.iniciar_sistema_principal)

        threading.Thread(target=animar_exito, daemon=True).start()

    def iniciar_sistema_principal(self):
        """Iniciar el sistema principal"""
        self.login_window.destroy()
        from main import mostrar_ventana_principal
        mostrar_ventana_principal()

    def salir_sistema(self):
        """Salir completamente del sistema"""
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir del sistema?"):
            self.login_window.quit()
            self.login_window.destroy()
