# Exercice 3 : Rendu de monnaie
#
# Objectif : rendre un montant N avec le minimum de pièces.
# Méthodes :
#   1) Backtracking avec élagage
#   2) Recherche exhaustive (tester toutes les combinaisons possibles)


def _construire_resultat(valeurs, choix, nombre_pieces):
    """Prépare le résultat final dans l'ordre des valeurs V."""
    detail = {}
    for i in range(len(valeurs)):
        detail[valeurs[i]] = choix[i]

    return {
        "trouve": True,
        "nombre_pieces": nombre_pieces,
        "repartition": choix,
        "detail": detail,
    }


def rendre_monnaie_backtrack(valeurs, montant):
    """
    Backtracking : on choisit combien de pièces utiliser pour chaque valeur.
    On garde la meilleure solution trouvée et on coupe les branches trop longues.
    """
    if montant < 0:
        print("Erreur : montant négatif")
        return {"trouve": False}

    if montant == 0:
        choix = []
        for _ in valeurs:
            choix.append(0)
        return _construire_resultat(valeurs, choix, 0)

    meilleur_choix = None
    meilleur_nombre = montant + 1  # pire cas : toutes des pièces de 1

    choix = []
    for _ in valeurs:
        choix.append(0)

    def backtrack(index, reste, nombre_actuel):
        nonlocal meilleur_choix, meilleur_nombre

        # Toutes les pièces ont été choisies
        if index == len(valeurs):
            if reste == 0 and nombre_actuel < meilleur_nombre:
                meilleur_nombre = nombre_actuel
                meilleur_choix = []
                for valeur in choix:
                    meilleur_choix.append(valeur)
            return

        # Élagage : déjà trop de pièces
        if nombre_actuel >= meilleur_nombre:
            return

        piece = valeurs[index]
        maximum = reste // piece

        # On essaie de mettre maximum pièces, puis on diminue (backtracking)
        for nb in range(maximum, -1, -1):
            choix[index] = nb
            backtrack(index + 1, reste - nb * piece, nombre_actuel + nb)

    backtrack(0, montant, 0)

    if meilleur_choix is None:
        return {"trouve": False}

    return _construire_resultat(valeurs, meilleur_choix, meilleur_nombre)


def rendre_monnaie_exhaustif(valeurs, montant):
    """
    Recherche exhaustive : on génère TOUTES les combinaisons possibles,
    puis on garde celle qui rend exactement N avec le moins de pièces.
    """
    if montant < 0:
        print("Erreur : montant négatif")
        return {"trouve": False}

    if montant == 0:
        choix = []
        for _ in valeurs:
            choix.append(0)
        return _construire_resultat(valeurs, choix, 0)

    toutes_les_solutions = []
    choix = []
    for _ in valeurs:
        choix.append(0)

    def enumerer(index, reste):
        if index == len(valeurs):
            if reste == 0:
                copie = []
                for valeur in choix:
                    copie.append(valeur)
                toutes_les_solutions.append(copie)
            return

        piece = valeurs[index]
        maximum = reste // piece

        for nb in range(0, maximum + 1):
            choix[index] = nb
            enumerer(index + 1, reste - nb * piece)

    enumerer(0, montant)

    if len(toutes_les_solutions) == 0:
        return {"trouve": False}

    meilleur_choix = toutes_les_solutions[0]
    meilleur_nombre = 0
    for valeur in meilleur_choix:
        meilleur_nombre = meilleur_nombre + valeur

    for solution in toutes_les_solutions:
        nombre = 0
        for valeur in solution:
            nombre = nombre + valeur
        if nombre < meilleur_nombre:
            meilleur_nombre = nombre
            meilleur_choix = solution

    return _construire_resultat(valeurs, meilleur_choix, meilleur_nombre)


def afficher_solution_monnaie(valeurs, resultat):
    """Affiche la solution de rendu de monnaie."""
    if not resultat["trouve"]:
        print("Aucune solution possible.")
        return

    print("Nombre total de pieces : " + str(resultat["nombre_pieces"]))
    print("Detail par valeur de piece :")
    for i in range(len(valeurs)):
        piece = valeurs[i]
        nb = resultat["repartition"][i]
        print("  piece " + str(piece) + " : " + str(nb))
