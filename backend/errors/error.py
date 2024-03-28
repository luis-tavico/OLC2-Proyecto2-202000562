class Error():
    def __init__(self, type, description, ambit, line, column):
        self.type = type
        self.description = description
        self.ambit = ambit
        self.line = line
        self.column = column