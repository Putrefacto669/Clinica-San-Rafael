# alertas.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
from database import run_query, run_non_query
from permisos import verificar_permiso, mostrar_error_permiso
from config import USUARIO_ACTUAL

# Variables globales
tree_alert = None

def crear_pestana_alertas(notebook):
    """Crear la pestaña de alertas"""
    global tree_alert
    
    frame_alert = ttk.Frame(notebook)
    notebook.add(frame_alert, text="⚠️ Alertas")
    
    # Frame de controles
    frame_controles_alert = ttk.Frame(frame_alert)
    frame_controles_alert.pack(fill="x", padx=5, pady=5)
    
    # Treeview
    tree_alert = ttk.Treeview(frame_alert, columns=("ID", "Nombre", "Stock", "Vencimiento", "Alerta", "Gravedad"), show="headings")
    for col in ("ID", "Nombre", "Stock", "Vencimiento", "Alerta", "Gravedad"):
        tree_alert.heading(col, text=col)
        tree_alert.column(col, width=120)
    tree_alert.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Configurar colores de alertas
    tree_alert.tag_configure("ALTA", background="#ffcccc")  # Rojo claro
    tree_alert.tag_configure("MEDIA", background="#fff0cc") # Amarillo claro  
    tree_alert.tag_configure("BAJA", background="#e6f7ff")  # Azul claro
    
    # Botones de control
    ttk.Button(frame_controles_alert, text="🔄 Ver Alertas", command=cargar_alertas).pack(side="left", padx=5)
    ttk.Button(frame_controles_alert, text="📦 Reponer Stock", command=reponer_stock_seguro).pack(side="left", padx=5)
    ttk.Button(frame_controles_alert, text="💾 Exportar Alertas", command=exportar_alertas_seguro).pack(side="left", padx=5)
    
    # Cargar alertas iniciales
    cargar_alertas()
    
    return frame_alert

def cargar_alertas():
    """Cargar y mostrar alertas del sistema"""
    try:
        tree_alert.delete(*tree_alert.get_children())
        hoy = datetime.date.today()
        rows = run_query("SELECT Id, Nombre, Stock, FechaVencimiento FROM Productos")

        alertas_encontradas = False

        for r in rows:
            id_, nombre, stock, fecha = r
            alertas = []
            gravedad = "BAJA"

            # Verificar stock bajo
            if stock < 5:
                alertas.append(f"STOCK CRÍTICO: {stock} unidades")
                gravedad = "ALTA"
            elif stock < 10:
                alertas.append(f"Stock bajo: {stock} unidades")
                gravedad = "MEDIA"

            # Verificar vencimientos
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

            # Si hay alertas, mostrar en treeview
            if alertas:
                alertas_encontradas = True
                fecha_str = formatear_fecha(fecha_dt)
                
                item_id = tree_alert.insert("", "end", values=(
                    id_, nombre, stock, fecha_str, ", ".join(alertas), gravedad
                ), tags=(gravedad,))

        if not alertas_encontradas:
            messagebox.showinfo("Alertas", "✅ No hay alertas en este momento. Todo está en orden.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las alertas:\n{str(e)}")

def reponer_stock_seguro():
    """Reponer stock con verificación de permisos"""
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

        # Ventana para reponer stock
        ventana_reponer = tk.Toplevel()
        ventana_reponer.title("Reponer Stock")
        ventana_reponer.geometry("300x150")
        ventana_reponer.transient(None)
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
                    from inventario import registrar_movimiento_seguro
                    registrar_movimiento_seguro(valores[1], 'REPOSICIÓN', cantidad)
                    messagebox.showinfo("Éxito", f"Stock repuesto. Nuevo stock: {nuevo_stock}")
                    ventana_reponer.destroy()
                    cargar_alertas()
                    # Actualizar inventario si está cargado
                    try:
                        from inventario import cargar_inventario
                        cargar_inventario()
                    except:
                        pass
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido")

        ttk.Button(ventana_reponer, text="✅ Confirmar", command=confirmar_reposicion).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reponer el stock:\n{str(e)}")

def exportar_alertas_seguro():
    """Exportar alertas con verificación de permisos"""
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
