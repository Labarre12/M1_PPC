# Exercice 1 : calcul de la distance de Levenshtein

from alphabet import ALPHABET


def distance_levenshtein(mot_a, mot_b):
    """
    Calcule le nombre minimal d'operations pour transformer mot_a en mot_b.
    Operations : insertion, suppression, substitution d'une lettre.
    """
    n = len(mot_a)
    m = len(mot_b)

    # dp[i][j] = distance entre mot_a[0:i] et mot_b[0:j]
    dp = []
    for i in range(n + 1):
        ligne = []
        for j in range(m + 1):
            ligne.append(0)
        dp.append(ligne)

    # Première ligne et première colonne : coût pour arriver depuis une chaîne vide
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if mot_a[i - 1] == mot_b[j - 1]:
                cout = 0
            else:
                cout = 1

            suppression = dp[i - 1][j] + 1
            insertion = dp[i][j - 1] + 1
            substitution = dp[i - 1][j - 1] + cout

            dp[i][j] = min(suppression, insertion, substitution)

    return dp[n][m]


def mot_valide(mot):
    """Retourne True si le mot est non vide et utilise seulement l'alphabet malgache."""
    if mot == "":
        return False

    for lettre in mot:
        if lettre not in ALPHABET:
            return False

    return True


# Noms en anglais gardés pour compatibilité avec d'anciens imports
levenshtein = distance_levenshtein
is_valid_word = mot_valide
