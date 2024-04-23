from abstract.instruction import Instruction
from environment.type import ExpressionType

class Print(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        for exp in self.expression:
            val = exp.execute(ast, env, gen)
            if val == None:
                continue
            elif (val.type == ExpressionType.NULL):
                return None
            elif (val.type == ExpressionType.NUMBER):
                # Imprimiendo expresion
                gen.add_br()
                if 't' in str(val.value):
                    gen.add_move('t3', str(val.value))
                else:
                    gen.add_li('t3', str(val.value))
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
                gen.add_system_call()
            elif (val.type == ExpressionType.STRING):
                gen.add_br()
                if 't' in str(val.value) and len(str(val.value)) < 2:
                    gen.add_move('a0', str(val.value))
                else:
                    gen.add_la('a0', str(val.value))
                gen.add_li('a7', '4')
                gen.add_system_call()
        # Imprimiendo salto de linea
        gen.add_br()
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()

        return None

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