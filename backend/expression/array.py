from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol

class Array(Instruction):
    def __init__(self, list_expression, line, column):
        self.list_expression = list_expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        arrVal = []
        for exp in self.list_expression:
            indexExp = exp.execute(ast, env)
            arrVal.append(indexExp)
        return Symbol(symbol_type=None, value=arrVal, data_type=ExpressionType.ARRAY, environment=env, line=self.line, column=self.column)