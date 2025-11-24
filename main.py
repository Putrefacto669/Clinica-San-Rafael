# main.py
import tkinter as tk
from tkinter import ttk
import time
from config import USUARIO_ACTUAL, ROL_ACTUAL, SISTEMA_PERMISOS
from theme_manager import ThemeManager, initialize_theme_system
from database import run_query
from permisos import verificar_permiso, configurar_interfaz_por_rol, configurar_botones_por_permisos
from correos import abrir_sistema_correos
from reportes import crear_pestana_reportes
from citas import crear_pestana_citas
from asistente_voz import abrir_asistente

# Variables globales
root = None
notebook = None

def crear_ventana_principal():
    """Crear la ventana principal del sistema"""
    global root, notebook
    
    root = tk.Tk()
    root.title("Clínica Popular San Rafael - Sistema de Gestión")
    root.geometry("1000x650")
    
    # Inicializar sistema de temas
    initialize_theme_system(root)
    
    # Configurar estilos
    configurar_estilos()
    
    # Crear notebook (pestañas)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Crear pestañas según permisos
    crear_pestanas_principales()
    
    return root

def configurar_estilos():
    """Configurar estilos de la interfaz"""
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

def crear_pestanas_principales():
    """Crear las pestañas principales según los permisos"""
    # Pestaña de Inventario (si tiene permisos)
    if verificar_permiso('inventario', 'leer'):
        from inventario import crear_pestana_inventario
        crear_pestana_inventario(notebook)
    
    # Pestaña de Alertas (si tiene permisos)
    if verificar_permiso('alertas', 'leer'):
        from alertas import crear_pestana_alertas
        crear_pestana_alertas(notebook)
    
    # Pestaña de Movimientos (si tiene permisos)
    if verificar_permiso('movimientos', 'leer'):
        from movimientos import crear_pestana_movimientos
        crear_pestana_movimientos(notebook)
    
    # Pestaña de Usuarios (si tiene permisos)
    if verificar_permiso('usuarios', 'leer'):
        from usuarios import crear_pestana_usuarios
        crear_pestana_usuarios(notebook)
    
    # Pestaña de Citas (si tiene permisos)
    if verificar_permiso('citas', 'leer'):
        crear_pestana_citas(notebook)
    
    # Pestaña de Reportes (si tiene permisos)
    if verificar_permiso('reportes', 'visualizar'):
        crear_pestana_reportes(notebook)

def inicializar_aplicacion():
    """Cargar datos iniciales al abrir la aplicación"""
    # Cargar datos de módulos existentes
    if verificar_permiso('inventario', 'leer'):
        from inventario import cargar_inventario
        cargar_inventario()
    
    if verificar_permiso('usuarios', 'leer'):
        from usuarios import cargar_usuarios
        cargar_usuarios()
    
    if verificar_permiso('movimientos', 'leer'):
        from movimientos import cargar_movimientos
        cargar_movimientos()
    
    if verificar_permiso('alertas', 'leer'):
        from alertas import cargar_alertas
        cargar_alertas()
    
    # Configurar interfaz según rol
    configurar_interfaz_por_rol(notebook)
    configurar_botones_por_permisos()
    
    # Crear barra de estado
    crear_barra_estado()
    
    # Añadir botón flotante del asistente
    if not hasattr(root, "btn_asistente_creado"):
        btn_asistente = tk.Button(root, text="💬 Asistente", command=abrir_asistente, 
                                bg="#0A64A4", fg="white", relief="flat", font=("Arial", 10, "bold"),
                                cursor="hand2")
        btn_asistente.place(relx=0.93, rely=0.92, anchor="center")
        root.btn_asistente_creado = True

def crear_barra_estado():
    """Crea una barra de estado en la ventana principal"""
    barra_estado = tk.Frame(root, bg="#0A64A4", height=25)
    barra_estado.pack(side="bottom", fill="x")
    tk.Label(barra_estado, text=f"Usuario: {USUARIO_ACTUAL} | Rol: {ROL_ACTUAL}",
             bg="#0A64A4", fg="white", font=("Segoe UI", 9)).pack(side="left", padx=10)

def mostrar_ventana_principal():
    """Mostrar la ventana principal con efecto de fade in"""
    root.deiconify()
    
    # Efecto de fade in
    alpha = 0.0
    while alpha < 1.0:
        root.attributes('-alpha', alpha)
        root.update()
        alpha += 0.05
        time.sleep(0.01)
    root.attributes('-alpha', 1.0)
    
    # Inicializar aplicación
    inicializar_aplicacion()

if __name__ == "__main__":
    # Iniciar con el sistema de login
    from login import SistemaLogin
    app_login = SistemaLogin()
    app_login.login_window.mainloop()
