from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error 

class Environment():
    def __init__(self, previous, id):
        self.previous = previous
        self.id = id
        self.symbols_table = {}
        self.interfaces = {}
        self.functions = {}

    def saveSymbol(self, ast, id, symbol):
        if id in self.symbols_table:
            ast.setErrors(Error("Semantico", f"Variable {id} ya existe", self.id, symbol.line, symbol.column))
            return
        self.symbols_table[id] = symbol

    def setSymbol(self, ast, id, type_assignment, symbol):
        tmpEnv = self
        while True:
            if id in tmpEnv.symbols_table:
                if tmpEnv.symbols_table[id].data_type == symbol.data_type:
                    if tmpEnv.symbols_table[id].symbol_type == "const":
                        ast.setErrors(Error("Semantico", f"Variable {id} es constante", self.id, symbol.line, symbol.column))
                        return symbol
                    if type_assignment == "+=":
                        if symbol.data_type == ExpressionType.NUMBER or symbol.data_type == ExpressionType.FLOAT or symbol.data_type == ExpressionType.STRING:
                            tmpEnv.symbols_table[id].value += symbol.value
                        else:
                            ast.setErrors(Error("Semantico", f"Tipos no compatibles para incrementar", self.id, symbol.line, symbol.column))
                    elif type_assignment == "-=":
                        if symbol.data_type == ExpressionType.NUMBER or symbol.data_type == ExpressionType.FLOAT or symbol.data_type == ExpressionType.STRING:
                            tmpEnv.symbols_table[id].value -= symbol.value
                        else:
                            ast.setErrors(Error("Semantico", f"Tipos no compatibles para decrementar", self.id, symbol.line, symbol.column))
                    else:
                        tmpEnv.symbols_table[id].value = symbol.value
                else:
                    if tmpEnv.symbols_table[id].data_type == ExpressionType.FLOAT and symbol.data_type == ExpressionType.NUMBER:
                        tmpEnv.symbols_table[id].value = float(symbol.value)
                    else:
                        ast.setErrors(Error("Semantico", f"Variable {id} no es del mismo tipo", self.id, symbol.line, symbol.column))
                return symbol
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        ast.setErrors(Error("Semantico", f"Variable {id} no existe", self.id, symbol.line, symbol.column))
        return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=None, line=0, column=0)

    def getSymbol(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.symbols_table:
                return tmpEnv.symbols_table[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        ast.setErrors(Error("Semantico", f"Variable {id} no existe", self.id, 0, 0))
        return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=None, line=0, column=0)
    
    def saveFunction(self, ast, id, function):
        if id in self.functions:
            ast.setErrors(Error("Semantico", f"Funcion {id} ya existe", self.id, function.line, function.column))
            return
        self.functions[id] = function
    
    def getFunction(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.functions:
                return tmpEnv.functions[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        ast.setErrors(Error("Semantico", f"Funcion {id} no existe", self.id, 0, 0))
        return {}
    
    def saveStruct(self, ast, id, struct):
        if id in self.interfaces:
            ast.setErrors(Error("Semantico", f"La interface {id} ya existe", self.id, struct.line, struct.column))
            return
        self.interfaces[id] = struct
    
    def getStruct(self, ast, id):
        tmpEnv = self
        while True:
            if id in tmpEnv.interfaces:
                return tmpEnv.interfaces[id]
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        ast.setErrors(Error("Semantico", f"La interface {id} no existe", self.id, 0, 0))
        return None
    
    def loopValidation(self):
        tmpEnv = self
        while True:
            if tmpEnv.id ==  "WHILE" or tmpEnv.id == "FOR" or tmpEnv.id == "SWITCH":
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False
    
    def functionValidation(self):
        tmpEnv = self
        while True:
            if 'FUNCTION_' in tmpEnv.id:
                return True
            if tmpEnv.previous == None:
                break
            else:
                tmpEnv = tmpEnv.previous
        return False
    
    def getGlobalEnvironment(self):
        tmpEnv = self
        while True:
            if tmpEnv.previous == None:
                return tmpEnv
            else:
                tmpEnv = tmpEnv.previous