class Symbol:
    def __init__(self, symbol_type, value, data_type, environment, line, column):
        self.symbol_type = symbol_type
        self.value = value
        self.data_type = data_type
        self.environment = environment
        self.line = line
        self.column = column