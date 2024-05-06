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
        arrValue = self.exp.execute(ast, env, gen)
        # Validar tipo
        if arrValue.type != ExpressionType.ARRAY:
            ast.setErrors(Error(type="Semantico", description="La expresion no es un arreglo", ambit=env.id , line=self.line, column=self.column))
            return None
        # Reservar espacio en memoria
        mem_space = []
        i = len(arrValue.value)
        while i < 10:
            temp = gen.new_temp()
            gen.add_br()
            gen.comment('Agregando un primitivo numerico')
            gen.add_li('t0', str(0))
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            mem_space.append(str(temp))
            i += 1
        # Generar arreglo
        temp_vals = ''
        temp_vals += ', '.join(arrValue.value)
        temp_vals += ', '
        temp_vals += ', '.join(mem_space)
        # Generar variable
        temp = gen.new_temp()
        nameId = 'arr_'+str(temp)
        gen.variable_data(nameId, 'word', temp_vals)
        # Generar simbolo
        sym = Symbol(symbol_type='VAR', id=self.id, data_type=ExpressionType.ARRAY, position=nameId, value=arrValue.value, line=self.line, column=self.column)
        # Agregar al entorno
        env.saveVariable(ast, self.id, sym)
        # Almacenar la longitud del array
        nmId = 'arr_'+str(temp)+'_length'
        temp = gen.new_temp()
        gen.add_br()
        gen.comment('Agregando un primitivo numerico')
        gen.add_li('t0', str(len(arrValue.value)))
        gen.add_li('t3', str(temp))
        gen.add_sw('t0', '0(t3)')
        # Generar simbolo
        sym = Symbol(symbol_type='VAR', id=self.id+"_length", data_type=ExpressionType.NUMBER, position=temp, value=len(arrValue.value), line=self.line, column=self.column)
        # Agregar al entorno
        env.saveVariable(ast, nmId, sym)
        return None