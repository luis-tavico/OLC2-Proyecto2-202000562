from abstract.instruction import Instruction

class Function(Instruction):
    def __init__(self, id, params, type, block, line, column):
        self.id = id
        self.params = params
        self.type = type
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None