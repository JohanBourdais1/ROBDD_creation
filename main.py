import subprocess
from parse_exp import build_robdd_from_expr, to_dot, ROBDD
from ROBDD_operator import bdd_and, bdd_or, bdd_xor

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
    expra="a.b"
    exprb="c.d"
    exprc="e.f"
    exprd="g.h"
    expre="i.j"
    order1 = ["a","b","c","d","e","f","g","h","i","j"]
    order2 = ["a","c","e","g","i","b","d","f","h","j"]
    robdd1 = ROBDD(order1)
    robdd2 = ROBDD(order2)
    ra1 = build_robdd_from_expr(expra,order1)
    ra2 = build_robdd_from_expr(expra,order2)
    rb1 = build_robdd_from_expr(exprb,order1)
    rb2 = build_robdd_from_expr(exprb,order2)
    rc1 = build_robdd_from_expr(exprc,order1)
    rc2 = build_robdd_from_expr(exprc,order2)
    rd1 = build_robdd_from_expr(exprd,order1)
    rd2 = build_robdd_from_expr(exprd,order2)
    re1 = build_robdd_from_expr(expre,order1)
    re2 = build_robdd_from_expr(expre,order2)
    res1 = bdd_xor(bdd_xor(bdd_xor(bdd_xor(ra1,rb1,robdd1),rc1,robdd1),rd1,robdd1),re1,robdd1)
    res2 = bdd_xor(bdd_xor(bdd_xor(bdd_xor(ra2,rb2,robdd2),rc2,robdd2),rd2,robdd2),re2,robdd2)
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
    
    expra="!a*b"
    exprb="!c*d"
    exprc="!e*f"
    exprd="!g*h"
    expre="!i*j"
    order1 = ["a","b","c","d","e","f","g","h","i","j"]
    order2 = ["a","c","e","g","i","b","d","f","h","j"]
    robdd1 = ROBDD(order1)
    robdd2 = ROBDD(order2)
    ra1 = build_robdd_from_expr(expra,order1)
    ra2 = build_robdd_from_expr(expra,order2)
    rb1 = build_robdd_from_expr(exprb,order1)
    rb2 = build_robdd_from_expr(exprb,order2)
    rc1 = build_robdd_from_expr(exprc,order1)
    rc2 = build_robdd_from_expr(exprc,order2)
    rd1 = build_robdd_from_expr(exprd,order1)
    rd2 = build_robdd_from_expr(exprd,order2)
    re1 = build_robdd_from_expr(expre,order1)
    re2 = build_robdd_from_expr(expre,order2)
    res1 = bdd_and(bdd_and(bdd_and(bdd_and(ra1,rb1,robdd1),rc1,robdd1),rd1,robdd1),re1,robdd1)
    res2 = bdd_and(bdd_and(bdd_and(bdd_and(ra2,rb2,robdd2),rc2,robdd2),rd2,robdd2),re2,robdd2)
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
    print("Regle sur le nom du fichier:\n robdd\"numéro d'exercice\"\"numéro d'expression\".\n Exemple: robdd241 <=> expression1 de l'exercice 2.4.")