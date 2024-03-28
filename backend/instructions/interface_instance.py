from abstract.instruction import Instruction
from environment.environment import Environment
from errors.error import Error

class Interfaceinstance(Instruction):
    def __init__(self, id_instance, id_interface, content, line, column):
        self.id_instance = id_instance
        self.id_interface = id_interface
        self.content = content
        self.line = line
        self.column = column

    def execute(self, ast, env):
        interfaceValue = env.getStruct(ast, self.id_interface)
        if interfaceValue == None:
            return None
        newEnv = Environment(None, 'INTERFACE_'+self.id_instance)
        for i in range(len(self.content)):
            id_param = list(interfaceValue[i].keys())[0]
            type_param = list(interfaceValue[i].values())[0]
            id_exp = list(self.content[i].keys())[0]
            val_exp = list(self.content[i].values())[0].execute(ast, env)
            if isinstance(val_exp, Environment):
                newEnv.saveSymbol(ast, id_param, val_exp)
            elif type_param == val_exp.data_type and id_param == id_exp:
                newEnv.saveSymbol(ast, id_param, val_exp)
            else:
                ast.setErrors(Error("Semantico", "El tipo o identificador de la interfaz es incorrecto", "InterfaceInstance", self.line, self.column))
                return None
        env.saveSymbol(ast, self.id_instance, newEnv)