from abstract.instruction import Instruction
from environment.execute import statementExecuter
from environment.environment import Environment

class If(Instruction):
    def __init__(self, exp, if_block, elseifs, else_block, line, column):
        self.exp = exp
        self.if_block = if_block
        self.elseifs = elseifs
        self.else_block = else_block
        self.line = line
        self.column = column  
    
    def execute(self, ast, env, gen):
        gen.comment('Generando setencia IF')
        # Se imprime el "if" en el código de la expresion
        condition = self.exp.execute(ast, env, gen)
        # Etiqueta de salida
        newLabel = gen.new_label()
        # Se agregan las etiquetas verdaderas
        for lvl in condition.truelvl:
            gen.new_body_label(lvl)
        # Instrucciones If
        if_env = Environment(env, "IF")
        statementExecuter(self.if_block, ast, if_env, gen)
        # Salto etiqueta de salida
        gen.add_jump(newLabel)
        # Se agregan las etiquetas falsas
        for lvl in condition.falselvl:
            gen.new_body_label(lvl)
        # Validar else if
        if self.elseifs != None:
            for elseif in self.elseifs:
                # Se imprime el "if" en el código de la expresion
                condition = elseif.exp.execute(ast, env, gen)
                # Se agregan las etiquetas verdaderas
                for lvl in condition.truelvl:
                    gen.new_body_label(lvl)
                # Instrucciones If
                elseif_env = Environment(env, "ELSEIF")
                statementExecuter(elseif.block, ast, elseif_env, gen)
                # Salto etiqueta de salida
                gen.add_jump(newLabel)
                # Se agregan las etiquetas falsas
                for lvl in condition.falselvl:
                    gen.new_body_label(lvl)
        # Validar else
        if self.else_block != None:
            else_env = Environment(env, "ELSE")
            statementExecuter(self.else_block, ast, else_env, gen)
        # Etiqueta de salida
        gen.new_body_label(newLabel)
        return None