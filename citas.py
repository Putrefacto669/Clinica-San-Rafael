# citas.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
import os
from database import run_query, run_non_query
from permisos import verificar_permiso, mostrar_error_permiso
from config import USUARIO_ACTUAL

# Funciones de citas flexibles
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
    h0 = datetime.strptime(hora_inicio, "%H:%M")
    hf = datetime.strptime(hora_fin, "%H:%M")
    cur = h0
    while cur <= hf:
        horarios.append(cur.strftime("%H:%M"))
        cur += timedelta(minutes=intervalo_minutos)
    return horarios

def limpiar_formulario_cita(entry_paciente, entry_doctor, combo_especialidad, date_cita, combo_hora, entry_observaciones):
    """Limpiar formulario de citas"""
    entry_paciente.delete(0, tk.END)
    entry_doctor.delete(0, tk.END)
    combo_especialidad.set("Medicina General")
    date_cita.set_date(date.today())
    combo_hora.set("08:00")
    entry_observaciones.delete(0, tk.END)

def cargar_citas_flexibles(tree_citas):
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

def agendar_cita_flexible(entry_paciente, entry_doctor, combo_especialidad, date_cita, combo_hora, entry_observaciones, tree_citas):
    """Agendar cita sin depender de IDs de base de datos"""
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

        # Validaciones básicas
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

        # Combinar fecha y hora
        try:
            fecha_hora = datetime.combine(fecha, datetime.strptime(hora, "%H:%M").time())
        except ValueError as ve:
            messagebox.showerror("Error", f"Formato de hora inválido. Use HH:MM (ej: 14:30)\nError: {ve}")
            combo_hora.focus()
            return

        # Verificar que la fecha no sea en el pasado
        if fecha_hora < datetime.now():
            messagebox.showwarning("Fecha inválida", "No se pueden agendar citas en fechas pasadas")
            date_cita.focus()
            return

        # Insertar en base de datos
        query = """
        INSERT INTO CitasFlexibles 
        (Paciente, Doctor, Especialidad, FechaCita, Observaciones, Estado, UsuarioCreacion) 
        VALUES (?, ?, ?, ?, ?, 'Pendiente', ?)
        """
        
        params = (paciente, doctor, especialidad, fecha_hora, observaciones, USUARIO_ACTUAL)
        
        if run_non_query(query, params):
            messagebox.showinfo("Éxito", f"✅ Cita agendada para {paciente} con {doctor}")
            limpiar_formulario_cita(entry_paciente, entry_doctor, combo_especialidad, date_cita, combo_hora, entry_observaciones)
            cargar_citas_flexibles(tree_citas)
        else:
            messagebox.showerror("Error", "No se pudo agendar la cita. Verifique los datos.")

    except Exception as e:
        error_msg = f"No se pudo agendar la cita:\n{str(e)}"
        messagebox.showerror("Error", error_msg)

def buscar_citas_flexibles(entry_buscar_cita, tree_citas):
    """Buscar citas flexibles"""
    try:
        texto_busqueda = entry_buscar_cita.get().strip()
        if not texto_busqueda:
            cargar_citas_flexibles(tree_citas)
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

def exportar_citas_csv(tree_citas):
    """Exportar citas a CSV"""
    try:
        filename = f"citas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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

def crear_pestana_citas(notebook):
    """Crear la pestaña de citas en el notebook principal"""
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
    btn_agendar_cita = ttk.Button(frame_form_citas, text="➕ Agendar Cita", width=15, 
                                 command=lambda: agendar_cita_flexible(entry_paciente, entry_doctor, combo_especialidad, date_cita, combo_hora, entry_observaciones, tree_citas))
    btn_agendar_cita.grid(row=3, column=1, padx=5, pady=8)

    # Controles
    ttk.Label(frame_controles_citas, text="Buscar:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
    entry_buscar_cita = ttk.Entry(frame_controles_citas, width=25)
    entry_buscar_cita.grid(row=0, column=1, padx=5, pady=4)

    ttk.Button(frame_controles_citas, text="🔍 Buscar", 
              command=lambda: buscar_citas_flexibles(entry_buscar_cita, tree_citas)).grid(row=0, column=2, padx=5, pady=4)
    ttk.Button(frame_controles_citas, text="🔄 Actualizar", 
              command=lambda: cargar_citas_flexibles(tree_citas)).grid(row=0, column=3, padx=5, pady=4)
    ttk.Button(frame_controles_citas, text="💾 Exportar CSV", 
              command=lambda: exportar_citas_csv(tree_citas)).grid(row=0, column=4, padx=5, pady=4)

    # Treeview
    tree_citas = ttk.Treeview(frame_tree_citas, columns=("ID", "Paciente", "Doctor", "Especialidad", "FechaHora", "Estado", "Observaciones"), show="headings")
    for col, width in [("ID",80), ("Paciente",220), ("Doctor",180), ("Especialidad",140), ("FechaHora",160), ("Estado",100), ("Observaciones",220)]:
        tree_citas.heading(col, text=col)
        tree_citas.column(col, width=width)
    tree_citas.pack(fill="both", expand=True)

    # Cargar citas iniciales
    crear_tabla_citas_flexibles()
    cargar_citas_flexibles(tree_citas)

    return frame_citas
