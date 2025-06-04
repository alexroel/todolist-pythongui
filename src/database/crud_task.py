from database.connection import get_connection
from models.task import Task

def create_task(title: str, category_id: int, completed: bool = False):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO task (title, completed, category_id) VALUES (?, ?, ?)",
            (title, int(completed), category_id)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error al crear la tarea: {e}")
        return None
    finally:
        conn.close()

def get_tasks_by_category(category_id: int):
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, completed, category_id FROM task WHERE category_id = ?",
            (category_id,)
        )
        rows = cursor.fetchall()
        return [Task(id=row[0], title=row[1], completed=bool(row[2]), category_id=row[3]) for row in rows]
    except Exception as e:
        print(f"Error al obtener tareas: {e}")
        return []
    finally:
        conn.close()

def update_task_completed(task_id: int, completed: bool):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE task SET completed = ? WHERE id = ?",
            (int(completed), task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar el estado de la tarea: {e}")
        return False
    finally:
        conn.close()

def delete_task(task_id: int):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar la tarea: {e}")
        return False
    finally:
        conn.close()