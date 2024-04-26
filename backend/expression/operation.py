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
        gen.comment('Realizando operacion')
        if 't' in str(op1.value):
            gen.add_move('t3', str(op1.value))
        else:
            gen.add_li('t3', str(op1.value))
        #gen.add_li('t3', str(op1.value))
        gen.add_lw('t1', '0(t3)')
        if 't' in str(op2.value):
            gen.add_move('t3', str(op2.value))
        else:
            gen.add_li('t3', str(op2.value)) 
        #gen.add_li('t3', str(op2.value))
        gen.add_lw('t2', '0(t3)')
        temp = gen.new_temp()

        # OPERACIONES ARITMETICAS
        if self.operator == "+":
            gen.add_operation('add', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "-":
            gen.add_operation('sub', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "*":
            gen.add_operation('mul', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "/":
            gen.add_operation('div', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])
        elif self.operator == "%":
            gen.add_operation('rem', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.NUMBER, [], [], [])
        
        # OPERACIONES RELACIONALES
        elif self.operator == "<":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_blt('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        elif self.operator == ">":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_bgt('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        elif self.operator == ">=":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_bge('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        elif self.operator == "<=":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_ble('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        elif self.operator == "==":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_beq('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        elif self.operator == "!=":
            # Generando etiquetas
            trueLvl = gen.new_label()
            falseLvl = gen.new_label()
            # Agregando condición
            gen.add_bne('t1', 't2', trueLvl)
            # Agregando salto
            gen.add_jump(falseLvl)
            # Result
            result = Value(str(temp), False, ExpressionType.BOOLEAN, [], [], [])
            result.truelvl.append(trueLvl)
            result.falselvl.append(falseLvl)
            # Etiqueta de salida
            newLabel = gen.new_label()
            for lvl in result.truelvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(1))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
                gen.add_jump(newLabel)
            # Se agregan las etiquetas falsas
            for lvl in result.falselvl:
                gen.new_body_label(lvl)
                # Agregando primitivo
                gen.add_li('t0', str(0))
                gen.add_li('t3', str(temp))
                gen.add_sw('t0', '0(t3)')
            gen.new_body_label(newLabel)
            return result
        
        # OPERACIONES LOGICAS
        elif self.operator == "&&":
            gen.add_operation('and', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.BOOLEAN, [], [], [])
        elif self.operator == "||":
            gen.add_operation('or', 't0', 't1', 't2')
            gen.add_li('t3', str(temp))
            gen.add_sw('t0', '0(t3)')
            return  Value(str(temp), True, ExpressionType.BOOLEAN, [], [], [])

        return None