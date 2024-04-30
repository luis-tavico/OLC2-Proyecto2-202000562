from abstract.instruction import Instruction
from environment.environment import Environment
from environment.type import ExpressionType
from environment.execute import statementExecuter
from expression.access import Access
from instructions.declaration import Declaration
from errors.error import Error
from environment.value import Value
from instructions.assignment import Assignment

class For(Instruction):
    def __init__(self, declaration, exp1, exp2, block, line, column):
        self.declaration = declaration
        self.exp1 = exp1
        self.exp2 = exp2
        self.block = block
        self.line = line
        self.column = column
   
    def execute(self, ast, env, gen):
        gen.comment('Generando un ciclo FOR')
        # Ejecutar declaracion
        self.declaration.execute(ast, env, gen)
        # Agregando etiqueta de retorno
        newLabel = gen.new_label()
        gen.new_body_label(newLabel)
        # Generando etiqueta false
        falseLvl = gen.new_label()
        # Ejecutar expresion 1 (condicion)
        condition = self.exp1.execute(ast, env, gen)
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
        # Instrucciones FOR
        for_env = Environment(env, "FOR")
        statementExecuter(self.block, ast, for_env, gen)
        # Ejecutar expresion 2 (incremento/decremento)
        self.exp2.execute(ast, env, gen)
        # Salto etiqueta de retorno
        gen.add_jump(newLabel)
        # Se agregan las etiquetas falsas
        for lvl in result.falselvl:
            gen.new_body_label(lvl)

        return None