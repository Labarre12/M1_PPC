# Exercice 1 : énumération par BFS (parcours en largeur)
#
# Idée : partir du mot M, puis explorer mot par mot les voisins
# (1 insertion, 1 suppression ou 1 substitution).

from alphabet import ALPHABET
from exercice1.levenshtein import mot_valide


def voisins(mot):
    """Retourne tous les mots à distance 1 de 'mot'."""
    resultat = set()

    # 1) Suppressions : on retire la lettre à la position i
    for i in range(len(mot)):
        nouveau = mot[:i] + mot[i + 1:]  # mot sans la lettre i
        resultat.add(nouveau)

    # 2) Insertions : on insère chaque lettre de l'alphabet à chaque position possible
    for i in range(len(mot) + 1):         # +1 car on peut aussi insérer après le dernier caractère
        for lettre in ALPHABET:
            nouveau = mot[:i] + lettre + mot[i:]  # on glisse la lettre à la position i
            resultat.add(nouveau)

    # 3) Substitutions : on remplace la lettre i par chaque autre lettre de l'alphabet
    for i in range(len(mot)):
        for lettre in ALPHABET:
            if lettre != mot[i]:          # inutile de remplacer par la même lettre
                nouveau = mot[:i] + lettre + mot[i + 1:]
                resultat.add(nouveau)

    # Filtre final : on ne garde que les mots composés de lettres de l'alphabet malgache
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

    # Borne sur la longueur : un mot à distance ≤ k diffère d'au plus k caractères
    longueur_min = max(0, len(mot_reference) - k)
    longueur_max = len(mot_reference) + k

    deja_vus      = {mot_reference}  # ensemble des mots déjà découverts (évite les cycles)
    niveau_courant = {mot_reference}  # mots du niveau BFS courant (distance exacte = tour actuel)
    tous_les_mots  = {mot_reference}  # résultat final : tous les mots à distance ≤ k

    # Chaque itération correspond à un niveau de distance supplémentaire
    for distance in range(k):
        niveau_suivant = set()

        for mot in niveau_courant:
            for voisin in voisins(mot):
                if voisin in deja_vus:
                    continue  # déjà trouvé, on passe

                if len(voisin) < longueur_min or len(voisin) > longueur_max:
                    continue  # élagage : longueur impossible pour distance ≤ k

                deja_vus.add(voisin)       # on marque pour ne pas le revisiter
                niveau_suivant.add(voisin) # il sera exploré au prochain niveau
                tous_les_mots.add(voisin)  # on l'ajoute au résultat

        niveau_courant = niveau_suivant  # on passe au niveau suivant

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

    par_distance   = {0: {mot_reference}}  # distance 0 = le mot lui-même
    deja_vus       = {mot_reference}
    niveau_courant = {mot_reference}

    for distance in range(1, k + 1):
        niveau_suivant = set()

        for mot in niveau_courant:
            for voisin in voisins(mot):
                if voisin in deja_vus:
                    continue  # déjà assigné à un niveau précédent

                if len(voisin) < longueur_min or len(voisin) > longueur_max:
                    continue  # élagage longueur

                deja_vus.add(voisin)
                niveau_suivant.add(voisin)

        par_distance[distance] = niveau_suivant  # on associe ce niveau à cette distance exacte
        niveau_courant = niveau_suivant

    # Conversion des sets en listes triées pour un affichage cohérent
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
