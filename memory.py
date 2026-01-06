# engine/memory.py
class Memory:
    def __init__(self):
        self.value = 0.0

    def add(self, x):
        self.value += x

    def subtract(self, x):
        self.value -= x

    def recall(self):
        return self.value

    def clear(self):
        self.value = 0.0
