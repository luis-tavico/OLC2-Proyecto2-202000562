from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Push(Instruction):
    def __init__(self, array, expression, line, column):
        self.array = array
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Traer el arreglo
        sym = env.getVariable(ast, self.array.id, {'line': self.line, 'column': self.column})
        if(sym.data_type == ExpressionType.NULL):
            ast.setErrors(Error(type="Semantico", description=f"El arreglo {self.array} no ha sido encontrado", ambit=env.id , line=self.line, column=self.column))
            return None
        ###
        l = env.getVariable(ast, sym.position+"_length", {'line': self.line, 'column': self.column})
        # Ejecutar expresion
        #exp = self.expression.execute(ast, env, gen)
        # Agregar llamada
        gen.add_br()
        gen.comment('Push a un arreglo')
        '''
        gen.add_lw('t1', str(sym.position+'_length'))
        #gen.add_lw('t1', str(sym.position+'_length'))
        gen.add_slli('t2', 't1', '2')
        gen.add_lw('t4', str(sym.position))
        gen.add_operation('add', 't3', 't2', 't4')
        # incrementar tamaño
        gen.add_operation('addi', 't1', 't1', '1')
        gen.add_sw('t1', str(sym.position+'_length'))
        return None
        '''
        '''
        gen.add_la('t0', str(sym.position)) 
        gen.add_lw('t1', str(sym.position+'_length'))
        if 't' in str(exp.value):
            gen.add_move('t3', str(exp.value))
        else:
            gen.add_li('t3', str(exp.value))
        gen.add_slli('t2', 't1', '2')
        gen.add_operation('add', 't2', 't2', 't0')
        gen.add_sw('t3', '0(t2)')
        # incrementar tamaño
        gen.add_operation('addi', 't1', 't1', '1')
        gen.add_la('t4', str(sym.position+'_length'))
        gen.add_sw('t1', '0(t4)')
        '''
        '''
        gen.add_la('t0', str(sym.position)) 
        gen.add_lw('t1', str(sym.position+'_length'))
        gen.add_move('t2', 't1')
        gen.add_operation('add', 't1', 't1', 't0')
        if 't' in str(exp.value):
            gen.add_move('t3', str(exp.value))
        else:
            gen.add_li('t3', str(exp.value))
        gen.add_sw('t3', '0(t1)')
        gen.add_operation('addi', 't2', 't2', '1')
        gen.add_la('t4', str(sym.position+'_length'))
        gen.add_sw('t2', '0(t4)')
        '''
        '''
        gen.add_li('t0', str(28))
        gen.add_la('t1', str(sym.position))
        # 
        gen.add_li('t6', str(l.position))
        gen.add_lw('t2', "0(t6)")
        
        gen.add_slli('t3', 't2', '2')
        gen.add_operation('add', 't4', 't1', 't3')
        gen.add_sw('t0', '0(t4)')
        # incrementar tamaño
        gen.add_operation('addi', 't2', 't2', '1')
        gen.add_la('t5', str(l.position))
        gen.add_sw('t2', '0(t5)')
        '''