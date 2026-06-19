# M1_PPC — Explication générale du projet

## Contexte

Ce projet est un travail de Master 1 en **Programmation Par Contraintes (PPC)**.
Il explore différentes techniques pour résoudre des problèmes combinatoires :
recherche exhaustive, backtracking, élagage et propagation de contraintes.

Tous les exercices sont en **Python pur** (sans bibliothèque de contraintes externe)
pour montrer les mécanismes fondamentaux.

---

## Structure du projet

```
M1_PPC/
├── main.py                  ← Point d'entrée principal (tous les exercices)
├── alphabet.py              ← Alphabet malgache (partagé par exercice 1)
├── requirements.txt         ← Dépendances Python
│
├── exercice1/               ← Distance de Levenshtein et énumération de mots
│   ├── levenshtein.py       ← Calcul de distance + validation
│   ├── enum_bfs.py          ← Enumération par BFS (parcours en largeur)
│   ├── enum_backtrack.py    ← Enumération par backtracking (2 variantes)
│   ├── enum_cp.py           ← Enumération par programmation par contraintes
│   └── EXPLICATION.md       ← Ce fichier d'explication
│
├── exercice2/               ← Partitions d'un entier
│   ├── partitions.py        ← Méthode récursive
│   ├── partitions_backtrack.py  ← Méthode backtracking explicite
│   └── EXPLICATION.md       ← Ce fichier d'explication
│
├── exercice3/               ← Rendu de monnaie optimal
│   ├── monnaie.py           ← Backtracking + exhaustif
│   └── EXPLICATION.md       ← Ce fichier d'explication
│
├── exercice4/               ← Mastermind (solveur IA)
│   ├── mastermind.py        ← Exhaustif + backtracking + mode interactif
│   └── EXPLICATION.md       ← Ce fichier d'explication
│
└── pruning/                 ← TP avancé : algorithmes AC3 et Regin (visualisation)
    ├── ac3.py
    ├── regin.py
    ├── visualisation.py
    └── main_pruning.py
```

---

## Fichier `main.py` — Point d'entrée

**Rôle :** Lance les démonstrations de tous les exercices. Gère les arguments en
ligne de commande pour personnaliser les paramètres.

### Commandes disponibles

```bash
# Lancer tous les exercices avec les valeurs par défaut
python main.py

# Lancer uniquement l'exercice 1 avec un autre mot et une distance de 1
python main.py --exercice 1 --m "fito" --k 1

# Lancer uniquement l'exercice 2 avec n=6
python main.py --exercice 2 --n 6

# Lancer uniquement l'exercice 3 avec des pièces personnalisées
python main.py --exercice 3 --monnaie-v "1,3,4" --monnaie-n 6

# Lancer uniquement l'exercice 4
python main.py --exercice 4

# Mode interactif Mastermind
python main.py --mastermind-interactif --mastermind-couleurs "R,V,B,J" --mastermind-longueur 4
```

### Fonction `demo_exercice1(mot_reference, k, ignorer_cp)`

```python
mots_bfs             = enumerer_mots_bfs(mot_reference, k)
mots_back_edition    = enumerer_mots_backtrack_edition(mot_reference, k)
mots_back_construction = enumerer_mots_backtrack_construction(mot_reference, k)
```
Lance les trois méthodes et affiche le nombre de mots trouvés par chacune (doit être
identique), la répartition par distance exacte, et la liste complète.

### Fonction `demo_exercice2(n)`

Lance les deux méthodes de partitions et vérifie qu'elles donnent le même résultat.

### Fonction `demo_exercice3(valeurs, montant)`

Lance les deux méthodes de rendu de monnaie sur deux exemples prédéfinis, et compare
les résultats.

### Fonction `demo_exercice4()`

Lance les deux méthodes Mastermind sur deux secrets fixes et affiche l'historique des
tentatives.

### Gestion des arguments CLI

```python
parser = argparse.ArgumentParser(...)
parser.add_argument("--m", default="vato", ...)
parser.add_argument("--k", type=int, default=2, ...)
...
args = parser.parse_args()
```
`argparse` parse automatiquement les arguments de la ligne de commande. `default`
donne la valeur utilisée si l'argument n'est pas fourni. `type=int` convertit
automatiquement la chaîne en entier.

---

## Résumé des exercices

### Exercice 1 — Distance de Levenshtein

**Problème :** Trouver tous les mots à distance ≤ k d'un mot de référence.

**Concepts clés :**
- **Distance de Levenshtein :** nombre minimal d'insertions, suppressions, substitutions
  pour transformer un mot en un autre. Calculée par programmation dynamique.
- **BFS :** explore les mots par niveaux de distance croissante.
- **Backtracking (édition) :** explore le graphe d'édition en profondeur.
- **Backtracking (construction) :** construit chaque mot lettre par lettre avec élagage.
- **CP :** construction lettre par lettre avec contrainte de faisabilité explicite.

**Intérêt pédagogique :** Montrer comment différentes stratégies d'exploration
(largeur vs profondeur) et différents élagages donnent le même résultat mais avec
des performances différentes.

---

### Exercice 2 — Partitions d'un entier

**Problème :** Trouver toutes les façons d'écrire n comme somme d'entiers positifs.

**Concepts clés :**
- **Paramètre d'ordre (`max_terme`) :** évite les doublons en imposant l'ordre décroissant.
- **Récursion fonctionnelle :** retourne des listes, pas d'état partagé.
- **Backtracking impératif :** modifie une liste `courant` avec append/pop.

**Intérêt pédagogique :** Illustration simple du backtracking et de l'importance de
copier les solutions (`list(courant)` au lieu de `courant`).

---

### Exercice 3 — Rendu de monnaie

**Problème :** Rendre un montant N avec le minimum de pièces parmi un ensemble donné.

**Concepts clés :**
- **Branch and Bound :** le backtracking maintient une borne supérieure (meilleur nombre
  de pièces trouvé) et coupe les branches qui ne peuvent pas l'améliorer.
- **Ordre d'exploration :** commencer par le maximum de grandes pièces permet de trouver
  une bonne solution rapidement, ce qui rend l'élagage plus efficace.
- **Exhaustif :** génère tout sans élagage, pour comparaison.

**Intérêt pédagogique :** Introduit l'optimisation (pas seulement trouver une solution,
mais la meilleure) et le concept de borne pour l'élagage.

---

### Exercice 4 — Mastermind

**Problème :** Trouver un code secret en un minimum d'essais, en utilisant les indices
(bien placés / mal placés) pour éliminer les possibilités.

**Concepts clés :**
- **Filtrage de candidats :** après chaque essai, on élimine les codes incompatibles avec
  l'indice reçu.
- **Cohérence avec l'historique :** un candidat valide doit être compatible avec TOUS les
  indices passés.
- **Deux représentations :** liste filtrée (exhaustif) vs. régénération par backtracking.

**Intérêt pédagogique :** Montre comment les contraintes réduisent progressivement
l'espace de recherche (comme dans un solveur CSP réel).

---

## Concepts communs à tous les exercices

### Le Backtracking

Le backtracking est une méthode d'exploration d'un espace de solutions :

```
1. Choisir une valeur pour la prochaine variable
2. Vérifier si ce choix est encore faisable (contraintes)
3. Si oui : aller plus profond (appel récursif)
4. Si non : passer au choix suivant
5. Quand toutes les valeurs ont été essayées : retour arrière (pop)
```

La mécanique `append` / appel récursif / `pop` est le cœur du backtracking.

### L'Elagage (Pruning)

L'élagage consiste à **couper des branches de l'arbre de recherche** avant de les
explorer complètement, quand on sait que la branche ne peut pas mener à une solution.

Types d'élagages dans ce projet :
- **Faisabilité :** "ce préfixe ne peut plus donner un mot à distance ≤ k" (ex. 1)
- **Optimalité :** "cette branche a déjà trop de pièces" (ex. 3)
- **Taille :** "ce mot est trop long / trop court" (ex. 1)
- **Déjà vu :** "ce mot a déjà été trouvé" (ex. 1 BFS)

### Programmation Dynamique vs Backtracking

| Technique              | Quand l'utiliser                              |
|------------------------|-----------------------------------------------|
| Prog. dynamique        | Sous-problèmes qui se répètent (Levenshtein)  |
| Backtracking           | Enumération avec contraintes                  |
| BFS                    | Trouver les solutions les plus proches d'abord |
| Branch and Bound       | Optimisation (trouver la meilleure solution)   |

---

## Comment lancer le projet

```bash
# Installation des dépendances (si nécessaire)
pip install -r requirements.txt

# Lancer tous les exercices
python main.py

# Lancer le TP avancé (pruning avec visualisation)
cd pruning && python main_pruning.py
```
