from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class ArrayDeclaration(Instruction):
    def __init__(self, id, type, exp, line, column):
        self.id = id
        self.type = type
        self.exp = exp
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        temp = gen.new_temp()
        arrValue = self.exp.execute(ast, env, gen)
        # Validar tipo
        if arrValue.type != ExpressionType.ARRAY:
            ast.setErrors(Error(type="Semantico", description="La expresion no es un arreglo", ambit=env.id , line=self.line, column=self.column))
            return None
        nameId = 'arr_'+str(temp)
        gen.variable_data(nameId, 'word', ', '.join(arrValue.value))
        nmId = 'arr_'+str(temp)+'_length'
        gen.variable_data(nmId, 'word', str(len(arrValue.value)))
        # Generar simbolo
        sym = Symbol(symbol_type='VAR', id=self.id, data_type=ExpressionType.ARRAY, position=nameId, line=self.line, column=self.column)
        # Agregar al entorno
        env.saveVariable(ast, self.id, sym)
        return None