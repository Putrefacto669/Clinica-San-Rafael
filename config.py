# config.py
import datetime
from datetime import datetime as dt, timedelta, date

# Variables globales para la sesión
USUARIO_ACTUAL = None
ROL_ACTUAL = None
SISTEMA_PERMISOS = None
modulo_reportes = None
frame_grafica_actual = None
theme_manager = None

# Configuración de base de datos SQL Server
def get_db_connection_string():
    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=DESKTOP-9U57LTA;"
        "DATABASE=ClinicaDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

# Configuración de base de datos MySQL para correos
def get_mysql_config():
    return {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'clinica_correos'
    }

# Configuración de correo
def get_email_config():
    return {
        'smtp_server': 'smtp.gmail.com',
        'port': 587,
        'email': 'lopezurbina2018@gmail.com',
        'password': 'uynt mkho qwbf xtyp'
    }
