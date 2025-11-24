# theme_manager.py
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.theme_button = None
        self.control_frame = None

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
        """Crear botón para cambiar tema"""
        try:
            if not self.control_frame:
                self.control_frame = ttk.Frame(self.root)
                self.control_frame.pack(side=tk.TOP, fill=tk.X)

            self.theme_button = tk.Button(
                self.control_frame,
                text="🌙 Modo Oscuro",
                command=self.toggle_theme,
                bg=self.themes[self.current_theme]["button_bg"],
                fg=self.themes[self.current_theme]["button_fg"],
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            self.theme_button.pack(side=tk.RIGHT, padx=10, pady=10)
            return self.theme_button
        except Exception as e:
            print(f"❌ Error creando botón de tema: {e}")
            return None

    def toggle_theme(self):
        """Cambiar entre temas"""
        try:
            self.current_theme = "dark" if self.current_theme == "light" else "light"
            self.apply_theme()
            
            if self.theme_button:
                new_text = "🌙 Modo Oscuro" if self.current_theme == "light" else "☀️ Modo Claro"
                self.theme_button.configure(text=new_text)
        except Exception as e:
            print(f"❌ Error cambiando tema: {e}")

    def apply_theme(self):
        """Aplicar tema a todos los widgets"""
        try:
            theme = self.themes[self.current_theme]
            style = ttk.Style()
            self._configure_ttk_styles(style, theme)
            self._apply_to_all_widgets(self.root, theme)
        except Exception as e:
            print(f"❌ Error aplicando tema: {e}")

    def _configure_ttk_styles(self, style, theme):
        """Configurar estilos ttk"""
        try:
            style.configure("TFrame", background=theme["bg_primary"])
            style.configure("TLabel", background=theme["bg_primary"], foreground=theme["text_primary"])
            style.configure("TButton", background=theme["button_bg"], foreground=theme["button_fg"])
            style.map("TButton",
                      background=[('active', theme["accent_color"])],
                      foreground=[('active', theme["button_fg"])])
            
            # Treeview con letras siempre negras
            style.configure("Treeview", 
                           background=theme["treeview_bg"], 
                           foreground="black",
                           fieldbackground=theme["treeview_bg"],
                           font=("Segoe UI", 9))
            style.map("Treeview", 
                      background=[("selected", theme["treeview_selected"])],
                      foreground=[("selected", "black")])
                      
        except Exception as e:
            print(f"❌ Error configurando estilos ttk: {e}")

    def _apply_to_all_widgets(self, widget, theme):
        """Aplicar tema recursivamente a todos los widgets"""
        try:
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.configure(bg=theme["bg_primary"])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg_primary"], fg=theme["text_primary"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=theme["button_bg"], fg=theme["button_fg"], 
                               activebackground=theme["accent_color"])
            elif isinstance(widget, (tk.Entry, tk.Text, tk.Spinbox)):
                widget.configure(bg=theme["bg_secondary"], fg=theme["text_primary"], 
                               insertbackground=theme["text_primary"])
            elif isinstance(widget, scrolledtext.ScrolledText):
                widget.configure(bg=theme["bg_secondary"], fg=theme["text_primary"], 
                               insertbackground=theme["text_primary"])
            elif isinstance(widget, ttk.Treeview):
                widget.configure(background=theme["treeview_bg"], foreground="black")
                
            for child in widget.winfo_children():
                self._apply_to_all_widgets(child, theme)
        except (tk.TclError, AttributeError):
            pass

    def initialize(self):
        """Inicialización completa del sistema de temas"""
        self.apply_theme()
        return self.create_theme_button()
