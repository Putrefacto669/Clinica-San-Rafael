# database.py
import pyodbc
import mysql.connector
from config import get_db_connection_string, get_mysql_config
import tkinter.messagebox as messagebox

def run_query(query, params=()):
    """Ejecutar consultas en SQL Server"""
    conn = None
    try:
        conn = pyodbc.connect(get_db_connection_string())
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except pyodbc.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo ejecutar la consulta:\n{str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def run_non_query(query, params=()):
    """Ejecutar operaciones sin retorno en SQL Server"""
    conn = None
    try:
        conn = pyodbc.connect(get_db_connection_string())
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except pyodbc.Error as e:
        error_msg = f"No se pudo ejecutar la operación:\n{str(e)}"
        messagebox.showerror("Error de Base de Datos", error_msg)
        return False
    finally:
        if conn:
            conn.close()

def run_mysql_query(query, params=()):
    """Ejecutar consultas en MySQL"""
    conn = None
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        print(f"Error MySQL: {e}")
        return []
    finally:
        if conn:
            conn.close()

def run_mysql_non_query(query, params=()):
    """Ejecutar operaciones sin retorno en MySQL"""
    conn = None
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Error MySQL: {e}")
        return False
    finally:
        if conn:
            conn.close()
