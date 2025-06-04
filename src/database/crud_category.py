from database.connection import get_connection
from models.category import Category

def create_category(category: Category):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (name) VALUES (?)", (category.name,))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al crear la categoría: {e}")
        return None
    finally:
        conn.close()

def get_all_categories():
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM category")
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            categories.append(Category(id=row[0], name=row[1]))
        return categories
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
        return []
    finally:
        conn.close()

def get_category_by_id(category_id: int):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM category WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        if row:
            return Category(id=row[0], name=row[1])
        return None
    except Exception as e:
        print(f"Error al obtener la categoría: {e}")
        return None
    finally:
        conn.close()

def update_category(category: Category):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE category SET name = ? WHERE id = ?", (category.name, category.id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar la categoría: {e}")
        return False
    finally:
        conn.close()

def delete_category(category_id: int):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE id = ?", (category_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar la categoría: {e}")
        return False
    finally:
        conn.close()