from abstract.instruction import Instruction
from expression.operation import Operation
from environment.type import ExpressionType
from environment.environment import Environment
from environment.execute import statementExecuter
from environment.value import Value

class Switch(Instruction):
    def __init__(self, exp, cases, line, column):
        self.exp = exp
        self.cases = cases
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        gen.comment('Generando sentencia SWITCH')
        # Etiqueta de salida
        exit = gen.new_label()
        for case in self.cases:
            if case.exp != None:
                # Ejecutando la condición
                condition = Operation(case.exp, '==', self.exp, self.line, self.column)
                condition = condition.execute(ast, env, gen)
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
                # Generando etiquetas
                trueLvl = gen.new_label()
                falseLvl = gen.new_label()
                # Agregando condición
                gen.add_beq('t1', 't2', trueLvl)
                # Agregando salto
                gen.add_jump(falseLvl)
                # Result
                result = Value("", False, ExpressionType.BOOLEAN, [], [], [])
                result.truelvl.append(trueLvl)
                result.falselvl.append(falseLvl)
                # Etiqueta de salida
                newLabel = gen.new_label()
                # Se agregan las etiquetas verdaderas
                for lvl in result.truelvl:
                    gen.new_body_label(lvl)
                # Instrucciones If
                if_env = Environment(env, "CASE")
                statementExecuter(case.block, ast, if_env, gen)
                # Salto etiqueta de salida
                gen.add_jump(newLabel)
                # Se agregan las etiquetas falsas
                for lvl in result.falselvl:
                    gen.new_body_label(lvl)
                # Etiqueta de salida
                gen.new_body_label(newLabel)
            else:
                default_env = Environment(env, "DEFAULT")
                statementExecuter(case.block, ast, default_env, gen)
        # Etiqueta de salida
        gen.new_body_label(exit)
        return None