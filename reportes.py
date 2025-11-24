# reportes.py
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from matplotlib.figure import Figure
import pandas as pd
from database import run_query

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
        """Crear gráfica de distribución de stock"""
        try:
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

def crear_pestana_reportes(notebook):
    """Crear la pestaña de reportes gráficos"""
    try:
        from permisos import verificar_permiso
        from config import ROL_ACTUAL, SISTEMA_PERMISOS
        
        # Verificar permisos
        if not verificar_permiso('reportes', 'visualizar'):
            print(f"❌ PERMISO DENEGADO: Usuario sin permisos para reportes")
            return None
            
        # Crear frame de reportes
        frame_reportes = ttk.Frame(notebook)
        notebook.add(frame_reportes, text="📈 Reportes")
        
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
            ("📈 Tendencia", "tendencia"),
            ("🏆 Top Productos", "top_productos")
        ]
        
        for i, (texto, tipo) in enumerate(reportes_disponibles):
            btn = ttk.Button(frame_controles_reportes, text=texto,
                            command=lambda t=tipo: mostrar_reporte(t, frame_grafica, modulo_reportes))
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        # Frame para gráficas
        frame_grafica = ttk.Frame(frame_reportes)
        frame_grafica.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mostrar reporte inicial
        frame_reportes.after(500, lambda: mostrar_reporte("stock", frame_grafica, modulo_reportes))
        
        return frame_reportes
        
    except Exception as e:
        print(f"❌ ERROR creando pestaña reportes: {e}")
        return None

def mostrar_reporte(tipo_reporte, frame_grafica_actual, modulo_reportes):
    """Mostrar el reporte seleccionado"""
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
        elif tipo_reporte == "tendencia":
            widget_grafica = modulo_reportes.crear_grafica_tendencia_mensual(frame_grafica_actual)
        elif tipo_reporte == "top_productos":
            widget_grafica = modulo_reportes.crear_grafica_top_productos(frame_grafica_actual)
        
        # Remover loading y mostrar gráfica
        lbl_loading.destroy()
        if widget_grafica:
            widget_grafica.pack(fill="both", expand=True)
        else:
            lbl_error = tk.Label(frame_grafica_actual, text="❌ No se pudo generar el reporte", 
                               font=('Arial', 12), bg='#E3F2FD', fg='red')
            lbl_error.pack(expand=True)
            
    except Exception as e:
        print(f"❌ Error mostrando reporte {tipo_reporte}: {e}")
        for widget in frame_grafica_actual.winfo_children():
            widget.destroy()
        
        lbl_error = tk.Label(frame_grafica_actual, 
                           text=f"❌ Error generando reporte:\n{str(e)}", 
                           font=('Arial', 10), bg='#E3F2FD', fg='red', justify='left')
        lbl_error.pack(expand=True)
