from abstract.instruction import Instruction
from environment.type import ExpressionType

class Print(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        outText = ""
        for exp in self.expression:
            sym = exp.execute(ast, env)
            if sym == None:
                continue
            if sym.data_type == ExpressionType.ARRAY:
                outText += self.print_array(sym.value)
            elif sym.data_type == ExpressionType.NULL:
                pass
            elif sym.data_type == ExpressionType.BOOLEAN:
                    if sym.value == True:
                        outText += "true"
                    elif sym.value == False:
                        outText += "false"
            else:
                outText += str(sym.value) + " "
        ast.setConsole(outText)

    def print_array(self, array):
        result = ""
        if isinstance(array, list):
            result += "[ "
            for i, sym in enumerate(array):
                result += self.print_array(sym)
                if i < len(array) - 1:
                    result += ", "
            result += " ]"
        elif array.data_type == ExpressionType.ARRAY:
            result += "[ "
            for i, sym in enumerate(array.value):
                result += self.print_array(sym)
                if i < len(array.value) - 1:
                    result += ", "
            result += " ]"
        else:
            result += str(array.value)
        return result