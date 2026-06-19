# Exercice 2 — Partitions d'un entier

## Objectif de l'exercice

Etant donné un entier n, trouver **toutes les façons** de l'écrire comme somme
d'entiers positifs. C'est ce qu'on appelle les **partitions** d'un entier.

Exemple pour n = 4 :
- 4
- 3+1
- 2+2
- 2+1+1
- 1+1+1+1

**Règle d'ordre :** on impose un ordre décroissant pour éviter les doublons.
Ainsi on écrit `3+1` mais pas `1+3` (c'est la même partition).

Deux méthodes sont implémentées et comparées :
1. **Récursive** (méthode fonctionnelle)
2. **Backtracking explicite** (méthode avec pile)

---

## Fichier `partitions.py`

**Rôle :** Calcule toutes les partitions de n de façon récursive pure, en retournant
des listes de listes.

### Fonction `partitions(n, max_terme=None)`

```python
if n < 0:
    print("Erreur : n doit être >= 0")
    return []
```
Validation d'entrée : n doit être positif ou nul.

```python
if max_terme is None or max_terme > n:
    max_terme = n
```
Au premier appel, `max_terme` est None. On l'initialise à n (le terme maximum ne peut
pas dépasser n lui-même). Cela garantit l'ordre décroissant : le premier terme est au
plus n, le deuxième au plus le premier, etc.

```python
if n == 0:
    return [[]]
```
Cas de base : si le reste à décomposer est 0, la seule partition est la partition
vide `[]`. Cela représente la fin d'une branche réussie.

```python
resultat = []
limite = max_terme
if n < limite:
    limite = n
```
La limite haute est le minimum entre `max_terme` (contrainte d'ordre) et n (on ne
peut pas prendre un terme plus grand que ce qui reste).

```python
for i in range(limite, 0, -1):
    restes = partitions(n - i, i)
    for reste in restes:
        partition = [i]
        for valeur in reste:
            partition.append(valeur)
        resultat.append(partition)
```
Pour chaque terme i (en partant du plus grand), on résout récursivement le problème
avec le reste `n - i`, en imposant que le prochain terme ne dépasse pas i (ordre
décroissant). On préfixe chaque partition du reste par i pour construire la partition
complète.

Exemple pour `partitions(4)` :
- i=4 → restes = `partitions(0, 4)` = `[[]]` → partition `[4]`
- i=3 → restes = `partitions(1, 3)` = `[[1]]` → partition `[3, 1]`
- i=2 → restes = `partitions(2, 2)` = `[[2], [1,1]]` → partitions `[2,2]` et `[2,1,1]`
- i=1 → restes = `partitions(3, 1)` = `[[1,1,1]]` → partition `[1,1,1,1]`

---

### Fonction `afficher_partition(partition)`

```python
texte = ""
for i in range(len(partition)):
    if i > 0:
        texte = texte + "+"
    texte = texte + str(partition[i])
return texte
```
Transforme une liste comme `[3, 1]` en la chaîne `"3+1"`. Le `if i > 0` évite
d'ajouter un `+` avant le premier terme.

---

## Fichier `partitions_backtrack.py`

**Rôle :** Même résultat que `partitions.py` mais avec un backtracking explicite.
Au lieu de retourner des listes, on maintient une liste `courant` qu'on **modifie**
(append/pop) pour explorer toutes les branches.

### Fonction `backtrack_partitions(reste, max_terme, courant, resultats)`

```python
if reste == 0:
    copie = []
    for valeur in courant:
        copie.append(valeur)
    resultats.append(copie)
    return
```
Cas de base : si tout a été décomposé (reste = 0), la partition en cours est complète.
On en fait une **copie** (important : sinon toutes les entrées dans `resultats`
pointeraient vers le même objet `courant` qui sera modifié par la suite).

```python
limite = max_terme
if reste < limite:
    limite = reste
```
Même borne que dans la version récursive.

```python
for i in range(limite, 0, -1):
    courant.append(i)                          # choix : on essaie le terme i
    backtrack_partitions(reste - i, i, courant, resultats)
    courant.pop()                              # backtracking : on annule le choix
```
La mécanique du backtracking :
1. `courant.append(i)` → on **choisit** le terme i
2. Appel récursif pour explorer les partitions du reste
3. `courant.pop()` → **retour arrière** : on annule le choix pour essayer i-1

### Fonction `partitions_backtrack(n)`

```python
resultats = []
courant = []
backtrack_partitions(n, n, courant, resultats)
return resultats
```
Fonction d'entrée qui initialise les structures et lance le backtracking.

---

## Différence entre les deux méthodes

| Aspect           | `partitions.py`                        | `partitions_backtrack.py`              |
|------------------|----------------------------------------|----------------------------------------|
| Style            | Fonctionnel (retourne des valeurs)     | Impératif (modifie une liste partagée) |
| Mémoire          | Crée de nombreuses listes intermédiaires | Une seule liste `courant` réutilisée  |
| Lisibilité       | Plus proche des maths                  | Montre clairement le mécanisme         |
| Résultat         | Identique                              | Identique                              |

Les deux fonctions produisent exactement les mêmes partitions dans le même ordre.

---

## Lien avec la programmation par contraintes

Cet exercice est un exemple simple de **recherche dans un espace combinatoire** :
- L'**espace de recherche** est l'ensemble de toutes les suites d'entiers possibles
- La **contrainte** est que la somme doit valoir n et les termes doivent être en ordre décroissant
- L'**élagage** est implicite via `max_terme` : on ne teste jamais des suites qui
  violeraient l'ordre décroissant
