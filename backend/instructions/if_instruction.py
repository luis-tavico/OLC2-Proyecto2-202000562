from abstract.instruction import Instruction
from environment.execute import statementExecuter
from environment.environment import Environment
from environment.type import ExpressionType
from environment.value import Value

class If(Instruction):
    def __init__(self, exp, if_block, elseifs, else_block, line, column):
        self.exp = exp
        self.if_block = if_block
        self.elseifs = elseifs
        self.else_block = else_block
        self.line = line
        self.column = column  
    
    def execute(self, ast, env, gen):
        gen.comment('Generando sentencia IF')
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
        if_env = Environment(env, "IF")
        jump = statementExecuter(self.if_block, ast, if_env, gen)
        if jump != None:
            if jump.type == ExpressionType.BREAK:
                gen.add_jump(gen.BreakLabels[-1])
            elif jump.type == ExpressionType.CONTINUE:
                gen.add_jump(gen.ContinueLabels[-1])
        else:
            # Salto etiqueta de salida
            gen.add_jump(newLabel)
        # Se agregan las etiquetas falsas
        for lvl in result.falselvl:
            gen.new_body_label(lvl)
        # Validar elseif
        if self.elseifs != None:
            for elseif in self.elseifs:
                # Obteniendo la condición
                condition = elseif.exp.execute(ast, env, gen)
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
                # Se agregan las etiquetas verdaderas
                for lvl in result.truelvl:
                    gen.new_body_label(lvl)
                # Instrucciones elseif
                elseif_env = Environment(env, "ELSEIF")
                jump = statementExecuter(elseif.block, ast, elseif_env, gen)
                if jump != None:
                    if jump.type == ExpressionType.BREAK:
                        gen.add_jump(gen.BreakLabels[-1])
                    elif jump.type == ExpressionType.CONTINUE:
                        gen.add_jump(gen.ContinueLabels[-1])
                else:
                    # Salto etiqueta de salida
                    gen.add_jump(newLabel)
                # Se agregan las etiquetas falsas
                for lvl in result.falselvl:
                    gen.new_body_label(lvl)
        # Validar else
        if self.else_block != None:
            else_env = Environment(env, "ELSE")
            jump = statementExecuter(self.else_block, ast, else_env, gen)
            if jump != None:
                if jump.type == ExpressionType.BREAK:
                    gen.add_jump(gen.BreakLabels[-1])
                elif jump.type == ExpressionType.CONTINUE:
                    gen.add_jump(gen.ContinueLabels[-1])
        # Etiqueta de salida
        gen.new_body_label(newLabel)
        return result