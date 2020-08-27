import logging

from datetime import datetime


logger = logging.getLogger(__name__)

logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(levelname)s-->%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs.log', mode='a')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
            logger.warning('Api_key will expire soon!!!')
            self.valid = False
            return None

        else:
            self.points = self.points - 2

    def is_valid(self):
        return self.valid
