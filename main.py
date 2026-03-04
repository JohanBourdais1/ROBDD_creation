import subprocess
from parse_exp import build_robdd_from_expr, to_dot 
from ROBDD_operator import bdd_and, bdd_or, bdd_xor

if __name__ == "__main__":
    expr = "(x+y).!z"
    order = ["x", "y", "z"]
    root = build_robdd_from_expr(expr, order)
    dot = to_dot(root)
    print(dot)
    f = open("robdd.dot", "w")
    f.write(dot)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd.dot", "-o", "robdd.png"],
        check=True
    )