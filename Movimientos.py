# movimientos.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import os
from database import run_query, run_non_query
from permisos import verificar_permiso, mostrar_error_permiso

# Variables globales
tree_mov = None
fecha_inicio = None
fecha_fin = None
combo_tipo = None
entry_producto_mov = None

def crear_pestana_movimientos(notebook):
    """Crear la pestaña de movimientos"""
    global tree_mov, fecha_inicio, fecha_fin, combo_tipo, entry_producto_mov
    
    frame_mov = ttk.Frame(notebook)
    notebook.add(frame_mov, text="📊 Movimientos")
    
    # Frame de filtros
    frame_filtros_mov = ttk.Frame(frame_mov)
    frame_filtros_mov.pack(fill="x", padx=5, pady=5)
    
    # Frame de controles
    frame_controles_mov = ttk.Frame(frame_mov)
    frame_controles_mov.pack(fill="x", padx=5, pady=5)
    
    # Treeview
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
    
    # Configurar fechas por defecto (últimos 30 días)
    fecha_inicio.set_date(datetime.date.today() - datetime.timedelta(days=30))
    fecha_fin.set_date(datetime.date.today())
    
    # Botones de control
    ttk.Button(frame_controles_mov, text="🔄 Actualizar", command=cargar_movimientos).pack(side="left", padx=5)
    ttk.Button(frame_controles_mov, text="🔍 Filtrar", command=filtrar_movimientos).pack(side="left", padx=5)
    ttk.Button(frame_controles_mov, text="🧹 Limpiar Filtros", command=limpiar_filtros).pack(side="left", padx=5)
    ttk.Button(frame_controles_mov, text="💾 Exportar CSV", command=exportar_movimientos_seguro).pack(side="left", padx=5)
    
    # Cargar movimientos iniciales
    cargar_movimientos()
    
    return frame_mov

def cargar_movimientos():
    """Cargar todos los movimientos"""
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
    """Filtrar movimientos según criterios"""
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
    """Limpiar todos los filtros"""
    fecha_inicio.set_date(datetime.date.today() - datetime.timedelta(days=30))
    fecha_fin.set_date(datetime.date.today())
    combo_tipo.set("")
    entry_producto_mov.delete(0, tk.END)
    cargar_movimientos()

def exportar_movimientos_seguro():
    """Exportar movimientos con verificación de permisos"""
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
