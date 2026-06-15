# Rapport Technique - Projet ASG-2026

Prototype de pipeline d'assemblage "de novo". Ce rapport accompagne le code
source (dossier `src/`) et les notebooks de demonstration (dossier `notebooks/`).

---

## 1. Vue d'ensemble du pipeline

```
FASTQ (reads bruts)
   |  Lot 1 : ingestion + qualite
   v
Reads filtres + k-mers
   |  Lot 1 : histogramme de frequence -> identification des erreurs
   v
k-mers solides
   |  Lot 3 : insertion dans le filtre de Bloom
   v
Graphe de de Bruijn implicite (jamais construit en memoire)
   |  Lot 3 : traversee on-the-fly (extensions A/C/G/T)
   v
Contigs (sequence assemblee)
```

Le Lot 2 (alignement par programmation dynamique) sert a valider localement les
chevauchements entre deux reads.

---

## 2. Lot 1 - Ingestion et qualite

- Lecture FASTQ par blocs de 4 lignes (`src/io_sequences.py`).
- Score de qualite Phred+33 : `score = ord(caractere) - 33`.
- Conversion **selective** en FASTA : on ne garde que les reads dont la qualite
  moyenne depasse un seuil.
- Decoupage en k-mers et **histogramme de frequence** (`src/kmers.py`).

### Identification du taux d'erreur

Le spectre de frequence des k-mers (frequence des frequences) montre un pic a
gauche (k-mers apparaissant 1 a 2 fois). Ces k-mers rares proviennent
essentiellement des erreurs de sequencage : un read errone genere des k-mers
uniques qui n'apparaissent presque jamais ailleurs. Les vrais k-mers, eux,
apparaissent un grand nombre de fois (proportionnel a la couverture).

---

## 3. Lot 2 - Alignement par programmation dynamique

- Algorithme : Plus Longue Sous-Sequence Commune (LCS) via une table `dp`
  (`src/alignement.py`).
- Sorties : le **score** (longueur de la LCS) et la **position du chevauchement**.
- Affichage lisible avec marqueurs `|` pour les positions communes.

### Choix du score de similarite

Le score retenu est la longueur de la LCS. Deux reads issus de la meme region de
la reference partagent une longue sous-sequence commune ; un score eleve indique
donc un chevauchement probable. Ce critere est tolerant aux erreurs ponctuelles
(substitutions) car la LCS peut "sauter" les positions erronees.

---

## 4. Lot 3 - Assemblage memory-efficient (approche Minia)

### Principe

Le graphe de de Bruijn n'est jamais construit explicitement. Seuls les k-mers
solides sont stockes, et uniquement sous forme de bits dans un **filtre de Bloom**
(`src/bloom.py`). La traversee (`src/assemblage.py`) genere a la volee les 4
extensions possibles (A, C, G, T) en 3' et teste leur appartenance au filtre.

- 1 extension valide -> on continue le contig.
- 0 extension -> fin du contig.
- plusieurs extensions -> bifurcation, on arrete ce contig.

### Impact de la taille de k

- `k` trop petit : des k-mers identiques peuvent apparaitre a plusieurs endroits
  (repetitions), ce qui cree des bifurcations et fragmente l'assemblage.
- `k` trop grand : un k-mer a plus de chances de contenir une erreur, ce qui
  reduit le nombre de k-mers solides et cree des trous de couverture.
- Pour le toy dataset, `k = 21` avec un `seuil = 5` donne de bons resultats.

### Impact du seuil de solidite

Le seuil separe les vrais k-mers des k-mers issus d'erreurs. Avec une forte
couverture, un seuil de l'ordre de 5 supprime presque toutes les erreurs tout en
conservant les vrais k-mers.

---

## 5. Analyse critique des faux positifs

Le filtre de Bloom ne produit jamais de faux negatif, mais il produit des **faux
positifs** : il peut affirmer qu'un k-mer existe alors qu'il n'a jamais ete
insere. Pendant la traversee, un faux positif cree une fausse extension :

- soit une **fausse bifurcation** (plusieurs extensions validees) qui casse le
  contig en deux,
- soit un **chemin fantome** qui s'eloigne de la vraie sequence.

Les parametres du filtre controlent ce risque :
- `m` (nombre de bits) : plus il est grand, moins il y a de collisions.
- `k_hachages` (nombre de fonctions de hachage) : un nombre adapte minimise la
  probabilite de faux positifs `(1 - e^(-k n / m))^k`.

Observation experimentale (notebook 04) : un taux de faux positifs eleve
(p = 0.1) fragmente fortement l'assemblage, alors qu'un taux faible (p = 1e-6)
permet de reconstruire la sequence en un seul contig. C'est pourquoi l'assemblage
par defaut utilise p = 1e-6.

---

## 6. Analyse de complexite : O(n^2) vs graphe

| Approche | Temps | Espace |
|----------|-------|--------|
| Alignement d'une paire | O(n * m) | O(n * m) |
| Alignement de toutes les paires | O(R^2 * n^2) | O(n * m) |
| Graphe implicite + Bloom | O(N * 4 * k_hachages) | O(m bits) |

(N = nombre total de k-mers, R = nombre de reads, n et m = longueurs des reads.)

L'alignement par paires devient impraticable pour des millions de reads
(croissance quadratique en R). L'approche par graphe traite chaque k-mer une fois
et utilise une memoire constante (le filtre de Bloom), d'ou son interet pour le
passage a l'echelle.

### Comparaison memoire (notebook 04)

Un `set` Python stocke les chaines de k-mers entieres ; sa taille croit avec le
nombre de k-mers et avec la longueur k. Le filtre de Bloom stocke uniquement des
bits et sa taille ne depend pas de k. Le gain memoire est significatif et
justifie le choix de cette structure.

---

## 7. Validation (clause de recette)

Critere : "Le logiciel est valide si, a partir d'un fichier de reads, il
reconstruit la sequence cible avec une identite superieure a 98%."

Sur le toy dataset (reference de 400 bases, reads de 50 bases avec ~1% d'erreur),
l'assemblage avec `k = 21`, `seuil = 5` et `p = 1e-6` reconstruit un contig
unique avec une identite d'environ 99.8% par rapport a la reference. Le critere
de recette est donc atteint.

---

## 8. Robustesse

Le pipeline gere un taux d'erreur de l'ordre de 1% grace au filtrage des k-mers
solides (les erreurs produisent des k-mers rares, ecartes par le seuil). Pour des
taux d'erreur plus eleves, il faudrait augmenter la couverture (plus de reads) ou
ajuster k et le seuil.

---

## 9. Limites et pistes d'amelioration

- Notre filtre de Bloom utilise 1 octet par case (simplicite pedagogique) ; une
  implementation par bits reels diviserait la memoire par 8.
- La traversee s'arrete a la moindre bifurcation ; un vrai assembleur gere les
  bulles (erreurs) et les repetitions de maniere plus fine.
- La mesure d'identite est basee sur la LCS ; un alignement global donnerait une
  mesure plus precise mais plus couteuse.
