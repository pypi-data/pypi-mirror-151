

class StatusException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f'code: {self.code}, msg: {self.msg}'
