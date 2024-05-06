from abstract.instruction import Instruction
from environment.generator import Generator
from environment.execute import statementExecuter
from environment.symbol import Symbol
from expression.primitive import Primitive
from instructions.declaration import Declaration
from environment.type import ExpressionType
from environment.value import Value

class Function(Instruction):
    def __init__(self, id, params, type, block, line, column):
        self.id = id
        self.params = params
        self.type = type
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        value = None
        nm_params = []
        # Con parametros
        if len(self.params) > 0:
            # Ejecutar parametros
            for param in self.params:
                for key, value in param.items():
                    if (value == ExpressionType.NUMBER):
                        nm_params.append(key)
                        val = Primitive(0, value, self.line, self.column)
                        dec = Declaration('VAR', key, value, val, self.line, self.column)
                        dec.execute(ast, env, gen)
            # Generar nueva environment
            gen_func = Generator()
            # Cargar valores
            gen_func.Temporal = gen.Temporal
            gen_func.Label    = gen.Label
            gen_func.TempList = gen.TempList
            gen_func.add_function(self.id)
            # Con retorno
            if self.type != ExpressionType.NULL:
                jump = statementExecuter(self.block, ast, env, gen_func)
                if jump != None:
                    value = Value(jump.value, True, self.type, [], [], [])  
                # Agregar fin de funcion
                gen_func.add_br()
                gen_func.add_end_function()
            # Sin retorno
            else:
                statementExecuter(self.block, ast, env, gen_func)
                # Agregar fin de funcion
                gen_func.add_br()
                gen_func.add_end_function()
        # Sin parametros
        else:
            # Generar nueva environment
            gen_func = Generator()
            # Cargar valores
            gen_func.Temporal = gen.Temporal
            gen_func.Label    = gen.Label
            gen_func.TempList = gen.TempList
            gen_func.add_function(self.id)
            # Con retorno
            if self.type != ExpressionType.NULL:
                pass
            # Sin retorno
            else:
                statementExecuter(self.block, ast, env, gen_func)
                # Agregar fin de funcion
                gen_func.add_br()
                gen_func.add_end_function()
        # Devolver valores
        gen.Temporal = gen_func.Temporal
        gen.Label    = gen_func.Label
        gen.TempList = gen_func.TempList
        gen.Data += gen_func.Data
        gen.add_functions_code(gen_func.get_code())
        #env.funcs[self.id] = {'params': nm_params, 'type': self.type, 'generator': gen_func}
        env.funcs[self.id] = {'params': nm_params, 'return': value}
        return value