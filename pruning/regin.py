# TP Pruning - Exercice 2 : filtrage de AllDifferent (algorithme de Regin)
#
# Idee : la contrainte globale AllDifferent se modelise par un graphe biparti
# Variables <-> Valeurs. Une affectation valide = un couplage qui sature toutes
# les variables. Une valeur reste possible pour une variable seulement s'il
# existe un couplage maximum utilisant l'arete correspondante.
#
# Regin caracterise ces aretes "utiles" grace au graphe de residu oriente :
#   - une arete hors-couplage est conservee si ses deux extremites sont dans
#     la meme Composante Fortement Connexe (cycle alternant), ou si elle est
#     atteignable depuis une valeur libre (chemin alternant).
#   - sinon elle n'appartient a aucun couplage maximum : on la supprime.
#
# Ce module produit la logique + une liste de snapshots pour la visualisation.


def cle_var(nom):
    return ("var", nom)


def cle_val(valeur):
    return ("val", valeur)


def valeurs_triees(variables, domaines):
    """Union triee de toutes les valeurs presentes dans les domaines."""
    ensemble = set()
    for variable in variables:
        for valeur in domaines[variable]:
            ensemble.add(valeur)
    return sorted(ensemble)


def couplage_maximum(variables, domaines):
    """
    Couplage maximum biparti par chemins augmentants (algorithme de Kuhn).
    Retourne (couplage_var, couplage_val) :
      couplage_var : dict variable -> valeur
      couplage_val : dict valeur -> variable
    """
    couplage_var = {}
    couplage_val = {}

    def chercher_chemin(variable, visitees):
        for valeur in domaines[variable]:
            if valeur in visitees:
                continue
            visitees.add(valeur)
            if valeur not in couplage_val or chercher_chemin(couplage_val[valeur], visitees):
                couplage_val[valeur] = variable
                couplage_var[variable] = valeur
                return True
        return False

    for variable in variables:
        chercher_chemin(variable, set())

    return couplage_var, couplage_val


def construire_arcs_residu(variables, domaines, couplage_var):
    """
    Construit le graphe oriente de residu (orientation de l'illustration).
      - arete du couplage   : valeur -> variable (type "M")
      - arete hors couplage : variable -> valeur (type "E")
    Retourne la liste d'arcs (depart_cle, arrivee_cle, type).
    """
    arcs = []
    for variable in variables:
        for valeur in domaines[variable]:
            if couplage_var.get(variable) == valeur:
                arcs.append((cle_val(valeur), cle_var(variable), "M"))
            else:
                arcs.append((cle_var(variable), cle_val(valeur), "E"))
    return arcs


def tarjan_scc(noeuds, adjacence):
    """
    Detection des Composantes Fortement Connexes (algorithme de Tarjan).
    Retourne une liste de composantes (chaque composante est une liste de noeuds).
    """
    index_courant = [0]
    indices = {}
    bas_liens = {}
    sur_pile = {}
    pile = []
    composantes = []

    import sys
    limite = sys.getrecursionlimit()
    if limite < 10000:
        sys.setrecursionlimit(10000)

    def parcours(noeud):
        indices[noeud] = index_courant[0]
        bas_liens[noeud] = index_courant[0]
        index_courant[0] = index_courant[0] + 1
        pile.append(noeud)
        sur_pile[noeud] = True

        for voisin in adjacence.get(noeud, []):
            if voisin not in indices:
                parcours(voisin)
                bas_liens[noeud] = min(bas_liens[noeud], bas_liens[voisin])
            elif sur_pile.get(voisin, False):
                bas_liens[noeud] = min(bas_liens[noeud], indices[voisin])

        if bas_liens[noeud] == indices[noeud]:
            composante = []
            while True:
                sommet = pile.pop()
                sur_pile[sommet] = False
                composante.append(sommet)
                if sommet == noeud:
                    break
            composantes.append(composante)

    for noeud in noeuds:
        if noeud not in indices:
            parcours(noeud)

    return composantes


def _adjacence(noeuds, arcs, inverse=False):
    """Construit un dict d'adjacence a partir des arcs (depart, arrivee, type)."""
    adjacence = {}
    for noeud in noeuds:
        adjacence[noeud] = []
    for depart, arrivee, _type in arcs:
        if inverse:
            adjacence[arrivee].append(depart)
        else:
            adjacence[depart].append(arrivee)
    return adjacence


def noeuds_atteignables(depart_set, adjacence):
    """Ensemble des noeuds atteignables depuis 'depart_set' (parcours en profondeur)."""
    visites = set()
    pile = list(depart_set)
    while pile:
        noeud = pile.pop()
        if noeud in visites:
            continue
        visites.add(noeud)
        for voisin in adjacence.get(noeud, []):
            if voisin not in visites:
                pile.append(voisin)
    return visites


def _copier_domaines(variables, domaines):
    copie = {}
    for variable in variables:
        copie[variable] = list(domaines[variable])
    return copie


def filtrer_regin(variables, domaines_initiaux):
    """
    Applique le filtrage de Regin sur la contrainte AllDifferent(variables).
    Retourne (domaines_finaux, faisable, etapes, infos).
      - etapes : liste de snapshots a visualiser
      - infos  : dict (couplage, sccs, aretes_supprimees, ...)
    """
    domaines = _copier_domaines(variables, domaines_initiaux)
    valeurs = valeurs_triees(variables, domaines)

    aretes = []
    for variable in variables:
        for valeur in domaines[variable]:
            aretes.append((variable, valeur))

    etapes = []

    def snapshot(phase, message, **extra):
        base = {
            "phase": phase,
            "message": message,
            "variables": list(variables),
            "valeurs": list(valeurs),
            "domaines": _copier_domaines(variables, domaines),
            "aretes": list(aretes),
            "couplage": {},
            "oriente": False,
            "composantes": None,
            "aretes_supprimees": [],
            "aretes_conservees": [],
            "domaines_finaux": None,
            "faisable": True,
        }
        base.update(extra)
        etapes.append(base)

    # Etape 1 : graphe biparti initial
    snapshot(
        "biparti",
        "Graphe biparti initial G = (V u D, E) : chaque arete relie une "
        "variable a une valeur de son domaine.",
    )

    # Etape 2 : couplage maximum
    couplage_var, couplage_val = couplage_maximum(variables, domaines)
    couplage_complet = (len(couplage_var) == len(variables))

    if not couplage_complet:
        snapshot(
            "couplage",
            "Aucun couplage complet : la contrainte AllDifferent est "
            "INSATISFAISABLE.",
            couplage=dict(couplage_var),
            faisable=False,
        )
        return domaines, False, etapes, {
            "couplage": couplage_var,
            "composantes": None,
            "aretes_supprimees": [],
        }

    texte_couplage = ", ".join(
        "(" + str(v) + "," + str(couplage_var[v]) + ")" for v in variables
    )
    snapshot(
        "couplage",
        "Couplage maximum trouve (complet) : M = {" + texte_couplage + "}.",
        couplage=dict(couplage_var),
    )

    # Etape 3 : graphe de residu oriente
    arcs = construire_arcs_residu(variables, domaines, couplage_var)
    snapshot(
        "residu",
        "Graphe de residu oriente : aretes du couplage valeur -> variable, "
        "aretes hors couplage variable -> valeur. On cherche cycles et chemins "
        "alternants.",
        couplage=dict(couplage_var),
        oriente=True,
    )

    # Etape 4 : SCC (Tarjan) + reachability depuis les valeurs libres + filtrage
    noeuds = [cle_var(v) for v in variables] + [cle_val(d) for d in valeurs]
    adjacence = _adjacence(noeuds, arcs, inverse=False)
    adjacence_inverse = _adjacence(noeuds, arcs, inverse=True)

    composantes = tarjan_scc(noeuds, adjacence)
    comp_index = {}
    for numero, composante in enumerate(composantes):
        for noeud in composante:
            comp_index[noeud] = numero

    # Valeurs libres = valeurs non utilisees par le couplage.
    valeurs_libres = [d for d in valeurs if d not in couplage_val]
    depart_libres = set(cle_val(d) for d in valeurs_libres)
    atteignables = noeuds_atteignables(depart_libres, adjacence_inverse)

    aretes_supprimees = []
    aretes_conservees = []
    for variable, valeur in aretes:
        if couplage_var.get(variable) == valeur:
            aretes_conservees.append((variable, valeur))
            continue
        meme_scc = comp_index[cle_var(variable)] == comp_index[cle_val(valeur)]
        sur_chemin_libre = (
            cle_var(variable) in atteignables and cle_val(valeur) in atteignables
        )
        if meme_scc or sur_chemin_libre:
            aretes_conservees.append((variable, valeur))
        else:
            aretes_supprimees.append((variable, valeur))

    for variable, valeur in aretes_supprimees:
        if valeur in domaines[variable]:
            domaines[variable].remove(valeur)

    domaines_finaux = _copier_domaines(variables, domaines)

    if aretes_supprimees:
        texte_suppr = ", ".join(
            "(" + str(v) + "," + str(d) + ")" for v, d in aretes_supprimees
        )
        message = ("Filtrage : suppression des aretes hors-couplage qui ne sont "
                   "ni dans une SCC, ni sur un chemin alternant : " + texte_suppr + ".")
    else:
        message = "Filtrage : aucune arete a supprimer, le graphe est deja filtre."

    snapshot(
        "scc",
        message,
        couplage=dict(couplage_var),
        oriente=True,
        composantes=dict(comp_index),
        aretes_supprimees=list(aretes_supprimees),
        aretes_conservees=list(aretes_conservees),
        domaines_finaux=domaines_finaux,
    )

    infos = {
        "couplage": couplage_var,
        "composantes": comp_index,
        "aretes_supprimees": aretes_supprimees,
        "valeurs_libres": valeurs_libres,
    }
    return domaines, True, etapes, infos
