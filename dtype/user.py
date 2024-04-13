from plant import Plant
from task import Task
# user class for frontend
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.plant = None
        self.tasks = []
