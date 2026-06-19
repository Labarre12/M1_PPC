# Exercice 3 — Rendu de monnaie

## Objectif de l'exercice

Etant donné un ensemble de valeurs de pièces V = [v1, v2, ..., vp] et un montant N,
trouver la **combinaison qui utilise le moins de pièces** pour atteindre exactement N.

Exemple : V = [1, 2, 5], N = 13
- Solution optimale : 5+5+2+1 = 4 pièces
- Solution non optimale : 1×13 = 13 pièces

Deux méthodes sont implémentées :
1. **Backtracking avec élagage** : explore intelligemment en coupant les branches trop longues
2. **Recherche exhaustive** : génère toutes les combinaisons, puis choisit la meilleure

---

## Fichier `monnaie.py`

**Rôle :** Unique fichier de cet exercice. Contient les deux méthodes de résolution
et une fonction d'affichage.

---

### Fonction utilitaire `_construire_resultat(valeurs, choix, nombre_pieces)`

```python
detail = {}
for i in range(len(valeurs)):
    detail[valeurs[i]] = choix[i]
```
Construit un dictionnaire `{valeur_pièce: nombre_utilisé}`.

```python
return {
    "trouve": True,
    "nombre_pieces": nombre_pieces,
    "repartition": choix,
    "detail": detail,
}
```
Retourne un dictionnaire structuré décrivant la solution. Le champ `repartition` est
la liste brute des quantités (ex: [1, 1, 2] pour 1×pièce1 + 1×pièce2 + 2×pièce3).

---

### Méthode 1 : `rendre_monnaie_backtrack(valeurs, montant)`

**Idée :** Explorer toutes les combinaisons possibles en profondeur, mais couper
immédiatement les branches qui ne peuvent pas améliorer la meilleure solution connue.

```python
if montant < 0:
    return {"trouve": False}
if montant == 0:
    choix = [0 for _ in valeurs]
    return _construire_resultat(valeurs, choix, 0)
```
Cas limites : montant négatif → pas de solution, montant 0 → 0 pièce de chaque.

```python
meilleur_choix = None
meilleur_nombre = montant + 1   # pire cas théorique : tout en pièces de 1
```
On initialise le meilleur connu à `montant + 1` (valeur impossible, garantit qu'on
acceptera la première solution trouvée).

```python
choix = []
for _ in valeurs:
    choix.append(0)
```
`choix[i]` contiendra le nombre de pièces de valeur `valeurs[i]` choisi.

#### Fonction interne `backtrack(index, reste, nombre_actuel)`

```python
if index == len(valeurs):
    if reste == 0 and nombre_actuel < meilleur_nombre:
        meilleur_nombre = nombre_actuel
        meilleur_choix = list(choix)   # on copie
    return
```
Toutes les valeurs ont été traitées. Si le montant est exactement atteint et que c'est
mieux que la solution précédente, on la sauvegarde.

```python
if nombre_actuel >= meilleur_nombre:
    return
```
**Elagage clé :** si on a déjà utilisé autant (ou plus) de pièces que la meilleure
solution connue, cette branche ne peut pas l'améliorer. On coupe.

```python
piece = valeurs[index]
maximum = reste // piece
for nb in range(maximum, -1, -1):
    choix[index] = nb
    backtrack(index + 1, reste - nb * piece, nombre_actuel + nb)
```
Pour la pièce courante, on essaie tous les nombres possibles (de `maximum` à 0).
On commence par le maximum (stratégie gloutonne) car les solutions avec beaucoup de
grandes pièces sont souvent meilleures → on trouve vite une bonne borne supérieure.

```python
backtrack(0, montant, 0)
if meilleur_choix is None:
    return {"trouve": False}
return _construire_resultat(valeurs, meilleur_choix, meilleur_nombre)
```
Lance le backtracking depuis le début. Si aucune solution n'a été trouvée, retourne
l'échec.

---

### Méthode 2 : `rendre_monnaie_exhaustif(valeurs, montant)`

**Idée :** Générer **toutes** les combinaisons qui totalisent exactement N, puis
choisir celle qui utilise le moins de pièces. Pas d'élagage intermédiaire.

```python
toutes_les_solutions = []
choix = [0] * len(valeurs)
```
Liste pour stocker toutes les solutions valides.

#### Fonction interne `enumerer(index, reste)`

```python
if index == len(valeurs):
    if reste == 0:
        copie = list(choix)
        toutes_les_solutions.append(copie)
    return
```
Toutes les pièces traitées : si le montant est exactement 0, on sauvegarde.

```python
piece = valeurs[index]
maximum = reste // piece
for nb in range(0, maximum + 1):
    choix[index] = nb
    enumerer(index + 1, reste - nb * piece)
```
Contrairement au backtracking, on commence à 0 et monte jusqu'au maximum. **Pas
d'élagage** : on explore tout. C'est beaucoup plus lent pour les grands montants.

```python
enumerer(0, montant)
if len(toutes_les_solutions) == 0:
    return {"trouve": False}
```
Lance l'énumération complète.

```python
meilleur_choix = toutes_les_solutions[0]
meilleur_nombre = sum(meilleur_choix)

for solution in toutes_les_solutions:
    nombre = sum(solution)
    if nombre < meilleur_nombre:
        meilleur_nombre = nombre
        meilleur_choix = solution
```
Parcourt toutes les solutions trouvées et garde celle avec le plus petit nombre total
de pièces.

---

### Fonction `afficher_solution_monnaie(valeurs, resultat)`

```python
if not resultat["trouve"]:
    print("Aucune solution possible.")
    return
print("Nombre total de pieces : " + str(resultat["nombre_pieces"]))
for i in range(len(valeurs)):
    piece = valeurs[i]
    nb = resultat["repartition"][i]
    print("  piece " + str(piece) + " : " + str(nb))
```
Affiche le résultat de façon lisible : nombre total de pièces, puis détail par
valeur.

---

## Comparaison des deux méthodes

| Aspect              | Backtracking                          | Exhaustif                             |
|---------------------|---------------------------------------|---------------------------------------|
| Exploration         | Profondeur + élagage                  | Exhaustive (toutes combinaisons)      |
| Rapidité            | Plus rapide (branches coupées)        | Plus lent (aucun élagage)             |
| Mémoire             | O(profondeur) = O(nombre de valeurs)  | O(nombre de solutions)                |
| Garantie d'optimalité | Oui (élagage sûr)                  | Oui (on voit tout)                    |
| Résultat            | Identique                             | Identique                             |

---

## Lien avec la programmation par contraintes

Ce problème est un cas classique d'**optimisation combinatoire** :
- **Variables :** quantité de chaque pièce (x1, x2, ..., xp)
- **Contrainte :** x1×v1 + x2×v2 + ... + xp×vp = N et xi ≥ 0
- **Objectif :** minimiser x1 + x2 + ... + xp (nombre total de pièces)

L'élagage du backtracking est une forme de **branch and bound** : on maintient
une borne supérieure (meilleure solution connue) et on coupe dès qu'on ne peut
plus l'améliorer.
