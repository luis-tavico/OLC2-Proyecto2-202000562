from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value
from errors.error import Error

class Pop(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Obtner arreglo
        sym = env.getVariable(ast, self.array.id, {'line': self.line, 'column': self.column})
        if(sym.data_type == ExpressionType.NULL):
            ast.setErrors(Error(type="Semantico", description=f"El arreglo {self.array} no ha sido encontrado", ambit=env.id , line=self.line, column=self.column))
            return None
        # Obtener tamaño de arreglo
        size = env.getVariable(ast, sym.position+"_length", {'line': self.line, 'column': self.column})
        gen.add_br()
        gen.comment('Pop a un arreglo')
        # Traer el arreglo
        gen.add_la('t4', str(sym.position))
        # Cargar longitud
        gen.add_br()
        gen.add_li('t3', str(size.position))
        gen.add_lw('t1', '0(t3)')
        gen.add_li('t2', str(4))
        # Decrementar la longitud
        gen.add_operation('addi', 't1', 't1', '-1')
        gen.add_sw('t1', '0(t3)')
        # Multiplicar el indice por el tamaño de cada elemento (4 bytes)
        gen.add_br()
        gen.add_operation('mul', 't1', 't1', 't2')
        # Sumar el desplazamiento a la dirección base
        gen.add_operation('add', 't4', 't4', 't1')
        # Acceder al valor en la direccion calculada
        gen.add_lw('t3', '0(t4)')
        # Almacenar el valor
        temp = gen.new_temp()
        gen.add_br()
        gen.comment('Agregando un primitivo numerico')
        gen.add_lw('t0', '0(t3)')
        gen.add_li('t3', str(temp))
        gen.add_sw('t0', '0(t3)')
                     
        return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])