import re

class Expression:
    def __init__(self, expression: str = ""):
        self.expression = self.normalize(expression.upper())

    def normalize(self, expression: str) -> str:
        expression = expression.replace(" ", "")
        expression = expression.replace("·", "*")
        return expression

    def validate(self) -> bool:
        if not re.fullmatch(r"(?:[A-Z]|0|1|'|\(|\)|\+|\*)+", self.expression):
            return False
        # Verifica paréntesis balanceados
        stack = []
        for char in self.expression:
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
