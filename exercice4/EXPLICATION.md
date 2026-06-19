# Exercice 4 — Mastermind simplifié

## Objectif de l'exercice

Le **Mastermind** est un jeu de déduction : un joueur choisit un code secret
(une séquence de couleurs) et l'autre joueur doit le deviner en un minimum
d'essais. Après chaque essai, le joueur reçoit des indices :

- **Bien placées :** bonne couleur à la bonne position
- **Mal placées :** bonne couleur mais à la mauvaise position

L'exercice implémente une **IA** qui joue le rôle du devineur.

Exemple avec 3 couleurs (R, V, B) et un code de longueur 3 :
- Secret : [R, V, B]
- Essai 1 : [R, R, R] → bien=1, mal=0
- Essai 2 : [R, V, V] → bien=2, mal=0
- Essai 3 : [R, V, B] → bien=3, mal=0 → trouvé !

Deux méthodes sont implémentées :
1. **Exhaustif :** maintient une liste des codes encore possibles, filtre après chaque essai
2. **Backtracking :** reconstruit les codes possibles par backtracking après chaque essai

---

## Fichier `mastermind.py`

**Rôle :** Unique fichier de cet exercice. Contient le calcul des indices, les deux
stratégies de résolution, et un mode interactif.

---

### Fonction `calculer_indice(secret, proposition)`

**Rôle :** Calcule le feedback (bien_placées, mal_placées) pour une proposition.

```python
bien_placees = 0
secret_reste = []
prop_reste = []

for i in range(len(secret)):
    if secret[i] == proposition[i]:
        bien_placees = bien_placees + 1
    else:
        secret_reste.append(secret[i])
        prop_reste.append(proposition[i])
```
**Première passe :** on compte les positions exactes (même couleur, même place).
Les couleurs non exactement placées sont séparées dans deux listes `_reste`.

```python
mal_placees = 0
for couleur in prop_reste:
    if couleur in secret_reste:
        mal_placees = mal_placees + 1
        secret_reste.remove(couleur)
```
**Deuxième passe :** pour chaque couleur de la proposition non bien placée, on
cherche si elle existe dans les restes du secret. Si oui, c'est une couleur mal
placée. On **retire** la couleur de `secret_reste` pour éviter de la compter deux
fois (ex: si le secret a 1 rouge et la proposition en a 2, on ne compte qu'1 mal placé).

---

### Fonction `generer_toutes_combinaisons(couleurs, longueur)`

**Rôle :** Génère toutes les combinaisons possibles (produit cartésien).

```python
resultat = []
def construire(prefixe):
    if len(prefixe) == longueur:
        copie = list(prefixe)
        resultat.append(copie)
        return
    for couleur in couleurs:
        prefixe.append(couleur)
        construire(prefixe)
        prefixe.pop()
construire([])
return resultat
```
Backtracking classique : on construit le code couleur par couleur. Quand le préfixe
atteint la bonne longueur, on sauvegarde. **Pas de contrainte** ici : on génère
tout. Pour `n` couleurs et longueur `L`, cela produit `n^L` combinaisons.

---

### Fonction `filtrer_candidats(candidats, proposition, indice_attendu)`

**Rôle :** Elimine les codes incompatibles avec le dernier indice reçu.

```python
restants = []
for candidat in candidats:
    indice = calculer_indice(candidat, proposition)
    if indice[0] == indice_attendu[0] and indice[1] == indice_attendu[1]:
        restants.append(candidat)
return restants
```
Pour chaque candidat encore possible, on simule : "si ce candidat était le secret,
quel indice donnerait la proposition ?". Si cet indice correspond à l'indice réel
reçu, le candidat reste. Sinon, il est éliminé.

---

### Fonction `combinaison_compatible(combinaison, historique)`

**Rôle :** Vérifie si une combinaison est compatible avec **tout** l'historique.

```python
for proposition, indice_attendu in historique:
    indice = calculer_indice(combinaison, proposition)
    if indice[0] != indice_attendu[0] or indice[1] != indice_attendu[1]:
        return False
return True
```
Parcourt tous les essais passés. La combinaison doit être cohérente avec chacun
d'eux. Un seul échec suffit à la disqualifier.

---

### Fonction `trouver_candidats_backtrack(couleurs, longueur, historique)`

**Rôle :** Reconstruit les candidats valides par backtracking.

```python
candidats = []
def backtrack(prefixe):
    if len(prefixe) == longueur:
        if combinaison_compatible(prefixe, historique):
            candidats.append(list(prefixe))
        return
    for couleur in couleurs:
        prefixe.append(couleur)
        backtrack(prefixe)
        prefixe.pop()
backtrack([])
return candidats
```
Construit le code couleur par couleur. Quand le code est complet, on vérifie sa
compatibilité avec l'historique. **Note :** l'élagage pourrait se faire en cours de
construction (en vérifiant partiellement à chaque étape), mais ici la vérification
est faite uniquement à la fin — c'est donc une génération exhaustive avec filtrage.

---

### Fonction `resoudre_mastermind_exhaustif(secret, couleurs, max_tentatives=20)`

**Rôle :** L'IA joue en maintenant une liste de candidats et en la filtrant.

```python
longueur = len(secret)
candidats = generer_toutes_combinaisons(couleurs, longueur)
historique = []
tentatives = 0
```
Initialisation : tous les codes sont candidats.

```python
while tentatives < max_tentatives:
    if len(candidats) == 0:
        break
    proposition = candidats[0]
```
L'IA propose toujours **le premier candidat restant** (stratégie simple, pas
optimale). Une stratégie plus élaborée choisirait la proposition qui élimine le
maximum de candidats.

```python
    indice = calculer_indice(secret, proposition)
    historique.append((proposition, indice))
    tentatives = tentatives + 1
```
On calcule l'indice réel et on l'enregistre dans l'historique.

```python
    if indice[0] == longueur:
        return {"trouve": True, "tentatives": tentatives, ...}
    candidats = filtrer_candidats(candidats, proposition, indice)
```
Si toutes les positions sont bonnes, le secret est trouvé. Sinon, on filtre les
candidats restants selon l'indice reçu.

---

### Fonction `resoudre_mastermind_backtrack(secret, couleurs, max_tentatives=20)`

**Rôle :** Même logique mais recalcule les candidats par backtracking à chaque tour.

```python
while tentatives < max_tentatives:
    candidats = trouver_candidats_backtrack(couleurs, longueur, historique)
    if len(candidats) == 0:
        break
    proposition = candidats[0]
    indice = calculer_indice(secret, proposition)
    historique.append((proposition, indice))
    tentatives = tentatives + 1
    if indice[0] == longueur:
        return {"trouve": True, ...}
```
**Différence clé :** au lieu de filtrer une liste existante, on **regénère** les
candidats à chaque tour en parcourant tout l'espace de recherche et en vérifiant
l'historique complet. Plus lent que la méthode exhaustive car on répète le travail,
mais illustre la puissance du backtracking avec contraintes.

---

### Fonction `afficher_historique_mastermind(historique)`

```python
num = 1
for proposition, indice in historique:
    texte = " ".join(str(c) for c in proposition)
    print("  Tentative " + str(num) + " : " + texte +
          "| bien placees=" + str(indice[0]) +
          ", mal placees=" + str(indice[1]))
    num = num + 1
```
Affiche chaque tentative avec la proposition et l'indice associé.

---

### Fonction `jouer_mastermind_interactif(couleurs, longueur, methode, max_tentatives)`

**Rôle :** Mode interactif : l'utilisateur entre son secret, l'IA le devine.

```python
entree = input("Secret : ")
parties = entree.strip().split()
secret = list(parties)
```
Lecture du secret depuis le clavier, séparé par des espaces.

```python
if len(secret) != longueur:
    print("Erreur : mauvaise longueur de secret.")
    return
for couleur in secret:
    if couleur not in couleurs:
        print("Erreur : couleur inconnue " + couleur)
        return
```
Validation du secret : bonne longueur et couleurs connues.

```python
if methode == "backtrack":
    resultat = resoudre_mastermind_backtrack(secret, couleurs, max_tentatives)
else:
    resultat = resoudre_mastermind_exhaustif(secret, couleurs, max_tentatives)
```
Choisit la méthode de résolution selon le paramètre.

---

## Comparaison des deux méthodes

| Aspect             | Exhaustif                              | Backtracking                           |
|--------------------|----------------------------------------|----------------------------------------|
| Candidats initiaux | Générés une fois au début              | Régénérés à chaque tour                |
| Mise à jour        | Filtre la liste existante              | Reconstruit depuis zéro                |
| Mémoire            | Stocke tous les candidats restants     | Pas de stockage (recalcul)             |
| Vitesse            | Rapide (filtre incrémental)            | Plus lent (recalcul complet)           |
| Résultat           | Identique (même candidat choisi)       | Identique                              |

---

## Lien avec la programmation par contraintes

Le Mastermind est un problème de **satisfaction de contraintes** (CSP) :
- **Variables :** les couleurs aux positions 1, 2, ..., L
- **Domaine :** l'ensemble des couleurs disponibles
- **Contraintes :** chaque indice reçu est une contrainte sur les variables
  (ex: "au moins 2 couleurs bien placées par rapport à l'essai [R,V,B]")

La méthode backtracking illustre directement comment un solveur CP travaille :
il essaie des valeurs, vérifie les contraintes, et revient en arrière si une
contradiction est détectée.
