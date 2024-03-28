from abstract.instruction import Instruction
from environment.type import ExpressionType
from expression.primitive import Primitive
from environment.symbol import Symbol
from errors.error import Error

class Declaration(Instruction):
    def __init__(self, symbol_type, id, data_type, expression, line, column):
        self.symbol_type = symbol_type
        self.id = id
        self.data_type = data_type
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        if self.expression == None:
            if self.data_type == ExpressionType.NUMBER:
                self.expression = Primitive(int(0), ExpressionType.NUMBER, 0, 0)
            elif self.data_type == ExpressionType.FLOAT:
                self.expression = Primitive(float(0), ExpressionType.FLOAT, 0, 0)
            elif self.data_type == ExpressionType.STRING:
                self.expression = Primitive(str(""), ExpressionType.STRING, 0, 0)
            elif self.data_type == ExpressionType.CHAR:
                self.expression = Primitive(str(""), ExpressionType.CHAR, 0, 0)
            elif self.data_type == ExpressionType.BOOLEAN:
                self.expression = Primitive(bool(True), ExpressionType.BOOLEAN, 0, 0)
        result = self.expression.execute(ast, env)
        if self.data_type == None:
            self.data_type = result.data_type
        if result.data_type != self.data_type:
            if result.data_type == ExpressionType.NUMBER and self.data_type == ExpressionType.FLOAT:
                result.value = float(result.value)
            else: 
                ast.setErrors(Error("Semantico", "Los tipos de datos son incorrectos", "Declaration", self.line, self.column))
                return
        symbol = Symbol(symbol_type=self.symbol_type, value=result.value, data_type=result.data_type, environment=env, line=self.line, column=self.column)
        env.saveSymbol(ast, self.id, symbol)