# ROBDD & Model Checking CTL

# Partie 1 — ROBDD

## Fichiers
- main.py
- parse_exp.py
- operator_robdd.py

### Parsing
Expressions booléennes avec :
- + (OR)
- . (AND)
- * (XOR)
- ! (NOT)

### Opérations entre deux ROBDD
- bdd_and(root1, root2, robdd)
- bdd_or(root1, root2, robdd)
- bdd_xor(root1, root2, robdd)
- retrourne la racine du robdd résultant

### Visualisation
- Export Graphviz (.dot)
- Génération d’images (.png)

### Règle de nommage
- robdd + "numéro d'exercice" + "numéro d'expression"
- Exemple: robdd241 <=> expression1 de l'exercice 2.4
---

# Partie 2 — Kripke & CTL

## Fichiers
- kripke.py
- kripke1.txt
- kripke2.txt
- kripke3.txt

### Structure de Kripke
- états
- état initial
- labels
- transitions

### CTL supporté
- Booléens : !, ., +, =>
- Temporels : EX, AX, EF, AF, EG, AG, EU, AU

### Model Checking
- Fonction sat(formula, k)
- Retourne les états satisfaisant la formule

### Contre-exemples
- Génération automatique de chemins
- Aide au debug des propriétés

---

# Installation

## Prérequis
- Python 3
- Graphviz

Installation Graphviz :
    sudo apt install graphviz

---

# Utilisation

## Partie ROBDD
    python main.py

### Ajout de test
- Allez dans la fonction main present dans le main.py
- Créez un string portant l'expression voulue. Exemple :"(x1.y1)*(x2.y2)"
- Pour ajouter un ordre, créez un tableau de string de façon décroissante. Exemple : ["x1", "y1", "x2", "y2"]
- Pour produir le robdd associé à l'expression, utilisez la fonction: build_robdd_from_expr(expression, (optionel) ordre);
Si aucun ordre n'est entré l'heuristique le fera à votre place 

## Partie Kripke
    python kripke.py

### Ajout de test
- Dans un fichier text, ecirvez les états (states: s0 s1 s2 s3 s4 s5), précisez l'état init (init: s0), ajoutez les labels : (labels:
s0: p0) et ajoutez les transitions (transitions: s0: s1)
- Dans la fonction main de Kripke.py, faites parse_kripke("nom de votre fichier text"), cela vous retournera le modèle de kripke voulu
- Utilisez parse_ctl("votre formule à tester"), cela vous retournera votre formule utilisable avec le système
- Pour finir, utilisez sat(modèle de kripke, formule). Cela retournera le resultat de l'application de votre formule sur le modèle de kripke.

---

# Auteurs

- Johan Bourdais
- Arthur Fourcart
