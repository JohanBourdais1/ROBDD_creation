import subprocess
from parse_exp import build_robdd_from_expr, to_dot, ROBDD
from ROBDD_operator import bdd_and, bdd_or, bdd_xor

if __name__ == "__main__":
    exprA = "z+(x.y)"
    exprB = "y.z"
    order = ["x", "y", "z"]
    robdd = ROBDD(order)
    rootA = build_robdd_from_expr(exprA, order)
    rootB = build_robdd_from_expr(exprB, order)
    root_and = bdd_and(rootB,rootA,robdd)
    root_or = bdd_or(rootA,rootB,robdd)
    root_xor = bdd_xor(rootA,rootB,robdd)
    dot = to_dot(root_or)
    print(dot)
    f = open("robdd.dot", "w")
    f.write(dot)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd.dot", "-o", "robdd.png"],
        check=True
    )