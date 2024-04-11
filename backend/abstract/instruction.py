from abc import ABC, abstractmethod

class Instruction(ABC):
    
    @abstractmethod
    def execute(self, ast, env, gen):
        pass