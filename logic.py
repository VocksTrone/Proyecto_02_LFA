import re

class Logic:
    def __init__(self, expression: str):
        self.original = expression
        self.expression = expression
        self.steps = []

    def apply_laws(self):
        change = True
        while change:
            change = False
            rules = [
                (r"([A-Z])\+0", r"\1", "Identidad"),
                (r"0\+([A-Z])", r"\1", "Identidad"),
                (r"([A-Z])\*1", r"\1", "Identidad"),
                (r"1\*([A-Z])", r"\1", "Identidad"),

                (r"([A-Z])\+1", "1", "Anulación"),
                (r"1\+([A-Z])", "1", "Anulación"),
                (r"([A-Z])\*0", "0", "Anulación"),
                (r"0\*([A-Z])", "0", "Anulación"),

                (r"([A-Z])\+(\1')", "1", "Complementario"),
                (r"([A-Z])\*(\1')", "0", "Complementario"),

                (r"([A-Z])\+\1", r"\1", "Idempotencia"),
                (r"([A-Z])\*\1", r"\1", "Idempotencia"),

                (r"([A-Z])''", r"\1", "Doble Negación"),

                (r"([A-Z])\+([A-Z])\*\1", r"\1", "Absorción"),
                (r"([A-Z])\*([A-Z])\+\1", r"\1", "Absorción"),

                (r"([A-Z])\*([A-Z])\+([A-Z])'\*([A-Z])", r"\2", "Consenso"),
            ]
            for pattern, replace, law in rules:
                new = re.sub(pattern, replace, self.expression)
                if new != self.expression:
                    self.steps.append((self.expression, law, new))
                    self.expression = new
                    change = True
                    break
        return self.expression

    def show_steps(self):
        if not self.steps:
            print("Expresión Simplificada al Mínimo")
        else:
            for before, law, after in self.steps:
                print(f"{before} --- {law} --- {after}")

    def final_result(self) -> str:
        return self.expression