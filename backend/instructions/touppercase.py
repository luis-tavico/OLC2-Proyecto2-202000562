from abstract.instruction import Instruction
from environment.type import ExpressionType
from expression.access import Access
from environment.value import Value

class Touppercase(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        if (isinstance(self.expression, Access)):
            sym = env.getVariable(ast, self.expression.id, {'line': self.line, 'column': self.column})
            temp = gen.new_temp()
            nameId = 'str_'+str(temp)
            gen.variable_data(nameId, 'string', '\"'+str(sym.value.upper())+'\"')
            return Value(nameId, False, sym.data_type, [], [], [])

        return Value("", False, ExpressionType.NULL, [], [], [])