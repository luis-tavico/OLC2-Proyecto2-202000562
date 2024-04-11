from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from environment.environment import Environment
from environment.execute import statementExecuter
from errors.error import Error

class Call(Expression):
    def __init__ (self, id, params, line, column):
        self.id = id
        self.params = params
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None