# Lot 1 : ingestion des donnees et controle de qualite
#
# - lecture des fichiers FASTQ (4 lignes par read)
# - calcul de la qualite (scores Phred)
# - conversion selective en FASTA (on garde les reads de bonne qualite)


def lire_fastq(chemin):
    """
    Lit un fichier FASTQ.
    Retourne une liste de tuples (identifiant, sequence, qualite).

    Format FASTQ : 4 lignes par read
      ligne 1 : @identifiant
      ligne 2 : sequence (ACGT)
      ligne 3 : +
      ligne 4 : ligne de qualite
    """
    reads = []
    fichier = open(chemin, "r")
    lignes = fichier.readlines()
    fichier.close()

    # On enleve les retours a la ligne
    lignes_propres = []
    for ligne in lignes:
        lignes_propres.append(ligne.strip())

    # On avance 4 lignes par 4 lignes
    i = 0
    while i + 3 < len(lignes_propres):
        ligne_id = lignes_propres[i]
        sequence = lignes_propres[i + 1]
        qualite = lignes_propres[i + 3]

        # On enleve le @ du debut de l'identifiant
        if ligne_id.startswith("@"):
            identifiant = ligne_id[1:]
        else:
            identifiant = ligne_id

        reads.append((identifiant, sequence, qualite))
        i = i + 4

    return reads


def score_phred(caractere):
    """Convertit un caractere de qualite en score Phred (encodage Phred+33)."""
    return ord(caractere) - 33


def qualite_moyenne(ligne_qualite):
    """Calcule le score Phred moyen d'une ligne de qualite."""
    if len(ligne_qualite) == 0:
        return 0

    total = 0
    for caractere in ligne_qualite:
        total = total + score_phred(caractere)

    return total / len(ligne_qualite)


def fastq_vers_fasta(reads, seuil_qualite=30):
    """
    Conversion selective FASTQ -> FASTA.
    On garde seulement les reads dont la qualite moyenne depasse le seuil.
    Retourne une liste de tuples (identifiant, sequence).
    """
    reads_fasta = []
    for identifiant, sequence, qualite in reads:
        if qualite_moyenne(qualite) >= seuil_qualite:
            reads_fasta.append((identifiant, sequence))

    return reads_fasta


def ecrire_fasta(chemin, reads_fasta):
    """Ecrit une liste (identifiant, sequence) au format FASTA."""
    fichier = open(chemin, "w")
    for identifiant, sequence in reads_fasta:
        fichier.write(">" + identifiant + "\n")
        fichier.write(sequence + "\n")
    fichier.close()


def lire_fasta(chemin):
    """
    Lit un fichier FASTA.
    Retourne une liste de tuples (identifiant, sequence).
    """
    reads = []
    fichier = open(chemin, "r")
    lignes = fichier.readlines()
    fichier.close()

    identifiant = None
    sequence = ""

    for ligne in lignes:
        ligne = ligne.strip()
        if ligne == "":
            continue

        if ligne.startswith(">"):
            # Nouvelle sequence : on sauvegarde la precedente
            if identifiant is not None:
                reads.append((identifiant, sequence))
            identifiant = ligne[1:]
            sequence = ""
        else:
            sequence = sequence + ligne

    # Ne pas oublier la derniere sequence
    if identifiant is not None:
        reads.append((identifiant, sequence))

    return reads
