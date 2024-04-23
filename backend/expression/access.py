from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value

class Access(Expression):
    def __init__(self, id, line, column):
        self.id = id
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Realizar busqueda en entorno
        sym = env.getVariable(ast, self.id, {'line': self.line, 'column': self.column})
        if(sym.data_type != ExpressionType.NULL):
            # Reconstrucción de Value
            return Value(sym.position, False, sym.data_type, [], [], [])
        return Value('', False, ExpressionType.NULL, [], [], [])