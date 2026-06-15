# TP Pruning - Exercice 1 : algorithme AC3 (arc-consistance)
#
# Idee : on rend le CSP arc-consistant en examinant des arcs orientes.
# Pour chaque arc (xi, xj), la fonction Revise supprime de D(xi) toute
# valeur qui n'a aucun support dans D(xj). Si D(xi) change, on remet dans
# la file tous les arcs (xk, xi) des voisins pour propager la reduction.
#
# Ce module ne fait QUE la logique : il produit une liste de "snapshots"
# (etapes) que la couche visualisation rejoue ensuite pas a pas.


def construire_contraintes(liste_contraintes):
    """
    Transforme une liste de contraintes binaires en arcs orientes.

    Entree : liste de triplets (a, relation, b), relation parmi "<", ">", "=".
    Sortie :
      - arcs : dict {(xi, xj): predicat(vi, vj) -> bool}
      - ordre : liste des arcs dans l'ordre de creation (pour la file initiale)
      - etiquettes : dict {(xi, xj): "X < Y"} pour l'affichage
    """
    arcs = {}
    ordre = []
    etiquettes = {}

    for a, relation, b in liste_contraintes:
        if relation == "<":
            arcs[(a, b)] = lambda vi, vj: vi < vj
            arcs[(b, a)] = lambda vi, vj: vi > vj
            etiquettes[(a, b)] = a + " < " + b
            etiquettes[(b, a)] = b + " > " + a
        elif relation == ">":
            arcs[(a, b)] = lambda vi, vj: vi > vj
            arcs[(b, a)] = lambda vi, vj: vi < vj
            etiquettes[(a, b)] = a + " > " + b
            etiquettes[(b, a)] = b + " < " + a
        elif relation == "=":
            arcs[(a, b)] = lambda vi, vj: vi == vj
            arcs[(b, a)] = lambda vi, vj: vi == vj
            etiquettes[(a, b)] = a + " = " + b
            etiquettes[(b, a)] = b + " = " + a
        else:
            raise ValueError("Relation inconnue : " + str(relation))

        ordre.append((a, b))
        ordre.append((b, a))

    return arcs, ordre, etiquettes


def revise(domaines, xi, xj, predicat):
    """
    Supprime de D(xi) les valeurs sans support dans D(xj).
    Retourne (modifie, valeurs_supprimees).
    """
    nouveau_domaine = []
    valeurs_supprimees = []

    for vi in domaines[xi]:
        a_un_support = False
        for vj in domaines[xj]:
            if predicat(vi, vj):
                a_un_support = True
                break

        if a_un_support:
            nouveau_domaine.append(vi)
        else:
            valeurs_supprimees.append(vi)

    domaines[xi] = nouveau_domaine
    return (len(valeurs_supprimees) > 0, valeurs_supprimees)


def voisins_entrants(arcs, cible, exclu):
    """Retourne les arcs (xk, cible) avec xk different de 'exclu'."""
    resultat = []
    for arc in arcs:
        depart, arrivee = arc
        if arrivee == cible and depart != exclu:
            resultat.append(arc)
    return resultat


def _copier_domaines(domaines):
    copie = {}
    for variable in domaines:
        copie[variable] = list(domaines[variable])
    return copie


def _snapshot(phase, domaines, file_arcs, arc_courant, message,
              valeurs_supprimees=None, arcs_reinseres=None, succes=None):
    """Construit un dictionnaire decrivant l'etat complet a afficher."""
    return {
        "phase": phase,
        "domaines": _copier_domaines(domaines),
        "file": list(file_arcs),
        "arc_courant": arc_courant,
        "message": message,
        "valeurs_supprimees": list(valeurs_supprimees) if valeurs_supprimees else [],
        "arcs_reinseres": list(arcs_reinseres) if arcs_reinseres else [],
        "succes": succes,
    }


def ac3(variables, domaines_initiaux, liste_contraintes):
    """
    Execute AC3 et renvoie (domaines_finaux, succes, etapes).

    'etapes' est la liste de snapshots a visualiser pas a pas.
    """
    arcs, ordre, etiquettes = construire_contraintes(liste_contraintes)
    domaines = _copier_domaines(domaines_initiaux)

    file_arcs = list(ordre)
    etapes = []

    etapes.append(_snapshot(
        "initial", domaines, file_arcs, None,
        "Etat initial : tous les arcs sont places dans la file Q.",
    ))

    succes = True

    while len(file_arcs) > 0:
        arc_courant = file_arcs.pop(0)
        xi, xj = arc_courant
        etiquette = etiquettes.get(arc_courant, xi + " ? " + xj)

        etapes.append(_snapshot(
            "traitement", domaines, file_arcs, arc_courant,
            "Arc extrait : (" + xi + ", " + xj + ")  ->  Revise(" + xi
            + ", " + xj + ")  [contrainte " + etiquette + "]",
        ))

        modifie, valeurs_supprimees = revise(domaines, xi, xj, arcs[arc_courant])

        if not modifie:
            etapes.append(_snapshot(
                "traitement", domaines, file_arcs, arc_courant,
                "Aucune valeur supprimee dans D(" + xi + "). La file Q est inchangee.",
            ))
            continue

        if len(domaines[xi]) == 0:
            etapes.append(_snapshot(
                "echec", domaines, file_arcs, arc_courant,
                "Echec : D(" + xi + ") est vide. Le CSP est insatisfaisable.",
                valeurs_supprimees=valeurs_supprimees, succes=False,
            ))
            succes = False
            return domaines, succes, etapes

        arcs_a_reinserer = voisins_entrants(arcs, xi, xj)
        nouveaux_reinseres = []
        for arc in arcs_a_reinserer:
            if arc not in file_arcs:
                file_arcs.append(arc)
                nouveaux_reinseres.append(arc)

        texte_supprimees = ", ".join(str(v) for v in valeurs_supprimees)
        message = ("Revise(" + xi + ", " + xj + ") : suppression de {"
                   + texte_supprimees + "} dans D(" + xi + ").")
        if nouveaux_reinseres:
            texte_arcs = ", ".join("(" + a + "," + b + ")" for a, b in nouveaux_reinseres)
            message = message + " Arcs reinseres : " + texte_arcs + "."
        else:
            message = message + " Aucun arc a reinserer."

        etapes.append(_snapshot(
            "suppression", domaines, file_arcs, arc_courant, message,
            valeurs_supprimees=valeurs_supprimees,
            arcs_reinseres=nouveaux_reinseres,
        ))

    etapes.append(_snapshot(
        "final", domaines, file_arcs, None,
        "Termine : la file Q est vide. Le CSP est ARC-CONSISTANT.",
        succes=True,
    ))

    return domaines, succes, etapes


def liste_aretes_non_orientees(liste_contraintes):
    """Retourne les aretes (a, b) sans doublon pour dessiner le graphe."""
    aretes = []
    for a, _relation, b in liste_contraintes:
        if (a, b) not in aretes and (b, a) not in aretes:
            aretes.append((a, b))
    return aretes
