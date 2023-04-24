def scale(num):
    return num * 1.2

class Post():
    def __init__(self, title = "null", owner = "default") -> None:
        self.title = title
        self.content = []
        self.owner = owner
        self.status = 0

    def add_content(self, text: str):
        self.content = text

    def change_status(self, stauts: int):
        self.status += stauts