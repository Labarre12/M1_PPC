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
    # Cas de base : tout a été décomposé → partition complète
    if reste == 0:
        copie = []
        for valeur in courant:
            copie.append(valeur)  # copie obligatoire : courant sera modifié plus tard par pop()
        resultats.append(copie)
        return

    limite = max_terme
    if reste < limite:
        limite = reste  # on ne peut pas prendre un terme plus grand que ce qui reste

    for i in range(limite, 0, -1):
        courant.append(i)                                       # choix : on ajoute le terme i
        backtrack_partitions(reste - i, i, courant, resultats)  # on résout le reste, termes ≤ i
        courant.pop()                                           # backtracking : on retire i


def partitions_backtrack(n):
    """Retourne toutes les partitions de n (méthode backtracking)."""
    if n < 0:
        print("Erreur : n doit être >= 0")
        return []

    resultats = []
    courant = []  # liste partagée modifiée par append/pop au fil de la récursion

    backtrack_partitions(n, n, courant, resultats)  # max_terme initial = n
    return resultats
