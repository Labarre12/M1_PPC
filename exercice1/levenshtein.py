# Exercice 1 : calcul de la distance de Levenshtein

from alphabet import ALPHABET


def distance_levenshtein(mot_a, mot_b):
    """
    Calcule le nombre minimal d'operations pour transformer mot_a en mot_b.
    Operations : insertion, suppression, substitution d'une lettre.
    """
    n = len(mot_a)  # nombre de lettres dans mot_a
    m = len(mot_b)  # nombre de lettres dans mot_b

    # Tableau 2D de taille (n+1)x(m+1) : dp[i][j] = distance entre mot_a[0:i] et mot_b[0:j]
    dp = []
    for i in range(n + 1):
        ligne = []
        for j in range(m + 1):
            ligne.append(0)
        dp.append(ligne)

    # Cas de base colonne 0 : transformer les i premières lettres de mot_a en "" = i suppressions
    for i in range(n + 1):
        dp[i][0] = i
    # Cas de base ligne 0 : transformer "" en les j premières lettres de mot_b = j insertions
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Coût de substitution : 0 si mêmes lettres, 1 sinon
            if mot_a[i - 1] == mot_b[j - 1]:
                cout = 0
            else:
                cout = 1

            suppression  = dp[i - 1][j] + 1        # supprimer mot_a[i-1]
            insertion    = dp[i][j - 1] + 1         # insérer mot_b[j-1] dans mot_a
            substitution = dp[i - 1][j - 1] + cout  # remplacer mot_a[i-1] par mot_b[j-1]

            dp[i][j] = min(suppression, insertion, substitution)  # meilleure des 3 opérations

    return dp[n][m]  # la distance finale est dans le coin bas-droit du tableau


def mot_valide(mot):
    """Retourne True si le mot est non vide et utilise seulement l'alphabet malgache."""
    if mot == "":
        return False  # un mot vide est rejeté

    for lettre in mot:
        if lettre not in ALPHABET:
            return False  # toute lettre hors alphabet invalide le mot

    return True


# Noms en anglais gardés pour compatibilité avec d'anciens imports
levenshtein = distance_levenshtein
is_valid_word = mot_valide
