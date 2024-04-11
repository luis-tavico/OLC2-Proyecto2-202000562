from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value

class Operation(Expression):
    def __init__(self, operationL, operator, operationR, line, column):
        self.operationL = operationL
        self.operator = operator
        self.operationR = operationR
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Ejecución de operandos
        op1 = self.operationL.execute(ast, env, gen)
        op2 = self.operationR.execute(ast, env, gen)

        gen.add_br()
        gen.add_li('t3', str(op1.value))
        gen.add_lw('t1', '0(t3)')
        gen.add_li('t3', str(op2.value))
        gen.add_lw('t2', '0(t3)')
        temp = gen.new_temp()

        # Operaciones aritmeticas
        if self.operator == "+":
            gen.add_operation('add', 't0', 't1', 't2')
            newVal = op1.intValue + op2.intValue
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), newVal, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "-":
            gen.add_operation('sub', 't0', 't1', 't2')
            newVal = op1.intValue - op2.intValue
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), newVal, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "*":
            gen.add_operation('mul', 't0', 't1', 't2')
            newVal = op1.intValue * op2.intValue
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), newVal, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "/":
            gen.add_operation('div', 't0', 't1', 't2')
            newVal = op1.intValue / op2.intValue
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), newVal, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "%":
            gen.add_operation('rem', 't0', 't1', 't2')
            newVal = op1.intValue % op2.intValue
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), newVal, ExpressionType.NUMBER, [], [], [])

        return None