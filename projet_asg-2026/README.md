# Projet ASG-2026 : Pipeline d'Assemblage "De Novo"

Prototype de pipeline d'assemblage de novo en Python. Il reconstruit une
sequence consensus (contig) a partir de fragments courts (reads), sans jamais
construire explicitement le graphe de de Bruijn en memoire.

## Structure

```
projet_asg-2026/
├── data/                 # toy dataset (reference + reads)
├── src/                  # code source (modules Python)
│   ├── io_sequences.py   # Lot 1 : lecture FASTQ, conversion FASTA, qualite
│   ├── kmers.py          # Lot 1 : k-mers (decoupage, comptage, spectre)
│   ├── alignement.py     # Lot 2 : alignement par programmation dynamique (LCS)
│   ├── bloom.py          # Lot 3 : filtre de Bloom
│   ├── assemblage.py     # Lot 3 : assemblage memory-efficient (approche Minia)
│   └── generer_toy.py    # generation du toy dataset
├── notebooks/            # demonstrations + graphiques
├── rapport/              # rapport technique
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

1. Generer le jeu de test :

```bash
python -m src.generer_toy
```

Cela cree `data/reference.fasta` (sequence cible connue) et
`data/toy_reads.fastq` (reads fragmentes avec environ 1% d'erreur).

2. Ouvrir les notebooks :

```bash
jupyter notebook
```

- `01_lot1_ingestion_kmers.ipynb` : ingestion + histogramme de frequence des k-mers
- `02_lot2_alignement.ipynb` : alignement de deux reads
- `03_lot3_assemblage_bloom.ipynb` : assemblage via filtre de Bloom
- `04_analyse_complexite_faux_positifs.ipynb` : analyses (faux positifs, memoire, complexite)

## Les 3 lots

- **Lot 1** : ingestion des donnees brutes (FASTQ), conversion selective en FASTA,
  decoupage en k-mers et histogramme de frequence pour identifier le taux d'erreur.
- **Lot 2** : moteur d'alignement par programmation dynamique (Plus Longue
  Sous-Sequence Commune) qui retourne le score et la position du chevauchement.
- **Lot 3** : assemblage "memory-efficient" via un filtre de Bloom. Le graphe de
  de Bruijn reste conceptuel : on teste les extensions A/C/G/T a la volee.
```
