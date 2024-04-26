from abstract.instruction import Instruction
from environment.environment import Environment
from environment.execute import statementExecuter
from environment.type import ExpressionType
from environment.value import Value

class While(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        gen.comment('Generando un ciclo WHILE')
        # Agregando etiqueta de retorno
        newLabel = gen.new_label()
        gen.new_body_label(newLabel)
        # Generando etiqueta false
        falseLvl = gen.new_label()
        # Obteniendo la condición
        condition = self.exp.execute(ast, env, gen)
        # Agregando un primitivo booleano
        temp = gen.new_temp()
        gen.add_br()
        gen.comment('Agregando un primitivo booleano')
        gen.add_li('t0', '1')
        gen.add_li('t3', str(temp))
        gen.add_sw('t0', '0(t3)')
        # Creando temporales
        gen.add_br()
        gen.add_li('t3', str(condition.value))
        gen.add_lw('t1', '0(t3)')
        gen.add_li('t3', str(temp))
        gen.add_lw('t2', '0(t3)')
        # Generando etiqueta true
        trueLvl = gen.new_label()
        # Agregando condición
        gen.add_beq('t1', 't2', trueLvl)
        # Agregando salto
        gen.add_jump(falseLvl)
        # Result
        result = Value("", False, ExpressionType.BOOLEAN, [], [], [])
        result.truelvl.append(trueLvl)
        result.falselvl.append(falseLvl)
        # Se agregan las etiquetas verdaderas
        for lvl in result.truelvl:
            gen.new_body_label(lvl)
        # Instrucciones While
        while_env = Environment(env, "WHILE")
        statementExecuter(self.block, ast, while_env, gen)
        # Salto etiqueta de retorno
        gen.add_jump(newLabel)
        # Se agregan las etiquetas falsas
        for lvl in result.falselvl:
            gen.new_body_label(lvl)
        return None








    '''
        # Se agregan las etiquetas verdaderas
        for lvl in condition.truelvl:
            gen.new_body_label(lvl)
        # Instrucciones While
        while_env = Environment(env, "WHILE")
        statementExecuter(self.block, ast, while_env, gen)
        # Salto etiqueta de retorno
        gen.add_jump(newLabel)
        # Se agregan las etiquetas falsas
        for lvl in condition.falselvl:
            gen.new_body_label(lvl)
        return None
    '''