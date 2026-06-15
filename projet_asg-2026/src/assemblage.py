# Lot 3 : Assemblage "memory-efficient" (approche type Minia)
#
# Idee : on ne construit JAMAIS le graphe de de Bruijn en entier.
# Le graphe est seulement conceptuel.
#
# - Les noeuds sont les k-mers solides.
# - Pour passer d'un k-mer au suivant (sens 3'), on prend le suffixe de
#   longueur k-1 et on ajoute une base A/C/G/T.
# - On teste chaque extension avec le filtre de Bloom (test d'appartenance
#   a cout memoire constant). Si le test est positif, on continue.
#
# Quand plusieurs extensions sont valides, c'est une bifurcation : on arrete
# le contig courant. Plusieurs contigs peuvent ainsi etre produits.

from src.kmers import compter_kmers, kmers_solides
from src.bloom import FiltreBloom, taille_optimale

BASES = "ACGT"


def construire_filtre(kmers_set, proba_faux_positif=0.000001):
    """
    Cree un filtre de Bloom et y insere tous les k-mers fournis.

    proba_faux_positif doit rester faible : chaque faux positif peut creer
    une fausse bifurcation et donc casser un contig en deux. Un assemblage de
    bonne qualite demande un taux de faux positifs tres bas (ex. 1e-6).
    """
    nb = len(kmers_set)
    taille_bits, nb_hachages = taille_optimale(nb, proba_faux_positif)
    filtre = FiltreBloom(taille_bits, nb_hachages)
    for kmer in kmers_set:
        filtre.ajouter(kmer)
    return filtre


def extensions_avant(kmer, filtre):
    """
    Retourne la liste des k-mers suivants valides (sens 3').
    On garde le suffixe (sans la 1ere lettre) et on essaie d'ajouter A/C/G/T.
    """
    suffixe = kmer[1:]
    valides = []
    for base in BASES:
        candidat = suffixe + base
        if filtre.contient(candidat):
            valides.append(candidat)
    return valides


def extensions_arriere(kmer, filtre):
    """
    Retourne la liste des k-mers precedents valides (sens 5').
    On garde le prefixe (sans la derniere lettre) et on essaie A/C/G/T devant.
    """
    prefixe = kmer[:-1]
    valides = []
    for base in BASES:
        candidat = base + prefixe
        if filtre.contient(candidat):
            valides.append(candidat)
    return valides


def construire_contig(filtre, seed, visites):
    """
    Construit un contig a partir d'un k-mer de depart (seed).
    On etend dans les deux sens tant qu'il n'y a qu'une seule extension valide.
    Une bifurcation (plusieurs extensions) arrete l'extension de ce cote.
    """
    contig = seed
    visites.add(seed)

    # Extension vers l'avant (3')
    courant = seed
    while True:
        suivants = extensions_avant(courant, filtre)
        if len(suivants) != 1:
            # 0 extension = fin ; plusieurs = bifurcation -> on arrete
            break
        prochain = suivants[0]
        if prochain in visites:
            break
        contig = contig + prochain[-1]
        visites.add(prochain)
        courant = prochain

    # Extension vers l'arriere (5')
    courant = seed
    while True:
        precedents = extensions_arriere(courant, filtre)
        if len(precedents) != 1:
            break
        precedent = precedents[0]
        if precedent in visites:
            break
        contig = precedent[0] + contig
        visites.add(precedent)
        courant = precedent

    return contig


def assembler(reads, k, seuil, proba_faux_positif=0.000001):
    """
    Pipeline complet d'assemblage :
      1) compter les k-mers des reads
      2) garder les k-mers solides (au-dela du seuil)
      3) inserer les k-mers solides dans le filtre de Bloom
      4) parcourir le graphe implicite pour produire les contigs
    Retourne la liste des contigs (du plus long au plus court).

    Parametres conseilles pour le toy dataset : k=21, seuil=5.
    """
    comptage = compter_kmers(reads, k)
    solides = kmers_solides(comptage, seuil)

    if len(solides) == 0:
        print("Aucun k-mer solide : baissez le seuil ou la taille k.")
        return []

    filtre = construire_filtre(solides, proba_faux_positif)

    contigs = []
    visites = set()

    for seed in solides:
        if seed in visites:
            continue
        contig = construire_contig(filtre, seed, visites)
        contigs.append(contig)

    # On trie du plus long au plus court
    contigs.sort(key=len, reverse=True)
    return contigs


def complement_inverse(sequence):
    """Retourne le complement inverse d'une sequence ADN."""
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    resultat = ""
    for base in sequence:
        if base in complement:
            resultat = complement[base] + resultat
        else:
            resultat = base + resultat
    return resultat


def _lcs_longueur(a, b):
    """Longueur de la plus longue sous-sequence commune (pour mesurer l'identite)."""
    n = len(a)
    m = len(b)
    precedent = []
    for j in range(m + 1):
        precedent.append(0)

    for i in range(1, n + 1):
        courant = [0]
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                courant.append(precedent[j - 1] + 1)
            else:
                if precedent[j] >= courant[j - 1]:
                    courant.append(precedent[j])
                else:
                    courant.append(courant[j - 1])
        precedent = courant

    return precedent[m]


def identite(contig, reference):
    """
    Mesure l'identite (%) entre un contig et la reference.
    On utilise la longueur de la LCS rapportee a la longueur de la reference.
    On teste aussi le complement inverse (le contig peut etre dans l'autre sens).
    """
    if len(reference) == 0:
        return 0.0

    lcs_direct = _lcs_longueur(contig, reference)
    lcs_inverse = _lcs_longueur(complement_inverse(contig), reference)

    meilleur = lcs_direct
    if lcs_inverse > meilleur:
        meilleur = lcs_inverse

    return 100.0 * meilleur / len(reference)


def meilleure_identite(contigs, reference):
    """Retourne la meilleure identite (%) parmi tous les contigs."""
    meilleur = 0.0
    for contig in contigs:
        valeur = identite(contig, reference)
        if valeur > meilleur:
            meilleur = valeur
    return meilleur
