from abstract.instruction import Instruction

class Interface(Instruction):
    def __init__(self, id, attributes, line, column):
        self.id = id
        self.attributes = attributes
        self.line = line
        self.column = column
    
    def execute(self, ast, env):
        env.saveStruct(ast, self.id, self.attributes)