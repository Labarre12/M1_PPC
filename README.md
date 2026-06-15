# Programmation par contraintes

Exercices 1 a 4, TP Pruning (AC3 + Regin) et projet ASG-2026.

## Installation

Depuis la racine du projet :

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Activer l'environnement (optionnel) :

```powershell
.venv\Scripts\Activate.ps1
```

---

## Exercices 1 a 4 — `main.py`

Point d'entree principal :

```powershell
python main.py
```

Lance la demonstration de **tous** les exercices (1, 2, 3 et 4).

### Exercice 1 — Mots a distance de Levenshtein

Enumeration par BFS, backtracking et programmation par contraintes.

```powershell
python main.py --exercice 1
python main.py --exercice 1 --m vato --k 2
python main.py --exercice 1 --m chat --k 1 --skip-cp
```

| Option | Description | Defaut |
|--------|-------------|--------|
| `--m` | Mot de reference | `vato` |
| `--k` | Distance maximale | `2` |
| `--skip-cp` | Ignorer la methode CP (plus lente) | — |

### Exercice 2 — Partitions d'un entier

```powershell
python main.py --exercice 2
python main.py --exercice 2 --n 5
```

| Option | Description | Defaut |
|--------|-------------|--------|
| `--n` | Entier a partitionner | `4` |

### Exercice 3 — Rendu de monnaie

```powershell
python main.py --exercice 3
python main.py --exercice 3 --monnaie-v 1,2,5 --monnaie-n 13
python main.py --exercice 3 --monnaie-v 1,3,4 --monnaie-n 6
```

| Option | Description | Defaut |
|--------|-------------|--------|
| `--monnaie-v` | Valeurs des pieces (separees par des virgules) | `1,2,5` |
| `--monnaie-n` | Montant a rendre | `13` |

### Exercice 4 — Mastermind simplifie

```powershell
python main.py --exercice 4
python main.py --mastermind-interactif
python main.py --mastermind-interactif --mastermind-couleurs R,V,B --mastermind-longueur 3
```

| Option | Description | Defaut |
|--------|-------------|--------|
| `--mastermind-interactif` | Mode interactif (vous entrez le secret) | — |
| `--mastermind-couleurs` | Couleurs disponibles | `R,V,B` |
| `--mastermind-longueur` | Longueur du code secret | `3` |

---

## TP Pruning — AC3 et Regin (`pruning/`)

Visualisation pas a pas avec boutons **Precedent / Suivant** (Matplotlib).

### Exercice 1 — AC3 (arc-consistance)

Cas impose : `X, Y, Z`, domaines `{1,2}`, contraintes `X < Y` et `Y = Z`.

```powershell
python -m pruning.main_pruning --exercice 1
```

### Exercice 2 — Regin / AllDifferent

Cas impose : `x1..x4` avec filtrage global (couplage, graphe de residu, SCC Tarjan).

```powershell
python -m pruning.main_pruning --exercice 2
```

### Les deux exercices

```powershell
python -m pruning.main_pruning --exercice 0
python -m pruning.main_pruning
```

### Export PNG (sans fenetre interactive)

Genere une image par etape dans `pruning/exports/` :

```powershell
python -m pruning.main_pruning --exercice 1 --export --no-show
python -m pruning.main_pruning --exercice 2 --export --no-show
python -m pruning.main_pruning --export --no-show
```

| Option | Description | Defaut |
|--------|-------------|--------|
| `--exercice` | `1` = AC3, `2` = Regin, `0` = les deux | `0` |
| `--export` | Exporter les etapes en PNG | — |
| `--no-show` | Ne pas ouvrir la fenetre Matplotlib | — |

Enonce detaille : [pruning/pruning.md](pruning/pruning.md)

---

## Projet ASG-2026 — Assemblage de novo

Pipeline separe dans `projet_asg-2026/`. Voir [projet_asg-2026/README.md](projet_asg-2026/README.md).

```powershell
cd projet_asg-2026
pip install -r requirements.txt
python -m src.generer_toy
jupyter notebook
```

---

## Structure du depot

```
programmation_par_contrainte/
├── main.py                 # Exercices 1 a 4
├── exercice1/              # Levenshtein, BFS, backtracking, CP
├── exercice2/              # Partitions
├── exercice3/              # Monnaie
├── exercice4/              # Mastermind
├── pruning/                # TP Pruning (AC3 + Regin)
│   ├── main_pruning.py     # Point d'entree du TP
│   ├── ac3.py
│   ├── regin.py
│   ├── visualisation.py
│   └── exports/            # PNG generes (--export)
└── projet_asg-2026/        # Projet assemblage genomique
```
