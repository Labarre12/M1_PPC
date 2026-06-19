# Exercice 1 — Enumération de mots par distance de Levenshtein

## Objectif de l'exercice

Etant donné un mot de référence M et un entier k, trouver **tous les mots** de
l'alphabet malgache qui sont à une distance de Levenshtein **inférieure ou égale à k**
de M. Trois méthodes différentes sont implémentées et comparées :

- **BFS** (parcours en largeur)
- **Backtracking** (retour arrière) — deux variantes
- **CP** (programmation par contraintes avec élagage)

---

## Fichier `alphabet.py` (racine du projet)

```python
ALPHABET = "abdefghijklmnoprstvyz"
```

Définit l'alphabet malgache (21 lettres). Il manque c, q, u, w, x par rapport à
l'alphabet latin. Toutes les fonctions de cet exercice n'acceptent que des mots
composés de ces lettres.

---

## Fichier `levenshtein.py`

**Rôle :** Calcule la distance de Levenshtein entre deux mots, et valide qu'un mot
appartient bien à l'alphabet malgache. C'est le module de base utilisé par tous les
autres.

### Fonction `distance_levenshtein(mot_a, mot_b)`

```python
n = len(mot_a)
m = len(mot_b)
```
On note n la longueur du premier mot, m celle du second.

```python
dp = []
for i in range(n + 1):
    ligne = []
    for j in range(m + 1):
        ligne.append(0)
    dp.append(ligne)
```
On construit un tableau 2D `dp` de taille (n+1) × (m+1), initialisé à zéro.
`dp[i][j]` contiendra la distance minimale entre les i premières lettres de mot_a
et les j premières lettres de mot_b.

```python
for i in range(n + 1):
    dp[i][0] = i
for j in range(m + 1):
    dp[0][j] = j
```
Cas de base : transformer les i premières lettres de mot_a en une chaîne vide coûte
i suppressions. Transformer une chaîne vide en les j premières lettres de mot_b coûte
j insertions.

```python
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if mot_a[i - 1] == mot_b[j - 1]:
            cout = 0
        else:
            cout = 1
```
Pour chaque paire de lettres, si elles sont identiques la substitution est gratuite
(coût 0), sinon elle coûte 1.

```python
        suppression  = dp[i - 1][j] + 1
        insertion    = dp[i][j - 1] + 1
        substitution = dp[i - 1][j - 1] + cout
        dp[i][j]     = min(suppression, insertion, substitution)
```
On choisit l'opération la moins chère parmi :
- supprimer la lettre i de mot_a → `dp[i-1][j] + 1`
- insérer une lettre dans mot_a  → `dp[i][j-1] + 1`
- substituer la lettre i         → `dp[i-1][j-1] + cout`

```python
    return dp[n][m]
```
La distance finale est dans le coin inférieur droit du tableau.

---

### Fonction `mot_valide(mot)`

```python
if mot == "":
    return False
```
Un mot vide n'est pas valide (on veut des mots non vides).

```python
for lettre in mot:
    if lettre not in ALPHABET:
        return False
return True
```
On vérifie que chaque lettre appartient à l'alphabet malgache.

---

## Fichier `enum_bfs.py`

**Rôle :** Enumère tous les mots à distance ≤ k en explorant le graphe d'édition
**niveau par niveau** (BFS = Breadth-First Search / Parcours en largeur). C'est la
méthode de référence : simple, correcte, garantit de trouver les mots dans l'ordre
croissant de distance.

### Fonction `voisins(mot)`

Génère tous les mots à exactement 1 opération d'édition du mot donné.

```python
resultat = set()
```
Un ensemble pour éviter les doublons.

**Suppressions :**
```python
for i in range(len(mot)):
    nouveau = mot[:i] + mot[i + 1:]
    resultat.add(nouveau)
```
Pour chaque position i, on retire la lettre i. `mot[:i]` = début, `mot[i+1:]` = fin.

**Insertions :**
```python
for i in range(len(mot) + 1):
    for lettre in ALPHABET:
        nouveau = mot[:i] + lettre + mot[i:]
        resultat.add(nouveau)
```
Pour chaque position (y compris avant le 1er et après le dernier caractère) et chaque
lettre de l'alphabet, on insère la lettre.

**Substitutions :**
```python
for i in range(len(mot)):
    for lettre in ALPHABET:
        if lettre != mot[i]:
            nouveau = mot[:i] + lettre + mot[i + 1:]
            resultat.add(nouveau)
```
Pour chaque position, on remplace la lettre par une autre lettre de l'alphabet.

```python
mots_valides = set()
for candidat in resultat:
    if mot_valide(candidat):
        mots_valides.add(candidat)
return mots_valides
```
On filtre pour ne garder que les mots utilisant uniquement l'alphabet malgache.

---

### Fonction `enumerer_mots_bfs(mot_reference, k)`

```python
longueur_min = max(0, len(mot_reference) - k)
longueur_max = len(mot_reference) + k
```
Un mot à distance ≤ k du mot de référence ne peut pas être plus court de k lettres
ni plus long de k lettres. C'est un élagage de taille.

```python
deja_vus      = {mot_reference}
niveau_courant = {mot_reference}
tous_les_mots  = {mot_reference}
```
On part du mot de référence, marqué comme déjà vu.

```python
for distance in range(k):
    niveau_suivant = set()
    for mot in niveau_courant:
        for voisin in voisins(mot):
            if voisin in deja_vus:
                continue
            if len(voisin) < longueur_min or len(voisin) > longueur_max:
                continue
            deja_vus.add(voisin)
            niveau_suivant.add(voisin)
            tous_les_mots.add(voisin)
    niveau_courant = niveau_suivant
```
À chaque itération, on explore les voisins du niveau courant. On ignore les mots déjà
vus (pour éviter les cycles) et les mots trop courts/longs (élagage). Le nouveau
niveau devient le niveau courant.

```python
liste_triee = list(tous_les_mots)
liste_triee.sort()
return liste_triee
```
On retourne les résultats triés alphabétiquement.

---

### Fonction `enumerer_mots_par_distance(mot_reference, k)`

Même logique que `enumerer_mots_bfs` mais stocke les résultats groupés par distance
exacte (0, 1, 2, ..., k) dans un dictionnaire.

---

## Fichier `enum_backtrack.py`

**Rôle :** Deux variantes de backtracking (exploration en profondeur avec retour
arrière). Même résultat que BFS mais explore différemment.

### Variante 1 : Backtracking sur les opérations d'édition

#### `backtrack_edition(mot, profondeur, k, longueur_min, longueur_max, chemin, resultats)`

```python
if longueur_min <= len(mot) <= longueur_max:
    resultats.add(mot)
```
Si le mot courant a une longueur acceptable, on l'ajoute aux résultats.

```python
if profondeur >= k:
    return
```
Élagage : si on a déjà fait k opérations, pas la peine d'aller plus loin.

```python
for voisin in voisins(mot):
    if voisin in chemin:
        continue
    chemin.add(voisin)
    backtrack_edition(voisin, profondeur + 1, k, ...)
    chemin.remove(voisin)  # backtracking
```
On explore chaque voisin non encore visité sur la branche courante. Le `chemin`
contient les mots de la branche en cours. Après l'appel récursif, on retire le
voisin du chemin (c'est le retour arrière = backtracking).

#### `enumerer_mots_backtrack_edition(mot_reference, k)`

Initialise `chemin = {mot_reference}` et `resultats = set()`, puis lance la
récursion. Trie et retourne les résultats.

---

### Variante 2 : Backtracking sur la construction du mot

#### `backtrack_construction(mot_reference, k, longueur, prefixe, resultats)`

Au lieu de naviguer dans le graphe d'édition, on **construit** un mot lettre par
lettre et on vérifie à la fin si sa distance est ≤ k.

```python
if len(prefixe) == longueur:
    mot = ""
    for lettre in prefixe:
        mot = mot + lettre
    if distance_levenshtein(mot_reference, mot) <= k:
        resultats.add(mot)
    return
```
Cas de base : le mot est complet. On calcule sa distance et on l'ajoute si elle est ≤ k.

```python
cases_restantes = longueur - len(prefixe)
for lettre in ALPHABET:
    prefixe.append(lettre)
    mot_partiel = "".join(prefixe)  # version lisible : on concatène
    distance = distance_levenshtein(mot_reference, mot_partiel)
    if distance <= k + cases_restantes - 1:
        backtrack_construction(...)
    prefixe.pop()
```
**Élagage clé :** si la distance du préfixe actuel est déjà trop grande (> k +
cases_restantes - 1), on abandonne cette branche. En effet, chaque lettre restante
peut au mieux réduire la distance de 1, donc si on est déjà trop loin, ça ne sert à
rien de continuer.

#### `enumerer_mots_backtrack_construction(mot_reference, k)`

Lance la construction pour chaque longueur possible (de `len(M)-k` à `len(M)+k`).

---

## Fichier `enum_cp.py`

**Rôle :** Programmation par contraintes (CP). Construit le mot lettre par lettre
avec un élagage plus rigoureux grâce à une contrainte explicite.

### Fonction `prefixe_encore_possible(mot_reference, prefixe, k, longueur_voulue)`

```python
cases_restantes = longueur_voulue - len(prefixe)
distance = distance_levenshtein(mot_reference, prefixe)
return distance <= k + cases_restantes
```
Vérifie si le préfixe actuel peut encore aboutir à un mot valide. La contrainte est :
`distance_actuelle ≤ k + cases_restantes`. Cela signifie que même si chaque lettre
restante coûte 0 (cas idéal), on doit rester dans les k opérations autorisées.

**Différence avec backtrack_construction :** ici la borne est `k + cases_restantes`
(sans le -1 de la variante 2), ce qui est la formulation exacte de la faisabilité.

### Fonction `chercher_mot(mot_reference, k, longueur, prefixe, resultats)`

```python
if len(prefixe) == longueur:
    mot = "".join(prefixe)
    if distance_levenshtein(mot_reference, mot) <= k:
        resultats.add(mot)
    return
```
Cas de base identique à la variante 2.

```python
for lettre in ALPHABET:
    prefixe.append(lettre)
    mot_partiel = "".join(prefixe)
    if prefixe_encore_possible(mot_reference, mot_partiel, k, longueur):
        chercher_mot(mot_reference, k, longueur, prefixe, resultats)
    prefixe.pop()  # backtracking
```
Pour chaque lettre, on vérifie la contrainte **avant** de plonger dans la récursion.
Si le préfixe n'est plus faisable, on écrête la branche immédiatement.

### Fonction `enumerer_mots_cp(mot_reference, k)`

Lance `chercher_mot` pour chaque longueur possible et retourne les résultats triés.

---

## Synthèse des 3 méthodes

| Méthode              | Exploration | Elagage                            | Avantage                          |
|----------------------|-------------|-------------------------------------|-----------------------------------|
| BFS                  | En largeur  | Longueur min/max, mots déjà vus     | Trouve les plus proches en premier |
| Backtrack (édition)  | En profondeur | Même que BFS                       | Plus simple à comprendre           |
| Backtrack (construction) | En profondeur | Distance partielle + cases restantes | Evite de générer des mots impossibles |
| CP                   | En profondeur | Contrainte de faisabilité stricte  | Elagage le plus efficace           |

Toutes les méthodes retournent exactement le même ensemble de mots.
