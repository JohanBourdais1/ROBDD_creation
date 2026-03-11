import subprocess
import time
from parse_exp import build_robdd_from_expr, to_dot, ROBDD
from operator_robdd import bdd_and, bdd_or, bdd_xor

def count_nodes(root):
    visited = set()
    def visit(node):
        if node.id in visited:
            return
        visited.add(node.id)
        if node.var is None:
            return
        visit(node.left)
        visit(node.right)
    visit(root)
    return len(visited)

if __name__ == "__main__":
    """2.4 Vérification d'équivalence
    """
    print("2.4 Vérification d'équivalence\n")
    exprA = "z+(x.y)"
    exprB = "(x.y)+z"
    order = ["x", "y", "z"]
    robdd = ROBDD(order)
    rootA = build_robdd_from_expr(exprA, order)
    rootB = build_robdd_from_expr(exprB, order)
    dot241 = to_dot(rootA)
    print("z+(x.y)")
    print(dot241)
    f = open("robdd241.dot", "w")
    f.write(dot241)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd241.dot", "-o", "robdd241.png"],
        check=True
    )
    print("\n")
    dot242 = to_dot(rootB)
    print("(x.y)+z")
    print(dot242)
    f = open("robdd242.dot", "w")
    f.write(dot242)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd242.dot", "-o", "robdd242.png"],
        check=True
    )
    print("\n")
    
    """2.5 Applications
    """
    print("2.5 Applications\n")
    expra="x1.y1"
    exprb="x2.y2"
    exprc="x3.y3"
    exprd="x4.y4"
    expre="x5.y5"
    order1 = ["x1","y1","x2","y2","x3","y3","x4","y4","x5","y5"]
    order2 = ["x1","x2","x3","x4","x5","y1","y2","y3","y4","y5"]
    robdd1 = ROBDD(order1)
    robdd2 = ROBDD(order2)
    start = time.time()
    ra1 = build_robdd_from_expr(expra,order1)
    rb1 = build_robdd_from_expr(exprb,order1)
    rc1 = build_robdd_from_expr(exprc,order1)
    rd1 = build_robdd_from_expr(exprd,order1)
    re1 = build_robdd_from_expr(expre,order1)
    res1 = bdd_xor(bdd_xor(bdd_xor(bdd_xor(ra1,rb1,robdd1),rc1,robdd1),rd1,robdd1),re1,robdd1)
    time1 = time.time()-start
    start = time.time()
    ra2 = build_robdd_from_expr(expra,order2)
    rb2 = build_robdd_from_expr(exprb,order2)
    rc2 = build_robdd_from_expr(exprc,order2)
    rd2 = build_robdd_from_expr(exprd,order2)
    re2 = build_robdd_from_expr(expre,order2)
    res2 = bdd_xor(bdd_xor(bdd_xor(bdd_xor(ra2,rb2,robdd2),rc2,robdd2),rd2,robdd2),re2,robdd2)
    time2 = time.time()-start
    cd_node1 = count_nodes(res1)
    cd_node2 = count_nodes(res2)
    dot251 = to_dot(res1)
    print("2.5.1")
    print(dot251)
    f = open("robdd251.dot", "w")
    f.write(dot251)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd251.dot", "-o", "robdd251.png"],
        check=True
    )
    print("\n")
    dot252 = to_dot(res2)
    print("2.5.2")
    print(dot252)
    f = open("robdd252.dot", "w")
    f.write(dot252)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd252.dot", "-o", "robdd252.png"],
        check=True
    )
    print("\n")
    
    expra="!x1*y1"
    exprb="!x2*y2"
    exprc="!x3*y3"
    exprd="!x4*y4"
    expre="!x5*y5"
    order1 = ["x1","y1","x2","y2","x3","y3","x4","y4","x5","y5"]
    order2 = ["x1","x2","x3","x4","x5","y1","y2","y3","y4","y5"]
    robdd1 = ROBDD(order1)
    robdd2 = ROBDD(order2)
    start = time.time()
    ra1 = build_robdd_from_expr(expra,order1)
    rb1 = build_robdd_from_expr(exprb,order1)
    rc1 = build_robdd_from_expr(exprc,order1)
    rd1 = build_robdd_from_expr(exprd,order1)
    re1 = build_robdd_from_expr(expre,order1)
    res1 = bdd_and(bdd_and(bdd_and(bdd_and(ra1,rb1,robdd1),rc1,robdd1),rd1,robdd1),re1,robdd1)
    time3 = time.time()-start
    start = time.time()
    ra2 = build_robdd_from_expr(expra,order2)
    rb2 = build_robdd_from_expr(exprb,order2)
    rc2 = build_robdd_from_expr(exprc,order2)
    rd2 = build_robdd_from_expr(exprd,order2)
    re2 = build_robdd_from_expr(expre,order2)
    res2 = bdd_and(bdd_and(bdd_and(bdd_and(ra2,rb2,robdd2),rc2,robdd2),rd2,robdd2),re2,robdd2)
    time4 = time.time()-start
    cd_node3 = count_nodes(res1)
    cd_node4 = count_nodes(res2)
    dot253 = to_dot(res1)
    print("2.5.3")
    print(dot253)
    f = open("robdd253.dot", "w")
    f.write(dot253)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd253.dot", "-o", "robdd253.png"],
        check=True
    )
    print("\n")
    dot254 = to_dot(res2)
    print("2.5.4")
    print(dot254)
    f = open("robdd254.dot", "w")
    f.write(dot254)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robdd254.dot", "-o", "robdd254.png"],
        check=True
    )
    print("\n")
    print("Tableau exercice 2.5\n")
    print(f"{'num expr':<10} {'nb_noeud':<10} {'temps':<10}")
    print("-"*30)
    print(f"{'2.5.1':<10} {cd_node1:<10} {time1:<10.6f}")
    print(f"{'2.5.2':<10} {cd_node2:<10} {time2:<10.6f}")
    print(f"{'2.5.3':<10} {cd_node3:<10} {time3:<10.6f}")
    print(f"{'2.5.4':<10} {cd_node4:<10} {time4:<10.6f}")
    print("\n")

    expr="(x1.y1)*(x2.y2)*(x3.y3)*(x4.y4)*(x5.y5)"
    order1 = ["x1","y1","x2","y2","x3","y3","x4","y4","x5","y5"]
    robdd1 = ROBDD(order1)
    res = build_robdd_from_expr(expr,order1)
    dottest = to_dot(res)
    print("test")
    print(dottest)
    f = open("robddtest.dot", "w")
    f.write(dottest)
    f.close()
    subprocess.run(
        ["dot", "-Tpng", "robddtest.dot", "-o", "robddtest.png"],
        check=True
    )
    print("\n")
    print("Regle sur le nom du fichier:\n robdd\"numéro d'exercice\"\"numéro d'expression\".\n Exemple: robdd241 <=> expression1 de l'exercice 2.4.")