# Generation du toy dataset (jeu de test)
#
# On part d'une sequence de reference connue, puis on la decoupe en
# fragments courts (reads). On ajoute environ 1% d'erreurs (substitutions)
# pour imiter des donnees de sequencage reelles.

import os
import random

BASES = "ACGT"


def generer_reference(longueur=400, graine=42):
    """Cree une sequence ADN aleatoire mais reproductible (meme graine = meme sequence)."""
    generateur = random.Random(graine)
    sequence = ""
    for _ in range(longueur):
        sequence = sequence + generateur.choice(BASES)
    return sequence


def fragmenter(reference, nb_reads, longueur_read, taux_erreur, graine=123):
    """
    Decoupe la reference en reads.
    - on choisit une position de depart aleatoire pour chaque read
    - on copie longueur_read bases
    - chaque base a une probabilite taux_erreur d'etre remplacee (erreur)
    """
    generateur = random.Random(graine)
    reads = []

    position_max = len(reference) - longueur_read
    if position_max < 0:
        print("Erreur : reference trop courte pour cette longueur de read.")
        return reads

    for i in range(nb_reads):
        debut = generateur.randint(0, position_max)
        morceau = reference[debut:debut + longueur_read]

        # On introduit des erreurs (substitutions)
        lettres = list(morceau)
        for j in range(len(lettres)):
            if generateur.random() < taux_erreur:
                lettres[j] = generateur.choice(BASES)

        read = ""
        for lettre in lettres:
            read = read + lettre

        identifiant = "read_" + str(i)
        reads.append((identifiant, read))

    return reads


def qualite_factice(longueur):
    """
    Cree une ligne de qualite Phred+33 plausible.
    Le caractere 'I' correspond a un bon score (Phred 40).
    """
    ligne = ""
    for _ in range(longueur):
        ligne = ligne + "I"
    return ligne


def ecrire_fasta(chemin, identifiant, sequence):
    """Ecrit une sequence au format FASTA."""
    fichier = open(chemin, "w")
    fichier.write(">" + identifiant + "\n")
    fichier.write(sequence + "\n")
    fichier.close()


def ecrire_fastq(chemin, reads):
    """Ecrit les reads au format FASTQ (4 lignes par read)."""
    fichier = open(chemin, "w")
    for identifiant, sequence in reads:
        fichier.write("@" + identifiant + "\n")
        fichier.write(sequence + "\n")
        fichier.write("+\n")
        fichier.write(qualite_factice(len(sequence)) + "\n")
    fichier.close()


def generer_toy(dossier_data=None, nb_reads=2000, longueur_read=50, taux_erreur=0.01):
    """Genere reference.fasta et toy_reads.fastq dans le dossier data/."""
    if dossier_data is None:
        # data/ se trouve a cote du dossier src/
        ici = os.path.dirname(os.path.abspath(__file__))
        dossier_data = os.path.join(ici, "..", "data")

    if not os.path.exists(dossier_data):
        os.makedirs(dossier_data)

    reference = generer_reference(longueur=400)
    reads = fragmenter(reference, nb_reads, longueur_read, taux_erreur)

    chemin_fasta = os.path.join(dossier_data, "reference.fasta")
    chemin_fastq = os.path.join(dossier_data, "toy_reads.fastq")

    ecrire_fasta(chemin_fasta, "reference", reference)
    ecrire_fastq(chemin_fastq, reads)

    print("Reference (" + str(len(reference)) + " bases) ecrite dans : " + chemin_fasta)
    print(str(len(reads)) + " reads ecrits dans : " + chemin_fastq)
    return reference, reads


if __name__ == "__main__":
    generer_toy()
