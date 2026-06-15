# TP Pruning : Algorithmes de Filtrage et Visualisation

---

## [cite_start]Exercice 1 : Implémentation et Visualisation d'AC3 [cite: 1]

[cite_start]L'objectif de cet exercice est de concevoir un programme qui ne se contente pas de résoudre un problème de contraintes, mais qui en expose la mécanique interne par une **représentation graphique pas à pas**[cite: 2].

### [cite_start]1. Objectifs techniques [cite: 3]
* [cite_start]Représenter le **Graphe de Contraintes** de manière visuelle[cite: 4].
* [cite_start]Afficher dynamiquement l'évolution de la **File (Queue)** des arcs à examiner[cite: 5].
* [cite_start]Visualiser la réduction des **Domaines** des variables en temps réel[cite: 6].
* [cite_start]Mettre en évidence les étapes de **Propagation** (réinsertion d'arcs dans la file)[cite: 7].

### [cite_start]2. Cahier des charges de l'application [cite: 8]
[cite_start]Votre programme doit produire une série de "clichés" (ou une animation) correspondant aux étapes clés[cite: 9].

---

### transcription-visuelle_illustration-1">**Transcription de l'Illustration 1 : Visualisation détaillée de l'algorithme AC3 (Arc-Consistance)**

Cette image présente un tableau de bord didactique divisé en trois phases principales (État Initial, Boucle Principale, État Final) pour résoudre un CSP à 3 variables.

#### A. ÉTAT INITIAL (Partie Gauche)
1. **Graphe de contraintes initial :** * Trois variables sous forme de nœuds bleus : $X$, $Y$ et $Z$.
   * Chaque variable est associée à son domaine initial affiché dans une petite boîte : $X:\{1, 2\}$, $Y:\{1, 2\}$, $Z:\{1, 2\}$.
   * Des flèches bleues orientées relient les nœuds pour former les arcs du graphe (boucles bidirectionnelles entre $X \leftrightarrow Y$ et $Y \leftrightarrow Z$, ainsi qu'un arc de $X$ vers $Z$).
2. **File d'arcs initiale ($Q$) :** * Représentée verticalement comme une pile/file contenant les arcs orientés à examiner : `(X,Y)`, `(Y,X)`, `(Y,Z)`, `(Z,Y)`.
3. **Vérification de cohérence locale :**
   * Un schéma miniature montre un triangle $X \rightarrow Y \rightarrow Z$ labellisé partout "COHÉRENT".

#### B. BOUCLE PRINCIPALE / ITÉRATIONS (Partie Centrale)

* **1. Arc examiné : $(X,Y)$ (Contrainte $X < Y$)**
  * *Visuel du graphe :* L'arc reliant $X$ à $Y$ est surligné en orange.
  * *Action `REVISE(X,Y)` :* Une boîte affiche la suppression de la valeur $2$ du domaine de $X$ car elle ne respecte pas $X < Y$ (le chiffre 2 est barré d'une croix rouge).
  * *Résultat :* $D(X) = \{1\}$, validé par une coche verte.
  * *Propagation :* Nouveaux arcs réinsérés : Aucun. La file $Q$ se vide de $(X,Y)$ mais conserve $(Y,X)$.

* **2. Arc examiné : $(Y,X)$ (Contrainte $Y > X$)**
  * *Visuel du graphe :* L'arc inverse de $Y$ vers $X$ est surligné en orange.
  * *Action `REVISE(Y,X)` :* La valeur $1$ est supprimée du domaine de $Y$ (barrée d'une croix rouge) car avec $D(X)=\{1\}$, il n'existe aucune valeur dans $X$ inférieure à $1$.
  * *Résultat :* $D(Y) = \{2\}$, validé par un carré vert.
  * *Propagation :* L'arc $(Z,Y)$ est réinséré de force dans la file pour vérifier l'impact de la modification de $Y$. Une icône verte indique *"Arc (Z,Y) réinséré !"* et la file $Q$ affiche l'arc `(Z,Y)` surligné en vert avec des rayons lumineux.

* **3. Arc examiné : $(Y,Z)$ (Contrainte $Y = Z$)**
  * *Visuel du graphe :* L'arc reliant $Y$ à $Z$ est surligné en orange, l'arc du bas est vert.
  * *Action `REVISE(Y,Z)` :* $D(Y)=\{2\}$ et $D(Z)=\{2\}$. Une ligne relie les deux valeurs.
  * *Résultat :* Aucune suppression nécessaire. La file $Q$ n'est pas modifiée.

#### C. ÉTAT FINAL (Partie Basse)
* Le graphe est stabilisé. Les boîtes affichent les domaines finis réduits : $\{1\} \xrightarrow{\text{COHÉRENT}} \{2\} \xrightarrow{\text{COHÉRENT}} \{2\}$.
* Un message de conclusion s'affiche avec une grande coche verte : **"CSP EST ARC-CONSISTANT"**.

---

* [cite_start]**Vue "État Initial"** : Affichage du graphe complet avec tous les domaines au maximum et la file $Q$ remplie de tous les arcs orientés[cite: 10].
* **Vue "Traitement de l'Arc"** :
  * [cite_start]Surligner l'arc $(X, Y)$ actuellement extrait de la file[cite: 12].
  * [cite_start]Afficher l'appel à la fonction `Revise(X, Y)`[cite: 13].
* **Vue "Suppression & Mise à jour"** :
  * [cite_start]Barrage visuel des valeurs supprimées du domaine $D(X)$[cite: 15].
  * [cite_start]Si le domaine est modifié, afficher visuellement quels arcs voisins sont réinsérés dans la file $Q$ (ex: apparition d'une icône de recyclage ou surbrillance)[cite: 16].
* [cite_start]**Vue "État Final"** : Affichage du graphe stabilisé (Arc-Consistant) ou signalement d'un échec si un domaine devient vide[cite: 17].

### [cite_start]3. Exemple de test imposé [cite: 18]
[cite_start]Utilisez les données suivantes pour valider votre visualisation[cite: 19]:
* [cite_start]**Variables** : $X, Y, Z$ [cite: 20]
* [cite_start]**Domaines** : $D(X)=\{1, 2\}$, $D(Y)=\{1, 2\}$, $D(Z)=\{1, 2\}$[cite: 21].
* [cite_start]**Contraintes** : $X < Y$ et $Y = Z$[cite: 22].

### [cite_start]4. Recommandations technologiques [cite: 23]
[cite_start]Pour la partie graphique, vous pouvez utiliser au choix[cite: 24]:
* [cite_start]**Python** : NetworkX pour la logique de graphe et Matplotlib ou Pyvis pour le rendu HTML interactif[cite: 25].
* [cite_start]**JavaScript** : D3.js ou Cytoscape.js pour une visualisation fluide directement dans le navigateur[cite: 26].

> [cite_start]**Consigne de rendu** : Votre programme doit permettre de naviguer entre les étapes (boutons "Suivant / Précédent") pour que l'on puisse observer précisément à quel moment une valeur est retirée et pourquoi un arc est revenu dans la file d'attente[cite: 27].

---

## [cite_start]Exercice 2 : Filtrage de AllDifferent (Algorithme de Régin) [cite: 28]

[cite_start]L'objectif est d'implémenter un outil de visualisation qui décompose le filtrage global de la contrainte `AllDifferent`[cite: 29]. [cite_start]Le programme doit montrer comment une vision "graphe" permet de supprimer des valeurs que de simples contraintes binaires ne verraient pas[cite: 30].

### [cite_start]1. Objectifs techniques [cite: 31]
* [cite_start]Construire et afficher le **Graphe Biparti** variables-valeurs[cite: 32].
* [cite_start]Visualiser le calcul du **Couplage Maximum** (Matching)[cite: 33].
* [cite_start]Transformer le graphe en **Graphe Orienté de Résidu**[cite: 34].
* [cite_start]Identifier et colorer les **Composantes Fortement Connexes (SCC)** pour justifier la suppression des arcs[cite: 35].

### [cite_start]2. Étapes de visualisation à implémenter [cite: 36]
[cite_start]Le programme devra générer les vues successives suivantes[cite: 37]:

* **Vue Bipartie Initiale** : À gauche, les variables $X_i$, à droite, l'union de leurs domaines. [cite_start]Les arcs représentent les valeurs possibles pour chaque variable[cite: 38, 39, 40].
* **Vue "Couplage Maximum"** : Mise en évidence (en gras ou en couleur) des arcs sélectionnés pour le couplage. [cite_start]Affichage d'un message indiquant si un couplage complet a été trouvé (sinon, le problème est insatisfaisable)[cite: 41, 42, 43].
* **Vue "Graphe de Résidu"** : Orientation des arcs : du domaine vers les variables pour le couplage, et inversement pour les autres. [cite_start]Affichage des cycles et des chemins alternés[cite: 44, 45, 46].
* **Vue "Filtrage Final"** : Surlignage des SCC (Composantes Fortement Connexes) trouvées par l'algorithme (ex: Tarjan). [cite_start]Animation de suppression : Faire disparaître les arcs qui ne sont ni dans le couplage, ni dans un cycle, ni sur un chemin valide[cite: 47, 48, 49].

---

### transcription-visuelle_illustration-2">**Transcription de l'Illustration 2 : Étapes de l'Algorithme de Régin pour AllDifferent**

Cette infographie technique à fond sombre détaille les quatre étapes de l'algorithme de Régin appliqué à un système de 4 variables.

#### ÉTAPE 1 : GRAPHE BIPARTI INITIAL
* **Structure du Graphe ($G = (V \cup D, E)$) :**
  * Colonne de gauche (Variables $V$) : Quatre nœuds bleus notés $x_1, x_2, x_3, x_4$.
  * Leurs domaines respectifs sont listés à côté : $D(x_1)=\{1,2\}$, $D(x_2)=\{1,2\}$, $D(x_3)=\{2,3\}$, $D(x_4)=\{2,3,4,5\}$.
  * Colonne de droite (Domaines $D$) : Quatre nœuds orange représentant les valeurs cibles distinctes : $1, 2, 3, 5$ (Note : le nœud inférieur est étiqueté 5 mais correspond à la réserve de valeurs).
  * Les liaisons (arcs gris non orientés) forment toutes les affectations initialement possibles.
* **Statut :** Une boîte en bas à gauche indique une coche verte : **"Couplage possible !"**.

#### ÉTAPE 2 : COUPLAGE MAXIMUM (MATCHING)
* Le même graphe biparti est représenté, mais un sous-ensemble d'arcs est sélectionné pour former un couplage maximum.
* **Arcs de couplage (Surlignés en vert fluo épais) :**
  * $x_1$ est lié à $1$
  * $x_2$ est lié à $2$
  * $x_3$ est lié à $3$
  * $x_4$ est lié à $4$ (représenté par le nœud du bas)
* **Légende en bas :** Le Couplage Maximum (Matching) trouvé est écrit textuellement : $M = \{(x_1,1), (x_2,2), (x_3,3), (x_4,4)\}$.

#### ÉTAPE 3 : GRAPHE DE RÉSIDU (ORIENTÉ)
* Le graphe change radicalement de structure visuelle pour illustrer le graphe de résidu ($G_M$).
* **Règles d'orientation des flèches :**
  * **Arcs de Couplage ($M$) :** Flèches épaisses vert fluo orientées de la droite vers la gauche (des Valeurs vers les Variables), par exemple: $(1 \rightarrow x_1)$.
  * **Arcs Hors Couplage ($E \setminus M$) :** Flèches fines bleues orientées de la gauche vers la droite (des Variables vers les Valeurs), par exemple: $(x_1 \rightarrow 2)$.
* **Chemins Alternés :** Des flèches et des lignes directrices en bas mettent en évidence des structures spécifiques appelées "CHEMIN ALTERNÉ VALIDE" transitant entre les valeurs $(1 \rightarrow 2 \rightarrow 1)$.

#### ÉTAPE 4 : SCC & FILTRAGE FINAL
* L'étape finale montre l'identification des Composantes Fortement Connexes (SCC) et l'élagage final des arcs superflus.
* **Zones de couleur (SCC détectées) :**
  * **SCC1 (Zone Jaune) :** Regroupe les nœuds $\{x_1, x_2, 1, 2\}$. Les arcs internes à cette zone sont marqués comme "ARC CONSERVÉ (dans SCC)".
  * **SCC2 (Zone Violette) :** Regroupe les nœuds $\{x_3, 3\}$.
* **Le Filtrage (Action d'élagage) :**
  * L'arc reliant la variable $x_4$ au nœud de valeur $2$, ainsi que l'arc reliant $x_3$ au nœud de valeur $2$ sont surlignés en rouge vif avec une **grosse croix rouge (X)**.
  * Une flèche pointe sur ces éléments avec la mention **"ARC INUTILE (ni M, ni SCC, ni chemin)"**.
* **Résultat - Domaines Filtrés :**
  * En bas à droite, le résultat de la réduction est affiché : $D(x_3) = \{3\}$ et $D(x_4) = \{3, 4, 5\}$.

---

### [cite_start]3. Exemple de test imposé [cite: 50]
[cite_start]Utilisez ce cas classique où le filtrage global surpasse l'arc-consistance binaire[cite: 51]:
* [cite_start]$x_1 \in \{1, 2\}$ [cite: 52]
* [cite_start]$x_2 \in \{1, 2\}$ [cite: 53]
* [cite_start]$x_3 \in \{2, 3\}$ [cite: 54]
* [cite_start]$x_4 \in \{2, 3, 4, 5\}$ [cite: 55]

> [cite_start]**Note** : Ici, $x_1$ et $x_2$ saturent les valeurs $\{1, 2\}$[cite: 56]. [cite_start]La valeur 2 doit donc être supprimée des domaines de $x_3$ et $x_4$[cite: 57]. [cite_start]Votre programme doit montrer visuellement pourquoi l'arc $(x_3, 2)$ est supprimé[cite: 58].

### [cite_start]4. Contraintes de développement [cite: 59]
* [cite_start]**Logique Graphe** : Utilisation impérative d'un algorithme de détection de SCC (Tarjan ou Kosaraju)[cite: 60].
* [cite_start]**Interactivité** : Comme pour l'exercice 1, l'utilisateur doit pouvoir cliquer sur "Suivant" pour voir le graphe changer d'état (notamment le changement d'orientation des arcs)[cite: 61].

---

## [cite_start]Livrable attendu [cite: 62]

[cite_start]Un **tableau comparatif** généré par le programme montrant les domaines *avant* et *après* le passage de l'algorithme de Régin, accompagné des graphiques exportés pour chaque étape clé[cite: 63].

---

## Utilisation (ligne de commande)

Depuis la racine du projet (apres `pip install -r requirements.txt`) :

```powershell
# Exercice 1 — AC3 (visualisation interactive)
python -m pruning.main_pruning --exercice 1

# Exercice 2 — Regin / AllDifferent
python -m pruning.main_pruning --exercice 2

# Les deux exercices
python -m pruning.main_pruning --exercice 0

# Export PNG de chaque etape (sans ouvrir la fenetre)
python -m pruning.main_pruning --exercice 1 --export --no-show
python -m pruning.main_pruning --exercice 2 --export --no-show
python -m pruning.main_pruning --export --no-show
```

Les images sont enregistrees dans `pruning/exports/` (`ac3_01.png`, `regin_01.png`, etc.).
Voir aussi [README.md](../README.md) pour les autres exercices du depot.