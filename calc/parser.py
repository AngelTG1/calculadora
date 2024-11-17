import ply.lex as lex
import ply.yacc as yacc

# Definir tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Reglas de los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Árbol sintáctico
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []

    def to_dict(self):
        """Convierte el árbol en un diccionario para facilitar la visualización en JSON."""
        return {
            "value": self.value,
            "children": [child.to_dict() for child in self.children]
        }

# Reglas de la gramática
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = Node('+', [p[1], p[3]])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = Node('-', [p[1], p[3]])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_multiply(p):
    'term : term MULTIPLY factor'
    p[0] = Node('*', [p[1], p[3]])

def p_term_divide(p):
    'term : term DIVIDE factor'
    if p[3].value == 0:
        raise ZeroDivisionError("Division by zero")
    p[0] = Node('/', [p[1], p[3]])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = Node(p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    raise SyntaxError("Syntax error in input")

parser = yacc.yacc()

def parse_expression(expression):
    """Evalúa la expresión y devuelve el árbol sintáctico."""
    return parser.parse(expression)
