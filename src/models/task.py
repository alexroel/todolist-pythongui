class Task:
    def __init__(self, id: int, title: str, completed: bool, category_id: int):
        self.id = id
        self.title = title
        self.completed = completed
        self.category_id = category_id

    def __repr__(self):
        return (f"Task(id={self.id}, title='{self.title}', "
                f"completed={self.completed}, category_id={self.category_id})")