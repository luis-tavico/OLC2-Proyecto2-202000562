from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value

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
            elif (val.type == ExpressionType.STRING or val.type == ExpressionType.CHAR):
                gen.add_br()
                if 't' in str(val.value) and len(str(val.value)) < 2:
                    gen.add_move('a0', str(val.value))
                else:
                    gen.add_la('a0', str(val.value))
                gen.add_li('a7', '4')
                gen.add_system_call()
            elif (val.type == ExpressionType.BOOLEAN):
                    # Agregando un primitivo booleano
                    temp = gen.new_temp()
                    gen.add_br()
                    gen.comment('Agregando un primitivo booleano')
                    gen.add_li('t0', '1')
                    gen.add_li('t3', str(temp))
                    gen.add_sw('t0', '0(t3)')
                    # Creando temporales
                    gen.add_br()
                    gen.add_li('t3', str(val.value))
                    gen.add_lw('t1', '0(t3)')
                    gen.add_li('t3', str(temp))
                    gen.add_lw('t2', '0(t3)')
                    # Generando etiquetas
                    trueLvl = gen.new_label()
                    falseLvl = gen.new_label()
                    # Agregando condición
                    gen.add_beq('t1', 't2', trueLvl)
                    # Agregando salto
                    gen.add_jump(falseLvl)
                    # Result
                    result = Value("", False, ExpressionType.BOOLEAN, [], [], [])
                    result.truelvl.append(trueLvl)
                    result.falselvl.append(falseLvl)
                    # Etiqueta de salida
                    newLabel = gen.new_label()
                    # Se agregan las etiquetas verdaderas
                    for lvl in result.truelvl:
                        gen.new_body_label(lvl)
                    # Imprimiendo expresion
                    gen.add_br()
                    gen.add_la('a0', 'str_true')
                    gen.add_li('a7', '4')
                    gen.add_system_call()
                    # Imprimiendo salto de linea
                    gen.add_br()
                    gen.add_li('a0', '10')
                    gen.add_li('a7', '11')
                    gen.add_system_call()
                    # Salto etiqueta de salida
                    gen.add_jump(newLabel)
                    # Se agregan las etiquetas falsas
                    for lvl in result.falselvl:
                        gen.new_body_label(lvl)
                    # Imprimiendo expresion
                    gen.add_br()
                    gen.add_la('a0', 'str_false')
                    gen.add_li('a7', '4')
                    gen.add_system_call()
                    # Imprimiendo salto de linea
                    gen.add_br()
                    gen.add_li('a0', '10')
                    gen.add_li('a7', '11')
                    gen.add_system_call()
                    # Etiqueta de salida
                    gen.new_body_label(newLabel)
        # Imprimiendo salto de linea
        gen.add_br()
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()
        '''
        if (val.type == ExpressionType.BOOLEAN):
            gen.new_body_label(newLabel)
        '''
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