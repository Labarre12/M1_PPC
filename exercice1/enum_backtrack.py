# Exercice 1 : recherche exhaustive par backtracking
#
# Variante 1 : backtracking sur les opérations d'édition (comme BFS mais en profondeur)
# Variante 2 : backtracking sur la construction du mot (comme CP)

from alphabet import ALPHABET
from exercice1.enum_bfs import voisins
from exercice1.levenshtein import distance_levenshtein, mot_valide


def backtrack_edition(mot, profondeur, k, longueur_min, longueur_max, chemin, resultats):
    """
    Explore récursivement les modifications du mot.
    profondeur = nombre d'opérations déjà faites
    chemin = mots déjà visités sur la branche courante
    """
    if longueur_min <= len(mot) <= longueur_max:
        resultats.add(mot)

    if profondeur >= k:
        return

    for voisin in voisins(mot):
        if voisin in chemin:
            continue

        chemin.add(voisin)
        backtrack_edition(voisin, profondeur + 1, k, longueur_min, longueur_max, chemin, resultats)
        chemin.remove(voisin)  # backtracking


def enumerer_mots_backtrack_edition(mot_reference, k):
    """Backtracking sur le graphe d'édition."""
    if not mot_valide(mot_reference):
        print("Erreur : le mot de référence contient des lettres hors alphabet.")
        return []

    longueur_min = max(0, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    resultats = set()
    chemin = {mot_reference}

    backtrack_edition(mot_reference, 0, k, longueur_min, longueur_max, chemin, resultats)

    liste = list(resultats)
    liste.sort()
    return liste


def backtrack_construction(mot_reference, k, longueur, prefixe, resultats):
    """Construit un mot lettre par lettre avec retour arrière."""
    if len(prefixe) == longueur:
        mot = ""
        for lettre in prefixe:
            mot = mot + lettre

        if distance_levenshtein(mot_reference, mot) <= k:
            resultats.add(mot)
        return

    cases_restantes = longueur - len(prefixe)

    for lettre in ALPHABET:
        prefixe.append(lettre)

        mot_partiel = ""
        for l in prefixe:
            mot_partiel = mot_partiel + l

        distance = distance_levenshtein(mot_reference, mot_partiel)
        if distance <= k + cases_restantes - 1:
            backtrack_construction(mot_reference, k, longueur, prefixe, resultats)

        prefixe.pop()


def enumerer_mots_backtrack_construction(mot_reference, k):
    """Backtracking en construisant le mot caractère par caractère."""
    if not mot_valide(mot_reference):
        print("Erreur : le mot de référence contient des lettres hors alphabet.")
        return []

    longueur_min = max(1, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    resultats = set()

    for longueur in range(longueur_min, longueur_max + 1):
        backtrack_construction(mot_reference, k, longueur, [], resultats)

    liste = list(resultats)
    liste.sort()
    return liste


# Compatibilité
enumerate_words_backtrack_edit = enumerer_mots_backtrack_edition
enumerate_words_backtrack_build = enumerer_mots_backtrack_construction
