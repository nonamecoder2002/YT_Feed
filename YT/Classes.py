from datetime import datetime


class Key:
    def __init__(self, value: str):
        self.key_value = value
        self.points = 10000
        self.activation_date = datetime.now()
        self.valid = True

    def use(self):
        if self.activation_date.day != datetime.now().day:
            self.points = 1000

        if self.points <= 5:

            self.valid = False
            return None

        else:
            self.points = self.points - 2

    def is_valid(self):
        return self.valid
