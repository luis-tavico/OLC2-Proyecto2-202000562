from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value
from errors.error import Error

class ArrayAccess(Expression):
    def __init__(self, array, index, line, column):
        self.array = array
        self.index = index
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Traer el arreglo
        sym = env.getVariable(ast, self.array, {'line': self.line, 'column': self.column})
        if(sym.data_type == ExpressionType.NULL):
            ast.setErrors(Error(type="Semantico", description=f"El arreglo {self.array} no ha sido encontrado", ambit=env.id , line=self.line, column=self.column))
            return None
        # Validar tipo principal
        indexVal = self.index.execute(ast, env, gen)
        if indexVal.type != ExpressionType.NUMBER:
            ast.setErrors(Error(type="Semantico", description="El indice contiene un valor incorrecto", ambit=env.id , line=self.line, column=self.column))
            return None
        # Agregar llamada
        gen.add_br()
        gen.comment('Acceso a un arreglo')
        if 't' in str(indexVal.value):
            gen.add_move('t3', str(indexVal.value))
        else:
            gen.add_li('t3', str(indexVal.value))
        gen.add_lw('t1', '0(t3)')
        gen.add_move('t0', 't1')
        gen.add_slli('t0', 't0', '2')
        gen.add_la('t1', str(sym.position))

        gen.add_lw('t1', '0(t1)')

        gen.add_operation('add', 't2', 't1', 't0')
        return Value('t2', True, ExpressionType.NUMBER, [], [], [])