# permisos.py
class SistemaPermisos:
    def __init__(self):
        self.permisos_por_rol = {
            'Administrador': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'usuarios', 'reportes', 'configuracion', 'citas'],
                'acciones': ['crear', 'leer', 'actualizar', 'eliminar', 'exportar', 'configurar', 'visualizar'],
                'descripcion': 'Acceso completo al sistema incluyendo reportes'
            },
            'Médico': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'reportes', 'citas'],
                'acciones': ['crear', 'leer', 'actualizar', 'exportar', 'visualizar'],
                'descripcion': 'Acceso a consultas, gestión de citas y reportes'
            },
            'Enfermero': {
                'modulos': ['inventario', 'alertas', 'movimientos', 'citas', 'reportes'],
                'acciones': ['crear', 'leer', 'actualizar', 'exportar', 'visualizar'],
                'descripcion': 'Gestión de medicamentos, citas y reportes básicos'
            },
            'Recepcionista': {
                'modulos': ['inventario', 'movimientos', 'citas', 'reportes'],
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

# Funciones de control de acceso
def verificar_permiso(modulo, accion=None):
    """Verificar si el usuario actual tiene permiso"""
    from config import ROL_ACTUAL, SISTEMA_PERMISOS
    if not ROL_ACTUAL or not SISTEMA_PERMISOS:
        return False
    return SISTEMA_PERMISOS.tiene_permiso(ROL_ACTUAL, modulo, accion)

def mostrar_error_permiso():
    """Mostrar mensaje de error de permisos"""
    from config import USUARIO_ACTUAL, ROL_ACTUAL
    import tkinter.messagebox as messagebox
    
    messagebox.showerror(
        "Acceso Denegado",
        "❌ No tiene permisos para realizar esta acción.\n\n"
        f"Usuario: {USUARIO_ACTUAL}\n"
        f"Rol: {ROL_ACTUAL}\n\n"
        "Contacte al administrador del sistema."
    )
