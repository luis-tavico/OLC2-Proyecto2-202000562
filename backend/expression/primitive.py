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