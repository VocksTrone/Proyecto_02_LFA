import re

class Expression:
    def __init__(self, expression: str = ""):
        self.expression = self.normalize(expression.upper())

    def normalize(self, expression: str) -> str:
        expression = expression.replace(" ", "")
        expression = expression.replace("·", "*")
        expression = expression.replace("+", "+")
        return expression

    def validate(self) -> bool:
        expression = self.expression
        if not re.fullmatch(r"[A-Z0-9\+\*\(\)']+", expression):
            return False
        stack = []
        for char in expression:
            if char == "(":
                stack.append(char)
            elif char == ")":
                if not stack:
                    return False
                stack.pop()
        return not stack

    def get(self) -> str:
        return self.expression

    def set(self, expression: str):
        self.expression = self.normalize(expression.upper())