from plant import Plant
from task import Task
# user class for frontend
class User:
    def __init__(self, username: str):
        self.username = username
        self.plant = None
        self.tasks = []
