from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value

class Array(Instruction):
    def __init__(self, list_expression, line, column):
        self.list_expression = list_expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        newArr = []
        for var in self.list_expression:
            value = var.execute(ast, env, gen)
            newArr.append(value.value)
        return  Value(newArr, False, ExpressionType.ARRAY, [], [], [])