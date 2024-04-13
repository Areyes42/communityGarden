from dtype.plant import Plant
from dtype.task import Task
# user class for frontend
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.plant_id = None
        self.tasks = []
