from logic import Constant, Variable, Not, And, Or

class Lexer:
    def __init__(self, text):
        text = text.replace('’', "'").replace('´', "'")
        self.text = ''.join(ch for ch in text if ch not in [' ', '\t', '\n'])
        self.index = 0

    def peek(self):
        return self.text[self.index] if self.index < len(self.text) else None

    def get(self):
        ch = self.peek()
        if ch is not None:
            self.index += 1
        return ch

def parse_expression(text):
    lx = Lexer(text)
    node = parse_or(lx)
    if lx.peek() is not None:
        raise ValueError(f"Entrada inesperada en posición {lx.index}: '{lx.peek()}'")
    return node

def parse_or(lx):
    left = parse_and(lx)
    while lx.peek() == '+':
        lx.get()
        right = parse_and(lx)
        left = Or(left, right)
    return left

def parse_and(lx):
    left = parse_factor(lx)
    while True:
        ch = lx.peek()
        if ch is None or ch in [')', '+']:
            break
        if ch == '*':
            lx.get()
            right = parse_factor(lx)
            left = And(left, right)
        else:
            if ch.isalpha() or ch in ['(', '0', '1', '~', "'"]:
                right = parse_factor(lx)
                left = And(left, right)
            else:
                break
    return left

def parse_factor(lx):
    ch = lx.peek()
    if ch is None:
        raise ValueError("Expresión incompleta.")

    if ch == '(':
        lx.get()
        node = parse_or(lx)
        if lx.get() != ')':
            raise ValueError("Falta cerrar paréntesis.")
        if lx.peek() == "'":
            lx.get()
            return Not(node)
        return node

    if ch in ['0', '1']:
        lx.get()
        node = Constant(int(ch))
        if lx.peek() == "'":
            lx.get()
            return Not(node)
        return node

    if ch in ['~', "'"]:
        lx.get()
        return Not(parse_factor(lx))

    if ch.isalpha():
        name = lx.get()
        node = Variable(name.upper())
        if lx.peek() == "'":
            lx.get()
            node = Not(node)
        return node

    raise ValueError(f"Carácter inesperado: '{ch}' en posición {lx.index}")
