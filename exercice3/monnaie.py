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
        detail[valeurs[i]] = choix[i]  # dict {valeur_pièce: quantité_utilisée}

    return {
        "trouve": True,
        "nombre_pieces": nombre_pieces,  # total de pièces
        "repartition": choix,            # liste brute des quantités par dénomination
        "detail": detail,                # même info sous forme de dictionnaire
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

    meilleur_choix  = None
    meilleur_nombre = montant + 1  # borne initiale : pire cas théorique (tout en pièces de 1)

    choix = []
    for _ in valeurs:
        choix.append(0)  # choix[i] = nombre de pièces de valeur valeurs[i]

    def backtrack(index, reste, nombre_actuel):
        nonlocal meilleur_choix, meilleur_nombre

        # Cas de base : toutes les dénominations ont été traitées
        if index == len(valeurs):
            if reste == 0 and nombre_actuel < meilleur_nombre:
                # On a trouvé une meilleure solution → on la sauvegarde
                meilleur_nombre = nombre_actuel
                meilleur_choix = []
                for valeur in choix:
                    meilleur_choix.append(valeur)  # copie de choix
            return

        # Élagage (Branch & Bound) : déjà autant ou plus de pièces que la meilleure connue
        if nombre_actuel >= meilleur_nombre:
            return  # cette branche ne peut pas améliorer le résultat

        piece   = valeurs[index]
        maximum = reste // piece  # nombre max de pièces de cette dénomination utilisables

        # On commence par le max (stratégie gloutonne) : trouve vite une bonne borne
        for nb in range(maximum, -1, -1):
            choix[index] = nb                                             # on fixe la quantité
            backtrack(index + 1, reste - nb * piece, nombre_actuel + nb) # on passe à la dénomination suivante

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
        # Cas de base : toutes les dénominations ont été traitées
        if index == len(valeurs):
            if reste == 0:               # on accepte uniquement si le montant est exactement atteint
                copie = []
                for valeur in choix:
                    copie.append(valeur) # copie obligatoire avant de continuer à modifier choix
                toutes_les_solutions.append(copie)
            return

        piece   = valeurs[index]
        maximum = reste // piece

        # Aucun élagage : on explore toutes les quantités de 0 à maximum
        for nb in range(0, maximum + 1):
            choix[index] = nb
            enumerer(index + 1, reste - nb * piece)

    enumerer(0, montant)

    if len(toutes_les_solutions) == 0:
        return {"trouve": False}

    # On parcourt toutes les solutions valides et on garde celle qui utilise le moins de pièces
    meilleur_choix  = toutes_les_solutions[0]
    meilleur_nombre = 0
    for valeur in meilleur_choix:
        meilleur_nombre = meilleur_nombre + valeur  # total de pièces de la première solution

    for solution in toutes_les_solutions:
        nombre = 0
        for valeur in solution:
            nombre = nombre + valeur   # total de pièces de cette solution
        if nombre < meilleur_nombre:
            meilleur_nombre = nombre
            meilleur_choix  = solution # on met à jour si c'est mieux

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
        nb    = resultat["repartition"][i]
        print("  piece " + str(piece) + " : " + str(nb))
