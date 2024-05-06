import ply.lex as lex
import ply.yacc as yacc

# Expressions imports
from environment.type import ExpressionType
from expression.access import Access
from expression.primitive import Primitive
from expression.operation import Operation
from expression.array import Array
from expression.array_access import ArrayAccess
from expression.call import Call
from expression.break_statement import Break
from expression.continue_statement import Continue
from expression.return_statement import Return
# Instructions imports
from instructions.declaration import Declaration
from instructions.assignment import Assignment
from instructions.if_instruction import If
from instructions.elseif_instruction import Elseif
from instructions.while_instruction import While
from instructions.for_instruction import For
from instructions.switch_instruction import Switch
from instructions.case import Case
from instructions.array_declaration import ArrayDeclaration
from instructions.array_assignment import Arrayassignment
from instructions.push import Push
from instructions.pop import Pop
from instructions.indexof import Indexof
from instructions.length import Length
from instructions.function import Function
from instructions.print import Print
from instructions.parseint import Parseint
from instructions.parsefloat import Parsefloat
from instructions.tostring import Tostring
from instructions.tolowercase import Tolowercase
from instructions.touppercase import Touppercase
from instructions.typeof import Typeof
# Error import
from errors.error import Error

errors = []

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

reserved_words = {
    'var': 'VAR',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'of': 'OF',
    'Object': 'OBJECT',
    'function': 'FUNCTION',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'push': 'PUSH',
    'pop': 'POP',
    'indexOf': 'INDEXOF',
    'length': 'LENGTH',
    'console': 'CONSOLE',
    'log': 'LOG',
    'parseInt': 'PARSEINT',
    'parseFloat': 'PARSEFLOAT',
    'toString': 'TOSTRING',
    'toLowerCase': 'TOLOWERCASE',
    'toUpperCase': 'TOUPPERCASE',
    'typeof': 'TYPEOF',
    'number': 'NUMBER',
    'float': 'FLOAT',
    'string': 'STRING',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'null': 'NULL'
}    

tokens = [
    'ID',
    'INTEGER',
    'DECIMAL',
    'TEXT',
    'CHARACTER',
    'BOOL',
    'LESS',
    'GREATER',
    'EQUAL_TO',
    'NOT_EQUAL_TO',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'AND',
    'OR',
    'NOT',
    'EQUAL',
    'PERIOD',
    'COLON',
    'SEMICOLON',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULUS',
    'ADITION',
    'SUBTRACTION',
    'INCREASE',
    'DECREASE',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_SQ_BRACKET',
    'RIGHT_SQ_BRACKET',
    'LEFT_CURLY_BRACKET',
    'RIGHT_CURLY_BRACKET'
 ] + list(reserved_words.values())

t_LESS = r'<'
t_GREATER = r'>'
t_EQUAL_TO = r'=='
t_NOT_EQUAL_TO = r'!='
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_EQUAL = r'='
t_PERIOD = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
t_ADITION = r'\+='
t_SUBTRACTION = r'-='
t_INCREASE = r'\+\+'
t_DECREASE = r'--'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LEFT_SQ_BRACKET = r'\['
t_RIGHT_SQ_BRACKET = r'\]'
t_LEFT_CURLY_BRACKET = r'\{'
t_RIGHT_CURLY_BRACKET = r'\}'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        floatValue = float(t.value)
        t.value = Primitive(floatValue, ExpressionType.FLOAT, t.lexer.lineno, find_column(t))
    except ValueError:
        print("Error al convertir a decimal %d", t.value)
        t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    return t

def t_INTEGER(t):
    r'\d+'
    try:
        intValue = int(t.value)
        t.value = Primitive(intValue, ExpressionType.NUMBER, t.lexer.lineno, find_column(t))
    except ValueError:
        print("Error al convertir a entero %d", t.value)
        t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    return t

def t_TEXT(t):
    r'\"([^\\\"]|\\.)*\"'
    try:
        strValue = str(t.value)
        t.value = Primitive(strValue[1:-1], ExpressionType.STRING, t.lexer.lineno, find_column(t))
    except ValueError:
        print("Error al convertir string %d", t.value)
        t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    return t

def t_CHARACTER(t):
    r'\'[a-zA-Z0-9]\''
    try:
        charValue = str(t.value)
        charValue = charValue[1:-1]
        if len(charValue) == 1:
            t.value = Primitive(charValue, ExpressionType.CHAR, t.lexer.lineno, find_column(t))
        else:
            errors.append(Error("Sintactico", "Token inesperado '"+t.value+"'.", "Global", t.lexer.lineno, find_column(t)))
            t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    except ValueError:
        print("Error al convertir caracter %d", t.value)
        t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    return t

def t_BOOL(t):
    r'true|false'
    try:
        boolValue = str(t.value)
        t.value = Primitive(True if boolValue == 'true' else False, ExpressionType.BOOLEAN, t.lexer.lineno, find_column(t))
    except ValueError:
        print("Error al convertir booleano %d", t.value)
        t.value = Primitive(None, ExpressionType.NULL, t.lexer.lineno, find_column(t))
    return t

def t_NULL(t):
    r'null'
    nullValue = str(t.value)
    t.value = Primitive("null", ExpressionType.STRING, t.lexer.lineno, find_column(t))
    return t
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value,'ID')
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_comment(t):
    r'//.*'
    pass

def t_comment_multiline(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass 

def t_error(t):
    errors.append(Error("Lexico", "El simbolo '"+t.value[0]+"' no es aceptado en el lenguaje.", "Global", t.lexer.lineno, find_column(t)))
    t.lexer.skip(1)

def find_column(t):
    last_line_break = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_line_break < 0:
        return t.lexpos + 1
    else:
        return t.lexpos - last_line_break

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL_TO', 'NOT_EQUAL_TO'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER_EQUAL', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'DIVIDE', 'MODULUS', 'TIMES'),
    ('right', 'NOT', 'UMINUS' ),
    ('left', 'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'LEFT_SQ_BRACKET', 'RIGHT_SQ_BRACKET'),
)

# START    
def p_start(t):
    '''start : block'''
    t[0] = t[1]

def p_block(t):
    '''block : block instruction
             | instruction '''
    if 2 < len(t):
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruction(t):
    '''instruction : declaration
                   | declaration_array
                   | assignment
                   | if
                   | switch
                   | while
                   | for
                   | function
                   | methods SEMICOLON
                   | call_function SEMICOLON
                   | break
                   | continue
                   | return
                   | print'''
    t[0] = t[1]

def p_declaration_type_value(t):
    '''declaration : symbol_type ID COLON data_type EQUAL expression SEMICOLON'''
    params = get_position(t)
    t[0] = Declaration(t[1], t[2], t[4], t[6], params.line, params.column)

def p_declaration_type(t):
    '''declaration : symbol_type ID COLON data_type SEMICOLON'''
    params = get_position(t)
    t[0] = Declaration(t[1], t[2], t[4], None, params.line, params.column)

def p_declaration_value(t):
    '''declaration : symbol_type ID EQUAL expression SEMICOLON'''
    params = get_position(t)
    t[0] = Declaration(t[1], t[2], None, t[4], params.line, params.column)

def p_assignment(t):
    '''assignment : ID EQUAL expression SEMICOLON
                  | ID ADITION expression SEMICOLON
                  | ID SUBTRACTION expression SEMICOLON''' 
    params = get_position(t)
    t[0] = Assignment(t[1], t[2], t[3], params.line, params.column)

def p_if(t):
    '''if : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET
          | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET ELSE LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET
          | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET else_if_list
          | IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET else_if_list ELSE LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    if len(t) == 8:
        params = get_position(t)
        t[0] = If(t[3], t[6], None, None, params.line, params.column)
    elif len(t) == 12:
        params = get_position(t)
        t[0] = If(t[3], t[6], None, t[10], params.line, params.column)
    elif len(t) == 9:
        params = get_position(t)
        t[0] = If(t[3], t[6], t[8], None, params.line, params.column)
    else:
        params = get_position(t)
        t[0] = If(t[3], t[6], t[8], t[11], params.line, params.column)

def p_else_if_list(t):
    '''else_if_list : else_if_list else_if
                    | else_if'''
    if len(t) > 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_else_if(t):
    '''else_if : ELSE IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    params = get_position(t)
    t[0] = Elseif(t[4], t[7], params.line, params.column)

def p_switch(t):
    '''switch : SWITCH LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET cases RIGHT_CURLY_BRACKET'''
    params = get_position(t)
    t[0] = Switch(t[3], t[6], params.line, params.column)

def p_cases(t):
    '''cases : cases case
             | case'''
    if len(t) > 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_case(t):
    '''case : CASE expression COLON block
            | DEFAULT COLON block'''
    params = get_position(t)
    if t[1] == 'default':
        t[0] = Case(None, t[3], params.line, params.column)
    else:
        t[0] = Case(t[2], t[4], params.line, params.column)

def p_while(t):
    '''while : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    params = get_position(t)
    t[0] = While(t[3], t[6], params.line, params.column)

def p_for(t):
    '''for : FOR LEFT_PARENTHESIS declaration expression SEMICOLON expression RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    params = get_position(t)
    t[0] = For(t[3], t[4], t[6], t[9], params.line, params.column)

def p_for_array(t):
    '''for : FOR LEFT_PARENTHESIS symbol_type ID OF ID RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    params = get_position(t)
    t[0] = For(None, t[4], t[6], t[9], params.line, params.column)

def p_break(t):
    '''break : BREAK SEMICOLON'''
    params = get_position(t)
    t[0] = Break(params.line, params.column)

def p_continue(t):
    '''continue : CONTINUE SEMICOLON'''
    params = get_position(t)
    t[0] = Continue(params.line, params.column)

def p_function(t):
    '''function : FUNCTION ID LEFT_PARENTHESIS RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET
                | FUNCTION ID LEFT_PARENTHESIS RIGHT_PARENTHESIS COLON data_type LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET
                | FUNCTION ID LEFT_PARENTHESIS params RIGHT_PARENTHESIS LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET
                | FUNCTION ID LEFT_PARENTHESIS params RIGHT_PARENTHESIS COLON data_type LEFT_CURLY_BRACKET block RIGHT_CURLY_BRACKET'''
    if len(t) == 8:
        params = get_position(t)
        t[0] = Function(t[2], [], ExpressionType.NULL, t[6], params.line, params.column)
    elif len(t) == 10:
        params = get_position(t)
        t[0] = Function(t[2], [], t[6], t[8], params.line, params.column)
    elif len(t) == 9:
        params = get_position(t)
        t[0] = Function(t[2], t[4], ExpressionType.NULL, t[7], params.line, params.column)
    else:
        params = get_position(t)
        t[0] = Function(t[2], t[4], t[7], t[9], params.line, params.column)
        
def p_params(t):
    '''params : params COMMA param
              | param'''
    params = []
    if len(t) > 2:
        params = t[1] + [t[3]]
    else:
        params.append(t[1])
    t[0] = params

def p_param(t):
    '''param : ID COLON data_type
             | ID COLON data_type LEFT_SQ_BRACKET RIGHT_SQ_BRACKET'''
    if len(t) > 5:
        param = {t[1] : ExpressionType.ARRAY}
        t[0] = param
    else:
        param = {t[1] : t[3]}
        t[0] = param

def p_return(t):
    '''return : RETURN expression SEMICOLON
              | RETURN SEMICOLON'''
    params = get_position(t)
    if len(t) > 3:
        t[0] = Return(t[2], params.line, params.column)
    else:
        t[0] = Return(None, params.line, params.column)

def p_call_function(t):
    '''call_function : ID LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
                     | ID LEFT_PARENTHESIS RIGHT_PARENTHESIS'''
    params = get_position(t)
    if len(t) > 4:
        t[0] = Call(t[1], t[3], params.line, params.column)
    else:
        t[0] = Call(t[1], [], params.line, params.column)

def p_embedded_functions(t):
    '''methods : methods PERIOD name_method LEFT_PARENTHESIS RIGHT_PARENTHESIS
               | methods PERIOD name_method expression
               | methods PERIOD name_method
               | access_array
               | value'''
    params = get_position(t)
    if len(t) > 5:
        if t[3] == "toString":
            t[0] = Tostring(t[1], params.line, params.column)
        elif t[3] == "toLowerCase":
            t[0] = Tolowercase(t[1], params.line, params.column)
        elif t[3] == "toUpperCase":
            t[0] = Touppercase(t[1], params.line, params.column)
        elif t[3] == "pop":
            t[0] = Pop(t[1], params.line, params.column)
    elif len(t) > 4:
        if t[3] == "push":
            t[0] = Push(t[1], t[4], params.line, params.column)
        elif t[3] == "indexOf":
            t[0] = Indexof(t[1], t[4], params.line, params.column)
    elif len(t) > 3:
        if t[3] == "length":
            t[0] = Length(t[1], params.line, params.column)
    else:
        t[0] = t[1]

def p_name_method(t):
    '''name_method : TOSTRING
                   | TOLOWERCASE
                   | TOUPPERCASE
                   | PUSH
                   | POP
                   | INDEXOF
                   | LENGTH'''
    t[0] = t[1]

def p_print(t):
    '''print : CONSOLE PERIOD LOG LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS SEMICOLON'''
    params = get_position(t)
    t[0] = Print(t[5], params.line, params.column)

def p_parseint(t):
    '''methods : PARSEINT expression'''
    params = get_position(t)
    t[0] = Parseint(t[2], params.line, params.column)

def p_parsefloat(t):
    '''methods : PARSEFLOAT expression'''
    params = get_position(t)
    t[0] = Parsefloat(t[2], params.line, params.column)

def p_typeof(t):
    '''methods : TYPEOF expression'''
    params = get_position(t)
    t[0] = Typeof(t[2], params.line, params.column)

def p_declaration_array(t):
    '''declaration_array : symbol_type ID COLON data_type LEFT_SQ_BRACKET RIGHT_SQ_BRACKET EQUAL LEFT_SQ_BRACKET expression_list RIGHT_SQ_BRACKET SEMICOLON'''
    params = get_position(t)
    t[9] = Array(t[9], params.line, params.column)
    t[0] = ArrayDeclaration(t[2], t[4], t[9], params.line, params.column)    

def p_assignment_array(t):
    '''assignment : ID LEFT_SQ_BRACKET expression RIGHT_SQ_BRACKET EQUAL expression SEMICOLON'''
    params = get_position(t)
    t[1] = Access(t[1], params.line, params.column)
    t[0] = Arrayassignment(t[1], [t[3]], t[6], params.line, params.column)

def p_access_array(t):
    '''access_array : ID LEFT_SQ_BRACKET expression RIGHT_SQ_BRACKET'''
    params = get_position(t)
    t[0] = ArrayAccess(t[1], t[3], params.line, params.column)
  
def p_expression_list(t):
    '''expression_list : expression_list COMMA expression
                       | expression '''
    exps = []
    if len(t) > 2:
        exps = t[1] + [t[3]]
    else:
        exps.append(t[1])
    t[0] = exps

def p_expression(t):
    '''expression : expression_unary
                  | expression_binary
                  | expression_group
                  | methods
                  | call_function'''
    t[0] = t[1]

def p_expression_unary(t):
    '''expression_unary : MINUS expression %prec UMINUS
                        | NOT expression
                        | expression INCREASE
                        | expression DECREASE'''
    params = get_position(t)
    if t[1] == '-':
        zero = Primitive(0, ExpressionType.NUMBER, params.line, params.column)
        t[0] = Operation(zero, t[1], t[2], params.line, params.column)
    elif t[1] == '!':
        one = Primitive(1, ExpressionType.NUMBER, params.line, params.column)
        t[0] = Operation(t[2], t[1], one, params.line, params.column)
    elif t[2] == '--' or t[2] == '++':
        t[0] = Operation(t[1], t[2], None, params.line, params.column)

def p_expression_binary(t):
    '''expression_binary : arithmetic
                         | relational
                         | logical'''
    t[0] = t[1]

def p_arithmetic(t):
    '''arithmetic : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULUS expression'''
    params = get_position(t)
    t[0] = Operation(t[1], t[2], t[3], params.line, params.column)

def p_relational(t):
    '''relational : expression LESS expression
                  | expression GREATER expression
                  | expression EQUAL_TO expression
                  | expression NOT_EQUAL_TO expression
                  | expression LESS_EQUAL expression
                  | expression GREATER_EQUAL expression'''
    params = get_position(t)
    t[0] = Operation(t[1], t[2], t[3], params.line, params.column)

def p_logical(t):
    '''logical : expression AND expression
               | expression OR expression'''
    params = get_position(t)
    t[0] = Operation(t[1], t[2], t[3], params.line, params.column)

def p_expression_group(t):
    '''expression_group : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS'''
    t[0] = t[2]

def p_data_symbol(t):
    '''symbol_type : VAR
                   | CONST'''
    t[0] = t[1]

def p_data_type(t):
    '''data_type : NUMBER
                 | FLOAT
                 | STRING
                 | CHAR
                 | BOOLEAN'''
    if t[1] == 'number':
        t[0] = ExpressionType.NUMBER
    elif t[1] == 'float': 
        t[0] = ExpressionType.FLOAT
    elif t[1] == 'string':
        t[0] = ExpressionType.STRING
    elif t[1] == 'char':
        t[0] = ExpressionType.CHAR
    elif t[1] == 'boolean':
        t[0] = ExpressionType.BOOLEAN

def p_value(t):
    '''value : INTEGER
             | DECIMAL
             | TEXT
             | CHARACTER
             | BOOL
             | NULL'''
    t[0] = t[1]

def p_value_id(t):
    '''value : ID'''
    params = get_position(t)
    t[0] = Access(t[1], params.line, params.column)

def p_error(t):
    if t:
        errors.append(Error("Sintactico", "Token inesperado '"+t.value+"'.", "Global", t.lexer.lineno, find_column(t)))
    else:
        errors.append(Error("Sintactico", "Se esperaba un token", "Global", 0, 0))

def get_position(t):
    line = t.lexer.lineno
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)

class Parser:
    def __init__(self):
        pass

    def interpret(self, input):
        errors.clear()
        lexer = lex.lex()
        lexer.ignore_case = False
        parser = yacc.yacc()
        result = parser.parse(input)
        return result
    
    def getErrors(self):
        return errors