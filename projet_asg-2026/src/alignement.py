# Lot 2 : alignement par programmation dynamique
#
# But : trouver la Plus Longue Sous-Sequence Commune (LCS) entre deux reads.
# Une sous-sequence garde l'ordre des lettres mais pas forcement la contiguite.
# Exemple : LCS de "ACGTAC" et "ACTAC" -> "ACTAC" (longueur 5).
#
# On retourne aussi le score (longueur de la LCS) et la position du chevauchement.


def construire_table(a, b):
    """
    Construit la table de programmation dynamique.
    dp[i][j] = longueur de la LCS entre a[0:i] et b[0:j].
    """
    n = len(a)
    m = len(b)

    # Table remplie de zeros, de taille (n+1) x (m+1)
    dp = []
    for i in range(n + 1):
        ligne = []
        for j in range(m + 1):
            ligne.append(0)
        dp.append(ligne)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                # Les lettres correspondent : on prolonge la diagonale
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Sinon on garde le meilleur des deux cotes
                if dp[i - 1][j] >= dp[i][j - 1]:
                    dp[i][j] = dp[i - 1][j]
                else:
                    dp[i][j] = dp[i][j - 1]

    return dp


def lcs(a, b):
    """
    Calcule la Plus Longue Sous-Sequence Commune entre a et b.
    Retourne (longueur, sous_sequence, dp).
    """
    dp = construire_table(a, b)

    # Remontee de la table pour reconstruire la sous-sequence
    i = len(a)
    j = len(b)
    lettres = []

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            lettres.append(a[i - 1])
            i = i - 1
            j = j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i = i - 1
        else:
            j = j - 1

    # Les lettres ont ete trouvees a l'envers, on les remet a l'endroit
    lettres.reverse()
    sous_sequence = ""
    for lettre in lettres:
        sous_sequence = sous_sequence + lettre

    longueur = dp[len(a)][len(b)]
    return longueur, sous_sequence, dp


def score_alignement(a, b):
    """Retourne le score d'alignement = longueur de la LCS."""
    longueur, sous_sequence, dp = lcs(a, b)
    return longueur


def position_chevauchement(a, b):
    """
    Retourne la position approximative du chevauchement dans chaque read.
    On renvoie (debut_a, fin_a, debut_b, fin_b) : les zones couvertes par la LCS.
    """
    dp = construire_table(a, b)

    i = len(a)
    j = len(b)

    fin_a = 0
    fin_b = 0
    debut_a = len(a)
    debut_b = len(b)
    premiere = True

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            if premiere:
                fin_a = i - 1
                fin_b = j - 1
                premiere = False
            debut_a = i - 1
            debut_b = j - 1
            i = i - 1
            j = j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i = i - 1
        else:
            j = j - 1

    return debut_a, fin_a, debut_b, fin_b


def afficher_alignement(a, b):
    """
    Affiche un alignement lisible base sur la LCS.
    Les lettres communes sont marquees par '|'.
    """
    longueur, sous_sequence, dp = lcs(a, b)

    ligne_a = ""
    ligne_milieu = ""
    ligne_b = ""

    i = 0  # position dans a
    j = 0  # position dans b
    indice_lcs = 0  # position dans la sous-sequence commune

    while i < len(a) or j < len(b):
        if (indice_lcs < len(sous_sequence)
                and i < len(a) and j < len(b)
                and a[i] == sous_sequence[indice_lcs]
                and b[j] == sous_sequence[indice_lcs]):
            # Lettre commune
            ligne_a = ligne_a + a[i]
            ligne_milieu = ligne_milieu + "|"
            ligne_b = ligne_b + b[j]
            i = i + 1
            j = j + 1
            indice_lcs = indice_lcs + 1
        elif i < len(a) and (indice_lcs >= len(sous_sequence) or a[i] != sous_sequence[indice_lcs]):
            # Lettre presente seulement dans a
            ligne_a = ligne_a + a[i]
            ligne_milieu = ligne_milieu + " "
            ligne_b = ligne_b + "-"
            i = i + 1
        else:
            # Lettre presente seulement dans b
            ligne_a = ligne_a + "-"
            ligne_milieu = ligne_milieu + " "
            ligne_b = ligne_b + b[j]
            j = j + 1

    texte = ligne_a + "\n" + ligne_milieu + "\n" + ligne_b
    return texte
