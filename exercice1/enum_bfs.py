# Exercice 1 : énumération par BFS (parcours en largeur)
#
# Idée : partir du mot M, puis explorer mot par mot les voisins
# (1 insertion, 1 suppression ou 1 substitution).

from alphabet import ALPHABET
from exercice1.levenshtein import mot_valide


def voisins(mot):
    """Retourne tous les mots à distance 1 de 'mot'."""
    resultat = set()

    # 1) Suppressions : enlever une lettre à chaque position
    for i in range(len(mot)):
        nouveau = mot[:i] + mot[i + 1:]
        resultat.add(nouveau)

    # 2) Insertions : ajouter une lettre de l'alphabet à chaque position
    for i in range(len(mot) + 1):
        for lettre in ALPHABET:
            nouveau = mot[:i] + lettre + mot[i:]
            resultat.add(nouveau)

    # 3) Substitutions : remplacer une lettre par une autre lettre
    for i in range(len(mot)):
        for lettre in ALPHABET:
            if lettre != mot[i]:
                nouveau = mot[:i] + lettre + mot[i + 1:]
                resultat.add(nouveau)

    # On garde seulement les mots valides
    mots_valides = set()
    for candidat in resultat:
        if mot_valide(candidat):
            mots_valides.add(candidat)

    return mots_valides


def enumerer_mots_bfs(mot_reference, k):
    """
    Retourne tous les mots à distance <= k de mot_reference.
    Méthode BFS : on explore niveau par niveau (distance 0, 1, 2, ...).
    """
    if not mot_valide(mot_reference):
        print("Erreur : le mot de référence contient des lettres hors alphabet.")
        return []

    longueur_min = max(0, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    deja_vus = {mot_reference}
    niveau_courant = {mot_reference}
    tous_les_mots = {mot_reference}

    for distance in range(k):
        niveau_suivant = set()

        for mot in niveau_courant:
            for voisin in voisins(mot):
                if voisin in deja_vus:
                    continue

                if len(voisin) < longueur_min or len(voisin) > longueur_max:
                    continue

                deja_vus.add(voisin)
                niveau_suivant.add(voisin)
                tous_les_mots.add(voisin)

        niveau_courant = niveau_suivant

    liste_triee = list(tous_les_mots)
    liste_triee.sort()
    return liste_triee


def enumerer_mots_par_distance(mot_reference, k):
    """Regroupe les mots trouvés par distance exacte (0, 1, ..., k)."""
    if not mot_valide(mot_reference):
        print("Erreur : le mot de référence contient des lettres hors alphabet.")
        return {}

    longueur_min = max(0, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    par_distance = {0: {mot_reference}}
    deja_vus = {mot_reference}
    niveau_courant = {mot_reference}

    for distance in range(1, k + 1):
        niveau_suivant = set()

        for mot in niveau_courant:
            for voisin in voisins(mot):
                if voisin in deja_vus:
                    continue

                if len(voisin) < longueur_min or len(voisin) > longueur_max:
                    continue

                deja_vus.add(voisin)
                niveau_suivant.add(voisin)

        par_distance[distance] = niveau_suivant
        niveau_courant = niveau_suivant

    resultat = {}
    for distance, mots in par_distance.items():
        liste = list(mots)
        liste.sort()
        resultat[distance] = liste

    return resultat


# Noms en anglais (compatibilité)
_neighbors = voisins
enumerate_words_bfs = enumerer_mots_bfs
enumerate_words_by_distance = enumerer_mots_par_distance
