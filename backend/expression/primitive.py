from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value

class Primitive(Expression):
    def __init__(self, value, type, line, column):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        temp = gen.new_temp()
        if(self.type == ExpressionType.NUMBER):
            gen.add_br()
            gen.comment('Agregando un primitivo numerico')
            gen.add_li('t0', str(self.value))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, self.type, [], [], [])
        elif (self.type == ExpressionType.STRING):
            nameId = 'str_'+str(temp)
            gen.variable_data(nameId, 'string', '\"'+str(self.value)+'\"')
            return  Value(nameId, False, self.type, [], [], [])
        elif (self.type == ExpressionType.CHAR):
            nameId = 'char_'+str(temp)
            gen.variable_data(nameId, 'byte', '\''+str(self.value)+'\'')
            return  Value(nameId, False, self.type, [], [], [])
        elif (self.type == ExpressionType.BOOLEAN):
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
            return result