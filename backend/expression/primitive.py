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
        if(self.type == ExpressionType.NUMBER):
            temp = gen.new_temp() # 4
            gen.add_br()
            gen.add_li('t0', str(self.value))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), self.value, self.type, [], [], [])