# Exercice 2 : partitions par backtracking explicite
#
# Même résultat que partitions(), mais avec une liste 'courante'
# qu'on remplit (append) puis défait (pop) à chaque branche.


def backtrack_partitions(reste, max_terme, courant, resultats):
    """
    reste     = somme qu'il reste à décomposer
    max_terme = plus grand terme autorisé
    courant   = partition en cours de construction
    resultats = liste où on stocke les solutions trouvées
    """
    if reste == 0:
        # On copie courant pour ne pas le modifier plus tard
        copie = []
        for valeur in courant:
            copie.append(valeur)
        resultats.append(copie)
        return

    limite = max_terme
    if reste < limite:
        limite = reste

    for i in range(limite, 0, -1):
        courant.append(i)                 # choix
        backtrack_partitions(reste - i, i, courant, resultats)
        courant.pop()                     # backtracking


def partitions_backtrack(n):
    """Retourne toutes les partitions de n (méthode backtracking)."""
    if n < 0:
        print("Erreur : n doit être >= 0")
        return []

    resultats = []
    courant = []

    backtrack_partitions(n, n, courant, resultats)
    return resultats
