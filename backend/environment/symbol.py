class Symbol:
    def __init__(self, symbol_type, id, data_type, position, line, column):
        self.symbol_type = symbol_type
        self.id = id
        self.data_type = data_type
        self.position = position
        self.line = line
        self.column = column