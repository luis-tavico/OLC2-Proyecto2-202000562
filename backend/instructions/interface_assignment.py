from abstract.instruction import Instruction

class Interfaceassignment(Instruction):
    def __init__(self, access_interface, expression, line, column):
        self.access_interface = access_interface
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        env_interface = self.access_interface.instance.execute(ast, env)
        struct = env_interface.symbols_table
        attribute = self.access_interface.attribute
        struct[attribute] = self.expression.execute(ast, env)
        return None