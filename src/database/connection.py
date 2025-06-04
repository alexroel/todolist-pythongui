import sqlite3
import os

DB_NAME = "todolist.db"
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), DB_NAME)

def get_connection():
    """Devuelve una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

def init_database():
    """Crea las tablas si no existen e inserta categorías iniciales."""
    conn = get_connection()
    if conn is None:
        print("No se pudo establecer conexión con la base de datos.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        """)
        # Insertar categorías iniciales si no existen
        categorias_iniciales = ["Mi Día", "Importante"]
        for nombre in categorias_iniciales:
            cursor.execute(
                "INSERT OR IGNORE INTO category (name) VALUES (?)", (nombre,)
            )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        conn.close()