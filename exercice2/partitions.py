# Exercice 2 : partitions d'un entier n (méthode récursive)
#
# Exemple : n = 4  ->  4, 3+1, 2+2, 2+1+1, 1+1+1+1
#
# Astuce : on impose un ordre décroissant (3+1 et pas 1+3)
# grâce au paramètre max_terme.


def partitions(n, max_terme=None):
    """
    Retourne toutes les façons d'écrire n comme somme d'entiers positifs.
    max_terme = plus grand nombre qu'on a le droit d'utiliser maintenant.
    """
    if n < 0:
        print("Erreur : n doit être >= 0")
        return []

    # Premier appel : max_terme est None → on l'initialise à n (le terme max possible)
    # Si max_terme > n : on le réduit à n (inutile de prendre plus que ce qui reste)
    if max_terme is None or max_terme > n:
        max_terme = n

    # Cas de base : n == 0, rien à décomposer → une seule partition : la liste vide
    if n == 0:
        return [[]]

    resultat = []

    # La limite est min(max_terme, n) : on ne peut pas dépasser le reste disponible
    limite = max_terme
    if n < limite:
        limite = n

    # On essaie i comme premier terme (du plus grand au plus petit pour l'ordre décroissant)
    for i in range(limite, 0, -1):
        restes = partitions(n - i, i)  # partitions du reste, avec termes ≤ i (ordre décroissant)
        for reste in restes:
            partition = [i]            # on préfixe le terme i devant chaque partition du reste
            for valeur in reste:
                partition.append(valeur)
            resultat.append(partition)

    return resultat


def afficher_partition(partition):
    """Transforme [3, 1] en '3+1'."""
    texte = ""
    for i in range(len(partition)):
        if i > 0:
            texte = texte + "+"  # séparateur entre les termes (pas avant le premier)
        texte = texte + str(partition[i])
    return texte


# Compatibilité
format_partition = afficher_partition
