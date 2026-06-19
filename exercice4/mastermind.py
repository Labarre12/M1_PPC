# Exercice 4 : Mastermind simplifié
#
# L'IA doit trouver la combinaison secrète en un minimum de tentatives.
# Méthodes :
#   1) Recherche exhaustive : on garde toutes les combinaisons possibles
#      et on élimine celles qui ne correspondent pas aux indices.
#   2) Backtracking : on reconstruit les combinaisons possibles selon l'historique.


def calculer_indice(secret, proposition):
    """
    Retourne (bien_placees, mal_placees).
    bien_placees  = bonne couleur au bon endroit
    mal_placees   = bonne couleur au mauvais endroit
    """
    bien_placees = 0

    secret_reste = []  # couleurs du secret non exactement placées
    prop_reste   = []  # couleurs de la proposition non exactement placées

    # 1ère passe : on compte les positions exactes
    for i in range(len(secret)):
        if secret[i] == proposition[i]:
            bien_placees = bien_placees + 1
        else:
            # On garde de côté les couleurs non exactement placées pour la 2e passe
            secret_reste.append(secret[i])
            prop_reste.append(proposition[i])

    # 2e passe : parmi les non-exactes, combien de couleurs sont présentes mais mal placées ?
    mal_placees = 0
    for couleur in prop_reste:
        if couleur in secret_reste:
            mal_placees = mal_placees + 1
            secret_reste.remove(couleur)  # on consomme la couleur pour ne pas la compter deux fois

    return bien_placees, mal_placees


def generer_toutes_combinaisons(couleurs, longueur):
    """Génère toutes les combinaisons possibles (produit cartésien)."""
    resultat = []

    def construire(prefixe):
        if len(prefixe) == longueur:
            copie = []
            for couleur in prefixe:
                copie.append(couleur)  # copie pour éviter les références partagées
            resultat.append(copie)
            return

        for couleur in couleurs:
            prefixe.append(couleur)  # on essaie cette couleur à la position suivante
            construire(prefixe)      # on descend
            prefixe.pop()            # backtracking

    construire([])
    return resultat


def filtrer_candidats(candidats, proposition, indice_attendu):
    """Garde seulement les secrets qui donneraient le même indice que celui reçu."""
    restants = []

    for candidat in candidats:
        indice = calculer_indice(candidat, proposition)
        # Si ce candidat était le secret, l'indice obtenu serait-il le même que l'indice réel ?
        if indice[0] == indice_attendu[0] and indice[1] == indice_attendu[1]:
            restants.append(candidat)  # oui → il reste possible

    return restants


def combinaison_compatible(combinaison, historique):
    """Vérifie si une combinaison respecte TOUS les indices déjà reçus."""
    for proposition, indice_attendu in historique:
        indice = calculer_indice(combinaison, proposition)
        if indice[0] != indice_attendu[0] or indice[1] != indice_attendu[1]:
            return False  # incompatible avec au moins un indice → on rejette
    return True


def trouver_candidats_backtrack(couleurs, longueur, historique):
    """
    Backtracking : construit les combinaisons possibles couleur par couleur
    en respectant l'historique des tentatives.
    """
    candidats = []

    def backtrack(prefixe):
        # Cas de base : combinaison complète → on vérifie la compatibilité
        if len(prefixe) == longueur:
            if combinaison_compatible(prefixe, historique):
                copie = []
                for couleur in prefixe:
                    copie.append(couleur)
                candidats.append(copie)
            return

        for couleur in couleurs:
            prefixe.append(couleur)  # on choisit cette couleur
            backtrack(prefixe)
            prefixe.pop()            # backtracking

    backtrack([])
    return candidats


def resoudre_mastermind_exhaustif(secret, couleurs, max_tentatives=20):
    """
    L'IA joue en filtrant exhaustivement l'ensemble des combinaisons.
    """
    longueur  = len(secret)
    candidats = generer_toutes_combinaisons(couleurs, longueur)  # tous les codes possibles
    historique = []
    tentatives = 0

    while tentatives < max_tentatives:
        if len(candidats) == 0:
            break  # aucun candidat restant → contradiction, ne devrait pas arriver

        proposition = candidats[0]                          # on joue toujours le premier candidat restant
        indice      = calculer_indice(secret, proposition)  # on obtient le feedback du secret
        historique.append((proposition, indice))
        tentatives = tentatives + 1

        if indice[0] == longueur:
            return {                            # toutes les positions sont correctes → trouvé !
                "trouve": True,
                "tentatives": tentatives,
                "historique": historique,
                "methode": "exhaustif",
            }

        candidats = filtrer_candidats(candidats, proposition, indice)  # on élimine les codes incompatibles

    return {
        "trouve": False,
        "tentatives": tentatives,
        "historique": historique,
        "methode": "exhaustif",
    }


def resoudre_mastermind_backtrack(secret, couleurs, max_tentatives=20):
    """
    L'IA joue en recalculant les candidats possibles par backtracking
    après chaque indice reçu.
    """
    longueur   = len(secret)
    historique = []
    tentatives = 0

    while tentatives < max_tentatives:
        # On régénère les candidats depuis zéro à chaque tour en filtrant via l'historique
        candidats = trouver_candidats_backtrack(couleurs, longueur, historique)

        if len(candidats) == 0:
            break  # plus aucun candidat compatible avec l'historique

        proposition = candidats[0]                          # on joue le premier candidat valide
        indice      = calculer_indice(secret, proposition)
        historique.append((proposition, indice))            # on mémorise l'essai et son indice
        tentatives = tentatives + 1

        if indice[0] == longueur:
            return {
                "trouve": True,
                "tentatives": tentatives,
                "historique": historique,
                "methode": "backtrack",
            }

    return {
        "trouve": False,
        "tentatives": tentatives,
        "historique": historique,
        "methode": "backtrack",
    }


def afficher_historique_mastermind(historique):
    """Affiche les tentatives une par une."""
    num = 1
    for proposition, indice in historique:
        texte = ""
        for couleur in proposition:
            texte = texte + str(couleur) + " "
        print(
            "  Tentative "
            + str(num)
            + " : "
            + texte
            + "| bien placees="
            + str(indice[0])
            + ", mal placees="
            + str(indice[1])
        )
        num = num + 1


def jouer_mastermind_interactif(couleurs, longueur, methode="exhaustif", max_tentatives=20):
    """
    Mode interactif : l'utilisateur choisit le secret au clavier.
    L'IA propose des combinaisons et l'utilisateur donne les indices.
    """
    print("\nMode interactif Mastermind")
    print("Couleurs possibles : " + str(couleurs))
    print("Longueur du code : " + str(longueur))
    print("Entrez votre secret (une couleur par case, separees par des espaces).")

    entree = input("Secret : ")
    parties = entree.strip().split()
    secret = []
    for partie in parties:
        secret.append(partie)

    if len(secret) != longueur:
        print("Erreur : mauvaise longueur de secret.")
        return

    for couleur in secret:
        if couleur not in couleurs:
            print("Erreur : couleur inconnue " + couleur)
            return

    if methode == "backtrack":
        resultat = resoudre_mastermind_backtrack(secret, couleurs, max_tentatives)
    else:
        resultat = resoudre_mastermind_exhaustif(secret, couleurs, max_tentatives)

    print("\nMethode : " + resultat["methode"])
    afficher_historique_mastermind(resultat["historique"])

    if resultat["trouve"]:
        print("Secret trouve en " + str(resultat["tentatives"]) + " tentative(s).")
    else:
        print("Secret non trouve.")

    return resultat
