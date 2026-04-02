import re

class Node:
    __slots__ = ("var", "left", "right", "id")
    def __init__(self, var, left, right, i):
        self.var = var
        self.left = left
        self.right = right
        self.id = i

ZERO = Node(None, None, None, 0)
ONE = Node(None, None, None, 1)


class ROBDD:
    def __init__(self, order):
        self.order = order
        self.var_index = {v: i for i, v in enumerate(order)}
        self.unique = {}
        self.next_id = 2

    def mk(self, var, left, right):
        if left == right:
            return left
        key = (var, left.id, right.id)
        if key in self.unique:
            return self.unique[key]
        n = Node(var, left, right, self.next_id)
        self.next_id += 1
        self.unique[key] = n
        return n

    def build(self, expr, env, vars_left):
        if not vars_left:
            return ONE if eval_expr(expr, env) else ZERO
        v = vars_left[0]
        env[v] = 0
        left = self.build(expr, env, vars_left[1:])
        env[v] = 1
        right = self.build(expr, env, vars_left[1:])
        return self.mk(v, left, right)

"""Get all the different tokens in a boolean expression."""
def tokenize(s):
    return re.findall(r'[a-zA-Z]\w*|[()+.*!]', s)

"""Parse a boolean expression in the form of an AST (Abstract Syntax Tree)."""
def parse(tokens):
    def parse_expr(i):
        node, i = parse_term(i)
        while i < len(tokens) and tokens[i] == '+':
            rhs, i = parse_term(i + 1)
            node = ('+', node, rhs)
        return node, i

    def parse_term(i):
        node, i = parse_factor(i)
        while i < len(tokens) and tokens[i] in ('.', '*'):
            op = tokens[i]
            rhs, i = parse_factor(i + 1)
            node = (op, node, rhs)
        return node, i

    def parse_factor(i):
        if tokens[i] == '!':
            node, i = parse_factor(i + 1)
            return ('!', node), i
        if tokens[i] == '(':
            node, i = parse_expr(i + 1)
            return node, i + 1
        return tokens[i], i + 1

    ast, _ = parse_expr(0)
    return ast

def eval_expr(ast, env):
    if ast == '0':
        return 0
    if ast == '1':
        return 1
    if isinstance(ast, str):
        return env[ast]
    if ast[0] == '!':
        return 1 - eval_expr(ast[1], env)
    a = eval_expr(ast[1], env)
    b = eval_expr(ast[2], env)
    if ast[0] == '+':
        return a | b
    if ast[0] == '.':
        return a & b
    if ast[0] == '*':
        return a ^ b


"""Print a ROBDD in DOT format for visualization."""
def to_dot(root):
    lines = ["digraph ROBDD {", "rankdir=TB;"]
    seen = set()

    def visit(n):
        if n.id in seen:
            return
        seen.add(n.id)

        if n == ZERO:
            lines.append('0 [shape=box,label="0"];')
            return
        if n == ONE:
            lines.append('1 [shape=box,label="1"];')
            return

        lines.append(f'{n.id} [label="{n.var}"];')
        lines.append(f'{n.id} -> {n.left.id} [label="0"];')
        lines.append(f'{n.id} -> {n.right.id} [label="1"];')
        

        visit(n.left)
        visit(n.right)

    visit(root)
    lines.append("}")
    return "\n".join(lines)

def heuristique(ast, order):
    if isinstance(ast, str):
        order.append(ast)
    else :
        if len(ast) > 1 :
            order = heuristique(ast[1],order)
            if len(ast) > 2:
                order = heuristique(ast[2],order)
    return order

""""Build a ROBDD from a boolean expression string and variable order."""
def build_robdd_from_expr(expr, order =[]):
    tokens = tokenize(expr)
    ast = parse(tokens)
    if order == [] :
        order = heuristique(ast,order)
    robdd = ROBDD(order)
    root = robdd.build(ast, {}, order)
    return root
