from abstract.instruction import Instruction

class Function(Instruction):
    def __init__(self, id, params, type, block, line, column):
        self.id = id
        self.params = params
        self.type = type
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env):
        functionData = {
            'symbol_type': "Function",
            'data_type': self.type,
            'params': self.params,
            'block': self.block,
            'environment': env,
            'line': self.line,
            'column': self.column
        }
        env.saveFunction(ast, self.id, functionData)