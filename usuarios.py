# usuarios.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database import run_query, run_non_query
from permisos import verificar_permiso, mostrar_error_permiso

# Variables globales
tree_usr = None
entry_nombre_usr = None
combo_rol = None

def crear_pestana_usuarios(notebook):
    """Crear la pestaña de usuarios"""
    global tree_usr, entry_nombre_usr, combo_rol
    
    frame_usr = ttk.Frame(notebook)
    notebook.add(frame_usr, text="👥 Usuarios")
    
    # Frame de formulario
    frame_form_usr = ttk.Frame(frame_usr)
    frame_form_usr.pack(fill="x", padx=5, pady=5)
    
    # Frame de controles
    frame_controles_usr = ttk.Frame(frame_usr)
    frame_controles_usr.pack(fill="x", padx=5, pady=5)
    
    # Treeview
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
    
    # Botones de control
    ttk.Button(frame_controles_usr, text="🔄 Actualizar", command=cargar_usuarios).pack(side="left", padx=5)
    ttk.Button(frame_controles_usr, text="➕ Agregar", command=agregar_usuario_seguro).pack(side="left", padx=5)
    ttk.Button(frame_controles_usr, text="🔄 Activar/Inactivar", command=cambiar_estado_seguro).pack(side="left", padx=5)
    ttk.Button(frame_controles_usr, text="🗑️ Eliminar", command=eliminar_usuario_seguro).pack(side="left", padx=5)
    
    # Cargar usuarios iniciales
    cargar_usuarios()
    
    return frame_usr

def cargar_usuarios():
    """Cargar lista de usuarios"""
    try:
        tree_usr.delete(*tree_usr.get_children())
        rows = run_query("SELECT Id, Nombre, Rol, Estado FROM Usuarios ORDER BY Nombre")
        for r in rows:
            tree_usr.insert("", "end", values=(int(r[0]), r[1], r[2], r[3]))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{str(e)}")

def limpiar_formulario_usr():
    """Limpiar formulario de usuarios"""
    entry_nombre_usr.delete(0, tk.END)
    combo_rol.set("")

def hash_password(password):
    """Encriptar contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# FUNCIONES CON CONTROL DE PERMISOS
def agregar_usuario_seguro():
    """Agregar usuario con verificación de permisos"""
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
        password_hash = hash_password(nombre)

        if run_non_query("INSERT INTO Usuarios (Nombre, Password, Rol, Estado) VALUES (?, ?, ?, 'Activo')",
                        (nombre, password_hash, rol)):
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' agregado correctamente\nContraseña inicial: mismo que el usuario")
            limpiar_formulario_usr()
            cargar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el usuario:\n{str(e)}")

def eliminar_usuario_seguro():
    """Eliminar usuario con verificación de permisos"""
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
    """Cambiar estado de usuario con verificación de permisos"""
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
