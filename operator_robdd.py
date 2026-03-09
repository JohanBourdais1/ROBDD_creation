from parse_exp import ZERO, ONE

def operator_function(rootA, rootB, ope, robdd, save=None):
    if save is None:
        save={}
        
    if (ope, rootA.id, rootB.id) in save:
        return save[(ope, rootA.id, rootB.id)]
    
    if rootA in (ZERO, ONE) and rootB in (ZERO, ONE):
        a = 1 if rootA == ONE else 0
        b = 1 if rootB == ONE else 0
        if ope == "and":
            r = a & b
        elif ope == "or":
            r = a | b
        elif ope == "xor":
            r = a ^ b
        res = ONE if r else ZERO
        save[(ope, rootA.id, rootB.id)] = res
        return res
    
    if rootA in (ZERO, ONE):
        var = rootB.var
    elif rootB in (ZERO, ONE):
        var = rootA.var
    else:
        if robdd.var_index[rootA.var] <= robdd.var_index[rootB.var]:
            var = rootA.var
        else:
            var = rootB.var
    if rootA not in (ZERO, ONE) and rootA.var == var:
        leftA = rootA.left
        rightA = rootA.right
    else:
        leftA = rightA = rootA
    if rootB not in (ZERO, ONE) and rootB.var == var:
        leftB = rootB.left
        rightB = rootB.right
    else:
        leftB = rightB = rootB
        
    left = operator_function(leftA, leftB, ope, robdd, save)
    right = operator_function(rightA, rightB, ope, robdd, save)
    res = robdd.mk(var, left, right)
    save[(ope, rootA.id, rootB.id)] = res
    return res

def bdd_and(a, b, robdd):
    return operator_function(a, b, "and", robdd)

def bdd_or(a, b, robdd):
    return operator_function(a, b, "or", robdd)

def bdd_xor(a, b, robdd):
    return operator_function(a, b, "xor", robdd)