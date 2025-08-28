class Node:
    def copy(self):
        raise NotImplementedError

class Constant(Node):
    def __init__(self, value):
        self.value = 1 if str(value) == '1' else 0

    def __eq__(self, other):
        return isinstance(other, Constant) and self.value == other.value

    def __hash__(self):
        return hash(('Constant', self.value))

    def __str__(self):
        return '1' if self.value == 1 else '0'

    def copy(self):
        return Constant(self.value)

class Variable(Node):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(('Variable', self.name))

    def __str__(self):
        return self.name

    def copy(self):
        return Variable(self.name)

class Not(Node):
    def __init__(self, child):
        self.child = child

    def __eq__(self, other):
        return isinstance(other, Not) and self.child == other.child

    def __hash__(self):
        return hash(('Not', self.child))

    def __str__(self):
        if isinstance(self.child, Variable):
            return f"{self.child}'"
        return f"({self.child})'"

    def copy(self):
        return Not(self.child.copy())

class And(Node):
    def __init__(self, *children):
        operations = []
        for c in children:
            if isinstance(c, And):
                operations.extend(c.children)
            else:
                operations.append(c)

        unique = []
        seen = set()
        for op in operations:
            if op not in seen:
                unique.append(op)
                seen.add(op)

        self.children = sorted(unique, key=lambda x: str(x))

    def __eq__(self, other):
        return isinstance(other, And) and self.children == other.children

    def __hash__(self):
        return hash(('And', tuple(self.children)))

    def __str__(self):
        parts = []
        for c in self.children:
            parts.append(f"({c})" if isinstance(c, Or) else str(c))
        return ''.join(parts)

    def copy(self):
        return And(*[c.copy() for c in self.children])

class Or(Node):
    def __init__(self, *children):
        operations = []
        for c in children:
            if isinstance(c, Or):
                operations.extend(c.children)
            else:
                operations.append(c)
        unique = []
        seen = set()
        for op in operations:
            if op not in seen:
                unique.append(op)
                seen.add(op)
        self.children = sorted(unique, key=lambda x: str(x))

    def __eq__(self, other):
        return isinstance(other, Or) and self.children == other.children

    def __hash__(self):
        return hash(('Or', tuple(self.children)))

    def __str__(self):
        return ' + '.join(str(c) for c in self.children)

    def copy(self):
        return Or(*[c.copy() for c in self.children])

def is_complement(a, b):
    return (isinstance(a, Not) and a.child == b) or (isinstance(b, Not) and b.child == a)

def contains(node, target):
    if node == target:
        return True
    if isinstance(node, (And, Or)):
        return any(contains(c, target) for c in node.children)
    if isinstance(node, Not):
        return contains(node.child, target)
    return False

def to_string(expr):
    return str(expr)

def apply_rules_once(node):
    if isinstance(node, Not):
        new_child, rule = apply_rules_once(node.child)
        if rule:
            return Not(new_child), rule

    if isinstance(node, (And, Or)):
        for idx, c in enumerate(node.children):
            new_c, rule = apply_rules_once(c)
            if rule:
                new_children = list(node.children)
                new_children[idx] = new_c
                node2 = And(*new_children) if isinstance(node, And) else Or(*new_children)
                return node2, rule

    if isinstance(node, Or):
        for i in range(len(node.children)):
            for j in range(i+1, len(node.children)):
                if is_complement(node.children[i], node.children[j]):
                    return Constant(1), "Complemento: A + A' = 1"
    if isinstance(node, And):
        for i in range(len(node.children)):
            for j in range(i+1, len(node.children)):
                if is_complement(node.children[i], node.children[j]):
                    return Constant(0), "Complemento: A · A' = 0"

    if isinstance(node, And):
        if any(isinstance(c, Constant) and c.value == 1 for c in node.children):
            rest = [c for c in node.children if not (isinstance(c, Constant) and c.value == 1)]
            if not rest:
                rest = [Constant(1)]
            return (rest[0] if len(rest) == 1 else And(*rest)), "Identidad: A · 1 = A"
    if isinstance(node, Or):
        if any(isinstance(c, Constant) and c.value == 0 for c in node.children):
            rest = [c for c in node.children if not (isinstance(c, Constant) and c.value == 0)]
            if not rest:
                rest = [Constant(0)]
            return (rest[0] if len(rest) == 1 else Or(*rest)), "Identidad: A + 0 = A"

    if isinstance(node, Or):
        if any(isinstance(c, Constant) and c.value == 1 for c in node.children):
            return Constant(1), "Anulación: A + 1 = 1"
    if isinstance(node, And):
        if any(isinstance(c, Constant) and c.value == 0 for c in node.children):
            return Constant(0), "Anulación: A · 0 = 0"

    if isinstance(node, And):
        ors = [c for c in node.children if isinstance(c, Or)]
        if ors:
            or_node = ors[0]
            others = [c for c in node.children if c is not or_node]
            new_terms = [And(*(others + [t])) for t in or_node.children]
            return Or(*new_terms), "Distributiva: A(B+C)=AB+AC"

    if isinstance(node, Or):
        cs = node.children
        for i in range(len(cs)):
            for j in range(i+1, len(cs)):
                a, b = cs[i], cs[j]
                if isinstance(a, And) and isinstance(b, And):
                    common = list(set(a.children).intersection(set(b.children)))
                    if common:
                        f = common[0]
                        rest_a = [x for x in a.children if x != f]
                        rest_b = [x for x in b.children if x != f]
                        left = And(*rest_a) if len(rest_a) > 1 else (rest_a[0] if rest_a else Constant(1))
                        right = And(*rest_b) if len(rest_b) > 1 else (rest_b[0] if rest_b else Constant(1))
                        new_node = And(f, Or(left, right))
                        others = [cs[k] for k in range(len(cs)) if k not in (i, j)]
                        return (Or(new_node, *others) if others else new_node), "Factorización: AB+AC=A(B+C)"

    if isinstance(node, Or):
        cs = node.children
        for i in range(len(cs)):
            for j in range(len(cs)):
                if i == j:
                    continue
                x, y = cs[i], cs[j]
                if isinstance(y, And) and x in y.children:
                    others = [ch for ch in y.children if ch != x]
                    And_ = others[0] if len(others) == 1 else And(*others)
                    new_node = And(x, Or(Constant(1), And_))
                    remaining = [cs[k] for k in range(len(cs)) if k not in (i, j)]
                    return (Or(new_node, *remaining) if remaining else new_node, "Factorización: A + A·B = A(1+B)")

    if isinstance(node, Or):
        cs = node.children
        for i in range(len(cs)):
            for j in range(len(cs)):
                if i == j:
                    continue
                x, y = cs[i], cs[j]
                if isinstance(y, And) and x in y.children:
                    return x.copy(), "Absorción: A + A·B = A"
    if isinstance(node, And):
        cs = node.children
        for i in range(len(cs)):
            for j in range(len(cs)):
                if i == j:
                    continue
                x, y = cs[i], cs[j]
                if isinstance(y, Or) and x in y.children:
                    return x.copy(), "Absorción: A(A+B) = A"

    if isinstance(node, Not):
        c = node.child
        if isinstance(c, And):
            return Or(*[Not(k) for k in c.children]), "De Morgan: ~(AB)=A'+B'"
        if isinstance(c, Or):
            return And(*[Not(k) for k in c.children]), "De Morgan: ~(A+B)=A'B'"

    return node, None

def simplify_with_steps(expr):
    steps = []
    current = expr
    steps.append(("Expresión inicial", to_string(current)))
    MAX_STEPS = 60
    for _ in range(MAX_STEPS):
        new_node, rule = apply_rules_once(current)
        if not rule:
            break
        steps.append((rule, to_string(new_node)))
        current = new_node
    return steps, current
