from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error

dominant_table = [
    [ExpressionType.NUMBER,  ExpressionType.FLOAT, ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.FLOAT,   ExpressionType.FLOAT, ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.STRING, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
    [ExpressionType.NULL,    ExpressionType.NULL,  ExpressionType.NULL,   ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL, ExpressionType.NULL],
]

class Operation(Expression):
    def __init__(self, operationL, operator, operationR, line, column):
        self.operationL = operationL
        self.operator = operator
        self.operationR = operationR
        self.line = line
        self.column = column

    def execute(self, ast, env):
        if self.operationL != None and self.operationR != None:
            operation1 = self.operationL.execute(ast, env)
            operation2 = self.operationR.execute(ast, env)
            dominant_type = dominant_table[operation1.data_type.value][operation2.data_type.value]
            #SUMA
            if self.operator == "+":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT or dominant_type == ExpressionType.STRING:
                    return Symbol(symbol_type=None, value=operation1.value+operation2.value, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para sumar", "Operation", self.line, self.column))
            #RESTA
            elif self.operator == "-" and self.operationR != None:
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value-operation2.value, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para restar", "Operation", self.line, self.column))
            #MULTIPLICACION
            elif self.operator == "*":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value*operation2.value, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para multiplicar", "Operation", self.line, self.column))
            #DIVISION
            elif self.operator == "/":
                if operation2.value == 0:
                    ast.setErrors(Error("Semantico", "No se puede dividir por 0", "Operation", self.line, self.column))
                    return 
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value/operation2.value, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para dividir", "Operation", self.line, self.column))
            #MODULO
            elif self.operator == "%":
                if dominant_type == ExpressionType.NUMBER:
                    return Symbol(symbol_type=None, value=operation1.value%operation2.value, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para modulo", "Operation", self.line, self.column))
            #MAYOR QUE
            elif self.operator == ">":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value>operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para mayor que", "Operation", self.line, self.column))
            #MENOR QUE 
            elif self.operator == "<":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value<operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para menor que", "Operation", self.line, self.column))
            #MAYOR O IGUAL QUE
            elif self.operator == ">=":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value>=operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para mayor o igual que", "Operation", self.line, self.column))
            #MENOR O IGUAL QUE
            elif self.operator == "<=":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value<=operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para menor o igual que", "Operation", self.line, self.column))
            #IGUAL QUE
            elif self.operator == "==":
                return Symbol(symbol_type=None, value=operation1.value==operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
            #DIFERENTE QUE
            elif self.operator == "!=":
                return Symbol(symbol_type=None, value=operation1.value!=operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
            #AND
            elif self.operator == "&&":
                return Symbol(symbol_type=None, value=operation1.value and operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
            #OR
            elif self.operator == "||":
                return Symbol(symbol_type=None, value=operation1.value or operation2.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
        else:
            operation1 = self.operationL.execute(ast, env)
            dominant_type = dominant_table[operation1.data_type.value][0]
            #NEGATIVO
            if self.operator == "-":
                if dominant_type == ExpressionType.NUMBER or dominant_type == ExpressionType.FLOAT:
                    return Symbol(symbol_type=None, value=operation1.value*-1, data_type=ExpressionType.NUMBER, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para negar", "Operation", self.line, self.column))
            #NOT
            elif self.operator == "!":
                dominant_type = ExpressionType.BOOLEAN
                return Symbol(symbol_type=None, value=not operation1.value, data_type=ExpressionType.BOOLEAN, environment=env, line=self.line, column=self.column)
            #INCREASE
            elif self.operator == "++":
                if dominant_type == ExpressionType.NUMBER:
                    env.setSymbol(ast, self.operationL.id, "+=", Symbol(symbol_type=None, value=1, data_type=dominant_type, environment=env, line=self.line, column=self.column))
                    return Symbol(symbol_type=None, value=operation1.value+1, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para incrementar", "Operation", self.line, self.column))
            elif self.operator == "--":
                if dominant_type == ExpressionType.NUMBER:
                    env.setSymbol(ast, self.operationL.id, "-=", Symbol(symbol_type=None, value=1, data_type=dominant_type, environment=env, line=self.line, column=self.column))
                    return Symbol(symbol_type=None, value=operation1.value-1, data_type=dominant_type, environment=env, line=self.line, column=self.column)
                ast.setErrors(Error("Semantico", "Tipos incorrectos para decrementar", "Operation", self.line, self.column))
        return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=env, line=self.line, column=self.column)