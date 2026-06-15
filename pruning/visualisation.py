# TP Pruning - Couche visualisation (Matplotlib + NetworkX)
#
# Lecteur commun qui rejoue une liste de "snapshots" pas a pas :
#   - navigation interactive avec les boutons "Precedent" / "Suivant" ;
#   - export de chaque etape en PNG.
#
# Deux types de dessin sont fournis :
#   - creer_dessin_ac3  : graphe de contraintes + file Q (Exercice 1) ;
#   - creer_dessin_regin: graphe biparti / residu / SCC (Exercice 2).

import os

import matplotlib.pyplot as plt
from matplotlib import widgets
import networkx as nx


# Palette pour colorer les composantes fortement connexes (Exercice 2).
PALETTE_SCC = [
    "#f4d35e", "#c8a2ff", "#8ed1a0", "#ff9aa2",
    "#9ad0ec", "#ffb997", "#b5e48c", "#d0a3bf",
]


def _fleche(ax, depart, arrivee, couleur, largeur=2.5, rad=0.08,
            style="-|>", tirets=False):
    """Trace une fleche orientee entre deux positions (depart -> arrivee)."""
    arrowprops = {
        "arrowstyle": style,
        "color": couleur,
        "lw": largeur,
        "shrinkA": 16,
        "shrinkB": 16,
        "connectionstyle": "arc3,rad=" + str(rad),
    }
    if tirets:
        arrowprops["linestyle"] = "dashed"
    ax.annotate("", xy=arrivee, xytext=depart, arrowprops=arrowprops)


def _ligne(ax, depart, arrivee, couleur, largeur=1.5, tirets=False, rad=0.0):
    style = "dashed" if tirets else "solid"
    ax.annotate("", xy=arrivee, xytext=depart, arrowprops={
        "arrowstyle": "-",
        "color": couleur,
        "lw": largeur,
        "linestyle": style,
        "shrinkA": 16,
        "shrinkB": 16,
        "connectionstyle": "arc3,rad=" + str(rad),
    })


# ---------------------------------------------------------------------------
# Exercice 1 : AC3
# ---------------------------------------------------------------------------

def creer_dessin_ac3(variables, aretes):
    """
    Retourne une fonction de dessin pour AC3.
    Les positions des noeuds sont calculees une seule fois (layout stable).
    """
    graphe = nx.Graph()
    graphe.add_nodes_from(variables)
    graphe.add_edges_from(aretes)
    positions = nx.spring_layout(graphe, seed=7)

    def dessiner(ax_graph, ax_info, etape, index, total, titre):
        ax_graph.set_axis_off()
        ax_info.set_axis_off()
        ax_graph.set_xlim(-1.4, 1.4)
        ax_graph.set_ylim(-1.5, 1.4)

        domaines = etape["domaines"]
        arc = etape["arc_courant"]
        supprimees = etape["valeurs_supprimees"]
        reinseres = etape["arcs_reinseres"]
        phase = etape["phase"]

        for a, b in aretes:
            _ligne(ax_graph, positions[a], positions[b], "#9bb3d4", largeur=1.5)

        if arc is not None:
            _fleche(ax_graph, positions[arc[0]], positions[arc[1]],
                    "#ff8c1a", largeur=3.5, rad=0.12)

        for arc_re in reinseres:
            _fleche(ax_graph, positions[arc_re[0]], positions[arc_re[1]],
                    "#2ca02c", largeur=3.0, rad=-0.18, tirets=True)

        for variable in variables:
            x, y = positions[variable]
            ax_graph.scatter([x], [y], s=1500, c="#4d79b3",
                             edgecolors="#23436f", linewidths=2, zorder=3)
            ax_graph.text(x, y, variable, ha="center", va="center",
                          color="white", fontsize=14, fontweight="bold", zorder=4)

            texte_dom = "{" + ", ".join(str(v) for v in domaines[variable]) + "}"
            ax_graph.text(x, y - 0.22, "D(" + variable + ") = " + texte_dom,
                          ha="center", va="center", fontsize=11,
                          bbox={"boxstyle": "round,pad=0.3", "fc": "#eef3fb",
                                "ec": "#9bb3d4"}, zorder=4)

        if phase == "suppression" and arc is not None and supprimees:
            x, y = positions[arc[0]]
            texte = "retire: " + ", ".join(str(v) for v in supprimees)
            ax_graph.text(x, y + 0.24, texte, ha="center", va="center",
                          fontsize=10, color="#c0392b", fontweight="bold",
                          zorder=5)

        ax_graph.set_title(titre + "\nEtape " + str(index + 1) + " / "
                           + str(total) + "   [phase : " + phase + "]",
                           fontsize=12, fontweight="bold")

        _panneau_ac3(ax_info, etape)

    return dessiner


def _panneau_ac3(ax_info, etape):
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)

    y = 0.97
    ax_info.text(0.0, y, "File Q (arcs a examiner)", fontsize=12,
                 fontweight="bold")
    y = y - 0.06

    arc = etape["arc_courant"]
    if arc is not None:
        ax_info.text(0.02, y, "-> en cours : (" + arc[0] + ", " + arc[1] + ")",
                     fontsize=11, color="#ff8c1a", fontweight="bold")
        y = y - 0.05

    file_arcs = etape["file"]
    reinseres = etape["arcs_reinseres"]
    if not file_arcs:
        ax_info.text(0.04, y, "(file vide)", fontsize=11, color="#555555")
        y = y - 0.05
    for a, b in file_arcs:
        est_reinsere = (a, b) in reinseres
        couleur = "#2ca02c" if est_reinsere else "#333333"
        suffixe = "  (reinsere)" if est_reinsere else ""
        ax_info.text(0.04, y, "(" + a + ", " + b + ")" + suffixe,
                     fontsize=11, color=couleur)
        y = y - 0.045

    y = min(y, 0.40)
    ax_info.text(0.0, y, "Message", fontsize=12, fontweight="bold")
    y = y - 0.05
    _texte_multiligne(ax_info, etape["message"], 0.02, y, largeur=34)

    succes = etape.get("succes")
    if succes is True:
        ax_info.text(0.0, 0.06, "CSP ARC-CONSISTANT", fontsize=13,
                     color="#2ca02c", fontweight="bold")
    elif succes is False:
        ax_info.text(0.0, 0.06, "ECHEC : domaine vide", fontsize=13,
                     color="#c0392b", fontweight="bold")


# ---------------------------------------------------------------------------
# Exercice 2 : Regin / AllDifferent
# ---------------------------------------------------------------------------

def creer_dessin_regin():
    """Retourne une fonction de dessin pour l'algorithme de Regin."""

    def dessiner(ax_graph, ax_info, etape, index, total, titre):
        ax_graph.set_axis_off()
        ax_info.set_axis_off()

        variables = etape["variables"]
        valeurs = etape["valeurs"]
        domaines = etape["domaines"]
        aretes = etape["aretes"]
        couplage = etape["couplage"]
        oriente = etape["oriente"]
        composantes = etape["composantes"]
        supprimees = etape["aretes_supprimees"]
        phase = etape["phase"]

        positions = {}
        for i, variable in enumerate(variables):
            positions[("var", variable)] = (0.0, -float(i))
        decalage = 0.0
        if len(valeurs) > 1:
            decalage = (len(variables) - 1) / float(len(valeurs) - 1)
        for j, valeur in enumerate(valeurs):
            positions[("val", valeur)] = (3.0, -float(j) * max(decalage, 0.6))

        ax_graph.set_xlim(-1.2, 4.4)
        bas = -max(len(variables), len(valeurs))
        ax_graph.set_ylim(bas - 0.8, 1.0)

        couleur_supprimee = set(supprimees)

        for variable, valeur in aretes:
            p_var = positions[("var", variable)]
            p_val = positions[("val", valeur)]
            est_couplage = couplage.get(variable) == valeur
            est_supprimee = (variable, valeur) in couleur_supprimee

            if not oriente:
                if est_couplage and phase == "couplage":
                    _ligne(ax_graph, p_var, p_val, "#2ca02c", largeur=4.0)
                elif est_supprimee:
                    _ligne(ax_graph, p_var, p_val, "#c0392b", largeur=2.0)
                else:
                    _ligne(ax_graph, p_var, p_val, "#b8b8b8", largeur=1.3)
            else:
                if est_couplage:
                    _fleche(ax_graph, p_val, p_var, "#2ca02c", largeur=3.5, rad=0.05)
                elif est_supprimee:
                    _fleche(ax_graph, p_var, p_val, "#c0392b", largeur=2.5, rad=0.05)
                else:
                    _fleche(ax_graph, p_var, p_val, "#4d79b3", largeur=1.6, rad=0.05)

            if est_supprimee:
                mx = (p_var[0] + p_val[0]) / 2.0
                my = (p_var[1] + p_val[1]) / 2.0
                ax_graph.text(mx, my, "X", ha="center", va="center",
                              color="#c0392b", fontsize=18, fontweight="bold",
                              zorder=6)

        for variable in variables:
            x, y = positions[("var", variable)]
            couleur = _couleur_noeud(("var", variable), composantes, "#4d79b3")
            ax_graph.scatter([x], [y], s=1200, c=couleur,
                             edgecolors="#23436f", linewidths=2, zorder=3)
            ax_graph.text(x, y, variable, ha="center", va="center",
                          color="white", fontsize=12, fontweight="bold", zorder=4)
            texte_dom = "{" + ", ".join(str(v) for v in domaines[variable]) + "}"
            ax_graph.text(x - 0.55, y, texte_dom, ha="right", va="center",
                          fontsize=10, color="#333333")

        for valeur in valeurs:
            x, y = positions[("val", valeur)]
            couleur = _couleur_noeud(("val", valeur), composantes, "#e08e3c")
            ax_graph.scatter([x], [y], s=1000, c=couleur,
                             edgecolors="#9c5a17", linewidths=2, zorder=3)
            ax_graph.text(x, y, str(valeur), ha="center", va="center",
                          color="white", fontsize=12, fontweight="bold", zorder=4)

        ax_graph.text(0.0, 0.6, "Variables", ha="center",
                      fontsize=11, fontweight="bold", color="#23436f")
        ax_graph.text(3.0, 0.6, "Valeurs", ha="center",
                      fontsize=11, fontweight="bold", color="#9c5a17")

        ax_graph.set_title(titre + "\nEtape " + str(index + 1) + " / "
                           + str(total) + "   [phase : " + phase + "]",
                           fontsize=12, fontweight="bold")

        _panneau_regin(ax_info, etape)

    return dessiner


def _couleur_noeud(cle, composantes, defaut):
    if composantes is None or cle not in composantes:
        return defaut
    return PALETTE_SCC[composantes[cle] % len(PALETTE_SCC)]


def _panneau_regin(ax_info, etape):
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)

    y = 0.97
    couplage = etape["couplage"]
    if couplage:
        ax_info.text(0.0, y, "Couplage M", fontsize=12, fontweight="bold")
        y = y - 0.05
        for variable in etape["variables"]:
            if variable in couplage:
                ax_info.text(0.04, y, "(" + variable + ", "
                             + str(couplage[variable]) + ")", fontsize=11,
                             color="#2ca02c")
                y = y - 0.045
        y = y - 0.02

    supprimees = etape["aretes_supprimees"]
    if supprimees:
        ax_info.text(0.0, y, "Aretes supprimees", fontsize=12,
                     fontweight="bold", color="#c0392b")
        y = y - 0.05
        for variable, valeur in supprimees:
            ax_info.text(0.04, y, "(" + variable + ", " + str(valeur) + ")",
                         fontsize=11, color="#c0392b")
            y = y - 0.045
        y = y - 0.02

    finaux = etape.get("domaines_finaux")
    if finaux is not None:
        ax_info.text(0.0, y, "Domaines filtres", fontsize=12, fontweight="bold")
        y = y - 0.05
        for variable in etape["variables"]:
            texte = "{" + ", ".join(str(v) for v in finaux[variable]) + "}"
            ax_info.text(0.04, y, "D(" + variable + ") = " + texte, fontsize=11)
            y = y - 0.045
        y = y - 0.02

    y = min(y, 0.34)
    ax_info.text(0.0, y, "Message", fontsize=12, fontweight="bold")
    y = y - 0.05
    _texte_multiligne(ax_info, etape["message"], 0.02, y, largeur=34)

    if etape.get("faisable") is False:
        ax_info.text(0.0, 0.05, "INSATISFAISABLE", fontsize=13,
                     color="#c0392b", fontweight="bold")


# ---------------------------------------------------------------------------
# Outils communs : texte, lecteur interactif, export
# ---------------------------------------------------------------------------

def _texte_multiligne(ax, texte, x, y, largeur=34, interligne=0.04):
    """Affiche un texte en le coupant en lignes de 'largeur' caracteres."""
    mots = texte.split(" ")
    ligne = ""
    lignes = []
    for mot in mots:
        if len(ligne) + len(mot) + 1 > largeur:
            lignes.append(ligne)
            ligne = mot
        else:
            ligne = (ligne + " " + mot).strip()
    if ligne:
        lignes.append(ligne)

    for ligne in lignes:
        ax.text(x, y, ligne, fontsize=10)
        y = y - interligne


def lire_etapes(etapes, dessiner, titre):
    """Ouvre une fenetre interactive avec boutons Precedent / Suivant."""
    fig = plt.figure(figsize=(14, 8))
    try:
        fig.canvas.manager.set_window_title(titre)
    except Exception:
        pass

    ax_graph = fig.add_axes([0.04, 0.16, 0.60, 0.76])
    ax_info = fig.add_axes([0.67, 0.16, 0.31, 0.76])
    ax_prec = fig.add_axes([0.30, 0.03, 0.16, 0.07])
    ax_suiv = fig.add_axes([0.54, 0.03, 0.16, 0.07])

    bouton_prec = widgets.Button(ax_prec, "<< Precedent")
    bouton_suiv = widgets.Button(ax_suiv, "Suivant >>")

    etat = {"i": 0}

    def afficher():
        ax_graph.clear()
        ax_info.clear()
        dessiner(ax_graph, ax_info, etapes[etat["i"]], etat["i"],
                 len(etapes), titre)
        fig.canvas.draw_idle()

    def precedent(_event):
        if etat["i"] > 0:
            etat["i"] = etat["i"] - 1
            afficher()

    def suivant(_event):
        if etat["i"] < len(etapes) - 1:
            etat["i"] = etat["i"] + 1
            afficher()

    bouton_prec.on_clicked(precedent)
    bouton_suiv.on_clicked(suivant)

    afficher()
    plt.show()
    return bouton_prec, bouton_suiv


def exporter_etapes(etapes, dessiner, titre, dossier, prefixe="etape"):
    """Sauvegarde chaque etape en PNG dans 'dossier'. Retourne la liste des fichiers."""
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    fichiers = []
    for index, etape in enumerate(etapes):
        fig = plt.figure(figsize=(14, 8))
        ax_graph = fig.add_axes([0.04, 0.10, 0.60, 0.82])
        ax_info = fig.add_axes([0.67, 0.10, 0.31, 0.82])
        dessiner(ax_graph, ax_info, etape, index, len(etapes), titre)

        nom = prefixe + "_" + str(index + 1).zfill(2) + ".png"
        chemin = os.path.join(dossier, nom)
        fig.savefig(chemin, dpi=110)
        plt.close(fig)
        fichiers.append(chemin)

    return fichiers
