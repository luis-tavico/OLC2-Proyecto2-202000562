from abstract.expression import Expression
from environment.type import ExpressionType
from instructions.assignment import Assignment
from environment.value import Value

class Call(Expression):
    def __init__ (self, id, params, line, column):
        self.id = id
        self.params = params
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        params_func = env.funcs[self.id]['params']
        for param in params_func:
            assignment = Assignment(param, '=', self.params.pop(0), self.line, self.column)
            assignment.execute(ast, env, gen)
        env.funcs[self.id]['return']
        val = env.funcs[self.id]['return']
        gen.add_br()
        gen.call_function(self.id)
        return val