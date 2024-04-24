from abstract.instruction import Instruction
from environment.environment import Environment
from environment.execute import statementExecuter

class While(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        gen.comment('Generando un ciclo While')
        # Agregando etiqueta de retorno
        newLabel = gen.new_label()
        gen.new_body_label(newLabel)
        # Se imprime el "if" en el código de la expresion
        condition = self.exp.execute(ast, env, gen)
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