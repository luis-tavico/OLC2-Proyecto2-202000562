from abstract.expression import Expression

class Interfaceaccess(Expression):
    def __init__(self, instance, attribute, line, column):
        self.instance = instance
        self.attribute = attribute
        self.line = line
        self.column = column

    def execute(self, ast, env):
        env_interface = self.instance.execute(ast, env)
        sym = env_interface.getSymbol(ast, self.attribute)
        return sym