from datetime import datetime


class Key:
    def __init__(self, value: str):
        self.value = value
        self.valid = True

    def is_valid(self):
        return self.valid

    def expire(self):
        self.valid = False

    def mk_valid(self):
        self.valid = True
