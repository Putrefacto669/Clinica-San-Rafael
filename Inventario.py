# inventario.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
from database import run_query, run_non_query
from permisos import verificar_permiso, mostrar_error_permiso
from config import USUARIO_ACTUAL

# Variables globales para los widgets
tree_inv = None
entry_nombre = None
entry_stock = None
fecha_vencimiento = None
entry_buscar = None
btn_agregar = None

def crear_pestana_inventario(notebook):
    """Crear la pestaña de inventario"""
    global tree_inv, entry_nombre, entry_stock, fecha_vencimiento, entry_buscar, btn_agregar
    
    frame_inv = ttk.Frame(notebook)
    notebook.add(frame_inv, text="📦 Inventario")
    
    # Frame de controles
    frame_controles_inv = ttk.Frame(frame_inv)
    frame_controles_inv.pack(fill="x", padx=5, pady=5)
    
    # Frame de formulario
    frame_form_inv = ttk.Frame(frame_inv)
    frame_form_inv.pack(fill="x", padx=5, pady=5)
    
    # Treeview
    global tree_inv
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
    
    # Controles de inventario
    ttk.Label(frame_controles_inv, text="Buscar producto:").grid(row=0, column=0, padx=5, pady=5)
    entry_buscar = ttk.Entry(frame_controles_inv, width=30)
    entry_buscar.grid(row=0, column=1, padx=5, pady=5)
    entry_buscar.bind('<Return>', lambda e: buscar_producto())
    
    ttk.Button(frame_controles_inv, text="🔍 Buscar", command=buscar_producto).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(frame_controles_inv, text="🔄 Actualizar", command=cargar_inventario).grid(row=0, column=3, padx=5, pady=5)
    
    # Botones de acción
    btn_agregar = ttk.Button(frame_form_inv, text="➕ Agregar", command=agregar_producto_seguro)
    btn_agregar.grid(row=0, column=6, padx=5, pady=2)
    
    ttk.Button(frame_form_inv, text="✏️ Editar", command=editar_producto_seguro).grid(row=0, column=7, padx=5, pady=2)
    ttk.Button(frame_form_inv, text="🗑️ Eliminar", command=eliminar_producto_seguro).grid(row=0, column=8, padx=5, pady=2)
    
    # Cargar datos iniciales
    cargar_inventario()
    
    return frame_inv

def cargar_inventario():
    """Cargar datos del inventario"""
    if tree_inv:
        try:
            tree_inv.delete(*tree_inv.get_children())
            rows = run_query("SELECT Id, Nombre, Stock, FechaVencimiento FROM Productos ORDER BY Nombre")
            for r in rows:
                fecha_formateada = formatear_fecha(r[3])
                tree_inv.insert("", "end", values=(int(r[0]), r[1], r[2], fecha_formateada))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el inventario:\n{str(e)}")

def buscar_producto():
    """Buscar productos por nombre"""
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
    """Limpiar formulario de inventario"""
    entry_nombre.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    fecha_vencimiento.set_date(datetime.date.today())

def cancelar_edicion():
    """Cancelar edición y volver al modo normal"""
    limpiar_formulario_inv()
    btn_agregar.config(state="normal")
    btn_agregar.config(text="➕ Agregar", command=agregar_producto_seguro)

# FUNCIONES CON CONTROL DE PERMISOS
def agregar_producto_seguro():
    """Agregar producto con verificación de permisos"""
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
    """Editar producto con verificación de permisos"""
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

        # Llenar formulario con datos actuales
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, valores[2])

        # Cambiar botón a modo edición
        btn_agregar.config(state="disabled")
        btn_agregar.config(text="💾 Guardar", command=lambda: actualizar_producto_seguro(valores[0]))

        # Agregar botón cancelar si no existe
        if not hasattr(editar_producto_seguro, 'btn_cancelar'):
            editar_producto_seguro.btn_cancelar = ttk.Button(frame_form_inv, text="❌ Cancelar", command=cancelar_edicion)
            editar_producto_seguro.btn_cancelar.grid(row=0, column=9, padx=5, pady=2)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el producto:\n{str(e)}")

def eliminar_producto_seguro():
    """Eliminar producto con verificación de permisos"""
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
                registrar_movimiento_seguro(nombre_producto, 'BAJA', stock_producto)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{str(e)}")

def actualizar_producto_seguro(id_producto):
    """Actualizar producto en base de datos"""
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
    """Registrar movimiento en el historial"""
    try:
        fecha_actual = datetime.date.today()
        run_non_query("INSERT INTO Movimientos (Producto, Tipo, Cantidad, Usuario, Fecha) VALUES (?, ?, ?, ?, ?)",
                     (producto, tipo, cantidad, USUARIO_ACTUAL, fecha_actual))
    except Exception as e:
        print(f"Error al registrar movimiento: {str(e)}")

def formatear_fecha(fecha):
    """Formatear fecha para mostrar"""
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
        return "Fecha inválida"
