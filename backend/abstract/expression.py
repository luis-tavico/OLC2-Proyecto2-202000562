from abc import ABC, abstractmethod

class Expression(ABC):
    
    @abstractmethod
    def execute(self, ast, env, gen):
        pass