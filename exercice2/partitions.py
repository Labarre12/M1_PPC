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

    if max_terme is None or max_terme > n:
        max_terme = n

    # Cas de base : il ne reste plus rien à décomposer
    if n == 0:
        return [[]]

    resultat = []

    # On essaie le plus grand terme possible, puis on descend
    limite = max_terme
    if n < limite:
        limite = n

    for i in range(limite, 0, -1):
        restes = partitions(n - i, i)
        for reste in restes:
            partition = [i]
            for valeur in reste:
                partition.append(valeur)
            resultat.append(partition)

    return resultat


def afficher_partition(partition):
    """Transforme [3, 1] en '3+1'."""
    texte = ""
    for i in range(len(partition)):
        if i > 0:
            texte = texte + "+"
        texte = texte + str(partition[i])
    return texte


# Compatibilité
format_partition = afficher_partition
