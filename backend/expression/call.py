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

    def execute(self, ast, env):
        func = env.getFunction(ast, self.id)
        if func == {}:
            return
        if len(self.params) != len(func['params']):
            ast.setErrors(Error("Semantico", "El numero de parametros no coincide con la definicion de la funcion", "Call", self.line, self.column))
            return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=env, line=self.line, column=self.column)
        function_env = Environment(env.getGlobalEnvironment(), 'FUNCTION_'+self.id)
        if len(self.params) > 0:
            symbolList = []
            for i in range(len(self.params)):
                symParam = self.params[i].execute(ast, env)
                symbolList.append(symParam)
                id_param = list(func['params'][i].keys())[0]
                type_param = list(func['params'][i].values())[0]
                if type_param != symParam.data_type:
                    ast.setErrors(Error("Semantico", "El tipo del parametro no coincide con la definicion de la funcion", "Call", self.line, self.column))
                    return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, line=self.line, column=self.column)
                function_env.saveSymbol(ast, id_param, symParam)
        # Ejecutar bloque
        returnValue = statementExecuter(func['block'], ast, function_env)
        if returnValue != None:
            if returnValue.data_type != func['data_type']:
                ast.setErrors(Error("Semantico", "El tipo de retorno no coincide con la definicion de la funcion", "Call", self.line, self.column))
                return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=env, line=self.line, column=self.column)
            return returnValue        
        return None