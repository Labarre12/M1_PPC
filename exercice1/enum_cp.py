# Exercice 1 : énumération par programmation par contraintes (backtracking)
#
# Idée : construire un mot lettre par lettre.
# À chaque étape, on teste si le préfixe peut encore mener à une solution.

from alphabet import ALPHABET
from exercice1.levenshtein import distance_levenshtein, mot_valide


def prefixe_encore_possible(mot_reference, prefixe, k, longueur_voulue):
    """
    Retourne True si le préfixe peut encore devenir un mot valide.
    Si la distance est déjà trop grande, inutile de continuer.
    """
    cases_restantes = longueur_voulue - len(prefixe)         # lettres qu'il reste à choisir
    distance = distance_levenshtein(mot_reference, prefixe)  # distance du préfixe partiel
    # Chaque lettre future peut au mieux corriger 1 d'écart → si déjà trop loin, on coupe
    return distance <= k + cases_restantes


def chercher_mot(mot_reference, k, longueur, prefixe, resultats):
    """
    Fonction récursive de backtracking.
    prefixe = liste de lettres déjà choisies (ex: ['v', 'a'])
    """
    # Cas de base : toutes les lettres ont été fixées → mot complet
    if len(prefixe) == longueur:
        mot = ""
        for lettre in prefixe:
            mot = mot + lettre  # on concatène la liste en chaîne

        if distance_levenshtein(mot_reference, mot) <= k:
            resultats.add(mot)  # solution valide
        return

    # On essaie chaque lettre de l'alphabet à la position courante
    for lettre in ALPHABET:
        prefixe.append(lettre)  # on fixe cette lettre (choix)

        mot_partiel = ""
        for l in prefixe:
            mot_partiel = mot_partiel + l

        # Propagation de contrainte : ce préfixe peut-il encore mener à une solution ?
        if prefixe_encore_possible(mot_reference, mot_partiel, k, longueur):
            chercher_mot(mot_reference, k, longueur, prefixe, resultats)
        # Si non : élagage, toute la sous-branche est abandonnée sans être explorée

        prefixe.pop()  # backtracking : on retire la lettre pour essayer la suivante


def enumerer_mots_cp(mot_reference, k):
    """Retourne tous les mots à distance <= k (méthode CP + backtracking)."""
    if not mot_valide(mot_reference):
        print("Erreur : le mot de référence contient des lettres hors alphabet.")
        return []

    longueur_min = max(1, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    resultats = set()

    # On lance une recherche séparée pour chaque longueur cible possible
    for longueur in range(longueur_min, longueur_max + 1):
        chercher_mot(mot_reference, k, longueur, [], resultats)

    liste = list(resultats)
    liste.sort()
    return liste


# Compatibilité
enumerate_words_cp = enumerer_mots_cp
