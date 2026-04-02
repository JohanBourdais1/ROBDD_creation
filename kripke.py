import re
from collections import deque
import time

class Kripke:
    def __init__(self):
        self.states = set()
        self.initial_state = None
        self.labels = {}
        self.transitions = {}

"""Parse a Kripke structure from a file."""
def parse_kripke(filename):
    k = Kripke()

    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("states:"):
            states = line.split(":")[1].split()
            k.states = set(states)
            for s in states:
                k.labels[s] = set()
                k.transitions[s] = []

        elif line.startswith("init:"):
            k.initial_state = line.split(":")[1].strip()

        elif line == "labels:":
            i += 1
            while i < len(lines) and not lines[i].endswith(":"):
                s, props = lines[i].split(":")
                k.labels[s.strip()] = set(props.split())
                i += 1
            continue

        elif line == "transitions:":
            i += 1
            while i < len(lines) and not lines[i].endswith(":"):
                s, succ = lines[i].split(":")
                k.transitions[s.strip()] = succ.split()
                i += 1
            continue

        i += 1

    return k


class Formula:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left is None and self.right is None:
            return self.op
        if self.right is None:
            return f"({self.op} {self.left})"
        return f"({self.left} {self.op} {self.right})"


"""Get all the different token types in a CTL formula."""
def tokenize(s):
    return re.findall(
        r'EX|AX|EF|AF|EG|AG|E|A|U|!|\+|\.|=>|\(|\)|\[|\]|true|false|[a-zA-Z_][a-zA-Z0-9_]*',
        s
    )


"""Parse a CTL formula into an AST (Abstract Syntax Tree)."""
def parse_ctl(s):
    tokens = tokenize(s)
    return parse_implication(tokens)


def parse_implication(tokens):
    left = parse_or(tokens)
    while tokens and tokens[0] == "=>":
        tokens.pop(0)
        right = parse_or(tokens)
        left = Formula("=>", left, right)
    return left


def parse_or(tokens):
    left = parse_and(tokens)
    while tokens and tokens[0] == "+":
        tokens.pop(0)
        right = parse_and(tokens)
        left = Formula("+", left, right)
    return left


def parse_and(tokens):
    left = parse_unary(tokens)
    while tokens and tokens[0] == ".":
        tokens.pop(0)
        right = parse_unary(tokens)
        left = Formula(".", left, right)
    return left


def parse_unary(tokens):
    tok = tokens.pop(0)

    if tok == "!":
        return Formula("!", parse_unary(tokens))

    if tok in ["EX", "AX", "EF", "AF", "EG", "AG"]:
        return Formula(tok, parse_unary(tokens))

    if tok == "(":
        node = parse_implication(tokens)
        tokens.pop(0)
        return node

    if tok == "true" or tok == "false":
        return Formula(tok)

    if tok == "E" or tok == "A":
        tokens.pop(0)
        left = parse_implication(tokens)
        tokens.pop(0)
        right = parse_implication(tokens)
        tokens.pop(0)
        return Formula(tok + "U", left, right)

    return Formula(tok)

def sat(formula, k):
    op = formula.op

    if op == "true":
        return set(k.states)

    if op == "false":
        return set()

    if op not in ["!", ".", "+", "=>", "EX", "AX", "EF", "EG", "EU", "AF", "AG", "AU"]:
        return {s for s in k.states if op in k.labels[s]}

    if op == "!":
        return k.states - sat(formula.left, k)

    if op == ".":
        return sat(formula.left, k) & sat(formula.right, k)

    if op == "+":
        return sat(formula.left, k) | sat(formula.right, k)

    if op == "=>":
        left = sat(formula.left, k)
        right = sat(formula.right, k)
        return (k.states - left) | right

    if op == "EX":
        target = sat(formula.left, k)
        return {s for s in k.states if any(t in target for t in k.transitions[s])}

    if op == "AX":
        target = sat(formula.left, k)
        res = set()
        for s in k.states:
            succ = k.transitions[s]
            if not succ or all(t in target for t in succ):
                res.add(s)
        return res

    if op == "EF":
        target = sat(formula.left, k)
        res = set(target)

        changed = True
        while changed:
            changed = False
            for s in k.states:
                if s not in res and any(t in res for t in k.transitions[s]):
                    res.add(s)
                    changed = True
        return res

    if op == "EG":
        res = sat(formula.left, k)

        changed = True
        while changed:
            changed = False
            for s in list(res):
                if not any(t in res for t in k.transitions[s]):
                    res.remove(s)
                    changed = True
        return res

    if op == "EU":
        phi = sat(formula.left, k)
        psi = sat(formula.right, k)

        res = set(psi)

        changed = True
        while changed:
            changed = False
            for s in k.states:
                if s not in res and s in phi:
                    if any(t in res for t in k.transitions[s]):
                        res.add(s)
                        changed = True
        return res

    if op == "AF":
        return k.states - sat(Formula("EG", Formula("!", formula.left)), k)

    if op == "AG":
        return k.states - sat(Formula("EF", Formula("!", formula.left)), k)

    return set()

def print_path(path, k):
    for s in path:
        print(s, "labels:", k.labels[s])

def counterexample_AG(formula, k):

    bad = sat(Formula("!", formula.left), k)

    visited = set()
    queue = deque([(k.initial_state, [k.initial_state])])

    while queue:
        state, path = queue.popleft()

        if state in bad:
            return path

        for succ in k.transitions[state]:
            if succ not in visited:
                visited.add(succ)
                queue.append((succ, path + [succ]))

    return None

def counterexample_EF(formula, k):

    target = sat(formula.left, k)

    visited = set()
    queue = deque([(k.initial_state, [k.initial_state])])

    while queue:
        state, path = queue.popleft()

        if state in target:
            return path

        for succ in k.transitions[state]:
            if succ not in visited:
                visited.add(succ)
                queue.append((succ, path + [succ]))

    return None

def counterexample_EU(formula, k):

    phi = sat(formula.left, k)
    psi = sat(formula.right, k)

    visited = set()
    queue = deque([(k.initial_state, [k.initial_state])])

    while queue:
        state, path = queue.popleft()

        if state in psi:
            return path

        if state not in phi:
            return path

        for succ in k.transitions[state]:
            if succ not in visited:
                visited.add(succ)
                queue.append((succ, path + [succ]))

    return None

def counterexample(formula, k):

    good = sat(formula, k)

    visited = {k.initial_state}
    queue = deque([(k.initial_state, [k.initial_state])])

    while queue:
        state, path = queue.popleft()

        # dès qu’on sort de Sat(φ)
        if state not in good:
            return path

        for succ in k.transitions[state]:
            if succ not in visited:
                visited.add(succ)
                queue.append((succ, path + [succ]))

    return None

if __name__ == "__main__":

    for i in ["kripke1.txt", "kripke2.txt"]:
        # Charge le modèle de kirpke
        k = parse_kripke(i)
        print("States:", k.states)
        print("Initial:", k.initial_state)
        print("Labels:", k.labels)
        print("Transitions:", k.transitions)
        print("-" * 40)

        # les formules à tester
        formulas = [
            "EF p1",
            "AF p1",
            "EG p0",
            "AG p0",
            "E[p0 U p1]",
            "EX p0",
            "AX p0",
            "AX p2",
            "!(EG p2)",
            "EF (p0 + p1)",
            "AF (p1 . p0)"
        ]

        # Parcourir les formules
        for s in formulas:
            f = parse_ctl(s)
            print("Formula:", s)

            start = time.time()
            result = sat(f, k)
            end = time.time()

            print("Sat(states):", result)
            print("Time: {:.6f}s".format(end - start))

            if k.initial_state in result:
                print("Initial state satisfies the formula")
            else:
                print("Initial state does NOT satisfy the formula")

                # Générer un contre-exemple simple
                if s.startswith("AG"):
                    path = counterexample_AG(f, k)
                    print(f"Counterexample path (AG violation): {path}")
                elif s.startswith("EF"):
                    path = counterexample_EF(f, k)
                    print(f"Counterexample path (EF failure): {path}")
                elif s.startswith("E["):
                    path = counterexample_EU(f, k)
                    print(f"Counterexample path (EU failure): {path}")
                else:
                    path = counterexample(f, k)
                    if path != None:
                        print(f"Counterexample path : {path}")
                    else:
                        print("No counterexample implemented for this operator")

                if path:
                    print_path(path, k)

            print("-" * 40)

        print("\n\n")
    


    for i in ["kripke3.txt"]:
        # Charge le modèle de kirpke
        k = parse_kripke(i)
        print("States:", k.states)
        print("Initial:", k.initial_state)
        print("Labels:", k.labels)
        print("Transitions:", k.transitions)
        print("-" * 40)

        # les formules à tester
        formulas = [
            "AG(p0=>EFp3)",
            "EF(p1=>EGp2)"
        ]

        # Parcourir les formules
        for s in formulas:
            f = parse_ctl(s)
            print("Formula:", s)

            start = time.time()
            result = sat(f, k)
            end = time.time()

            print("Sat(states):", result)
            print("Time: {:.6f}s".format(end - start))

            if k.initial_state in result:
                print("Initial state satisfies the formula")
            else:
                print("Initial state does NOT satisfy the formula")

                # Générer un contre-exemple simple
                if s.startswith("AG"):
                    path = counterexample_AG(f, k)
                    print(f"Counterexample path (AG violation): {path}")
                elif s.startswith("EF"):
                    path = counterexample_EF(f, k)
                    print(f"Counterexample path (EF failure): {path}")
                elif s.startswith("E["):
                    path = counterexample_EU(f, k)
                    print(f"Counterexample path (EU failure): {path}")
                else:
                    path = counterexample(f, k)
                    if path != None:
                        print(f"Counterexample path : {path}")
                    else:
                        print("No counterexample implemented for this operator")


                if path:
                    print_path(path, k)

            print("-" * 40)

        print("\n\n")
