# Lot 1 : analyse de granularite (k-mers)
#
# Un k-mer est un morceau de sequence de longueur k.
# Exemple : pour "ACGT" et k=2, les k-mers sont "AC", "CG", "GT".
#
# Compter les k-mers permet de reperer les erreurs de sequencage :
# un vrai k-mer apparait souvent, un k-mer issu d'une erreur apparait rarement.


def decouper_kmers(sequence, k):
    """Decoupe une sequence en k-mers (fenetre glissante de taille k)."""
    kmers = []
    if len(sequence) < k:
        return kmers

    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmers.append(kmer)

    return kmers


def compter_kmers(reads, k):
    """
    Compte les occurrences de chaque k-mer dans une liste de reads.
    reads = liste de tuples ; on suppose que la sequence est en position 1
            (identifiant, sequence) ou (identifiant, sequence, qualite).
    Retourne un dictionnaire k-mer -> nombre d'occurrences.
    """
    comptage = {}
    for read in reads:
        sequence = read[1]
        for kmer in decouper_kmers(sequence, k):
            if kmer in comptage:
                comptage[kmer] = comptage[kmer] + 1
            else:
                comptage[kmer] = 1

    return comptage


def kmers_solides(comptage, seuil):
    """
    Retourne l'ensemble des k-mers "solides" : ceux qui apparaissent
    strictement plus que 'seuil' fois (les autres sont consideres comme des erreurs).
    """
    solides = set()
    for kmer in comptage:
        if comptage[kmer] > seuil:
            solides.add(kmer)
    return solides


def spectre_frequence(comptage):
    """
    Calcule la "frequence des frequences".
    Retourne un dictionnaire : nombre_d_occurrences -> combien de k-mers ont ce nombre.

    Exemple : si 50 k-mers apparaissent exactement 1 fois,
              alors spectre[1] = 50.
    Le pic a faible frequence correspond souvent aux erreurs de sequencage.
    """
    spectre = {}
    for kmer in comptage:
        occurrences = comptage[kmer]
        if occurrences in spectre:
            spectre[occurrences] = spectre[occurrences] + 1
        else:
            spectre[occurrences] = 1

    return spectre
