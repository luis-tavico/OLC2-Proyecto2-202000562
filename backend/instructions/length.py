from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value
from errors.error import Error

class Length(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Realizar busqueda en entorno
        arr = self.array.execute(ast, env, gen)
        sym = env.getVariable(ast, arr.value+"_length", {'line': self.line, 'column': self.column})
        if(sym.data_type != ExpressionType.NULL):
            # Reconstrucción de Value
            return Value(sym.position, False, sym.data_type, [], [], [])
        return Value('', False, ExpressionType.NULL, [], [], [])