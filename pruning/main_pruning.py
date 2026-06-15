# TP Pruning - Point d'entree
#
# Lance les visualisations interactives pas a pas :
#   python -m pruning.main_pruning --exercice 1     (AC3)
#   python -m pruning.main_pruning --exercice 2     (Regin / AllDifferent)
#   python -m pruning.main_pruning --exercice 0     (les deux)
#
# Options utiles :
#   --export     genere les PNG de chaque etape dans pruning/exports/
#   --no-show    ne pas ouvrir la fenetre interactive (utile avec --export)

import argparse
import os

from pruning.ac3 import ac3, liste_aretes_non_orientees
from pruning.regin import filtrer_regin


DOSSIER_EXPORT = os.path.join(os.path.dirname(__file__), "exports")


# Cas de test impose - Exercice 1
VARIABLES_AC3 = ["X", "Y", "Z"]
DOMAINES_AC3 = {"X": [1, 2], "Y": [1, 2], "Z": [1, 2]}
CONTRAINTES_AC3 = [("X", "<", "Y"), ("Y", "=", "Z")]

# Cas de test impose - Exercice 2
VARIABLES_REGIN = ["x1", "x2", "x3", "x4"]
DOMAINES_REGIN = {
    "x1": [1, 2],
    "x2": [1, 2],
    "x3": [2, 3],
    "x4": [2, 3, 4, 5],
}


def _afficher_domaines(titre, variables, domaines):
    print(titre)
    for variable in variables:
        valeurs = ", ".join(str(v) for v in domaines[variable])
        print("  D(" + variable + ") = {" + valeurs + "}")


def afficher_tableau_comparatif(variables, domaines_avant, domaines_apres):
    """Livrable : tableau comparatif des domaines avant / apres filtrage."""
    print("\nTableau comparatif (avant / apres filtrage de Regin)")
    print("+----------+----------------------+----------------------+")
    print("| Variable | Domaine avant        | Domaine apres        |")
    print("+----------+----------------------+----------------------+")
    for variable in variables:
        avant = "{" + ", ".join(str(v) for v in domaines_avant[variable]) + "}"
        apres = "{" + ", ".join(str(v) for v in domaines_apres[variable]) + "}"
        print("| " + variable.ljust(8) + " | " + avant.ljust(20)
              + " | " + apres.ljust(20) + " |")
    print("+----------+----------------------+----------------------+")


def demo_ac3(montrer=True, exporter=False):
    print("=" * 64)
    print("Exercice 1 - AC3 (arc-consistance)")
    print("=" * 64)
    _afficher_domaines("Domaines initiaux :", VARIABLES_AC3, DOMAINES_AC3)
    print("Contraintes : X < Y et Y = Z")

    domaines_finaux, succes, etapes = ac3(
        VARIABLES_AC3, DOMAINES_AC3, CONTRAINTES_AC3
    )

    _afficher_domaines("\nDomaines apres AC3 :", VARIABLES_AC3, domaines_finaux)
    print("Resultat : " + ("ARC-CONSISTANT" if succes else "ECHEC (domaine vide)"))
    print("Nombre d'etapes generees : " + str(len(etapes)))

    if exporter or montrer:
        from pruning.visualisation import (
            creer_dessin_ac3, exporter_etapes, lire_etapes,
        )
        aretes = liste_aretes_non_orientees(CONTRAINTES_AC3)
        dessiner = creer_dessin_ac3(VARIABLES_AC3, aretes)
        titre = "Exercice 1 : AC3 (X < Y, Y = Z)"

        if exporter:
            fichiers = exporter_etapes(
                etapes, dessiner, titre, DOSSIER_EXPORT, prefixe="ac3"
            )
            print("Images exportees : " + str(len(fichiers)) + " fichier(s) dans "
                  + DOSSIER_EXPORT)
        if montrer:
            lire_etapes(etapes, dessiner, titre)

    return domaines_finaux


def demo_regin(montrer=True, exporter=False):
    print("\n" + "=" * 64)
    print("Exercice 2 - Regin / AllDifferent")
    print("=" * 64)
    _afficher_domaines("Domaines initiaux :", VARIABLES_REGIN, DOMAINES_REGIN)

    domaines_finaux, faisable, etapes, infos = filtrer_regin(
        VARIABLES_REGIN, DOMAINES_REGIN
    )

    if not faisable:
        print("\nLa contrainte AllDifferent est INSATISFAISABLE "
              "(pas de couplage complet).")
    else:
        print("\nCouplage maximum : M = " + str(infos["couplage"]))
        print("Aretes supprimees : " + str(infos["aretes_supprimees"]))
        afficher_tableau_comparatif(
            VARIABLES_REGIN, DOMAINES_REGIN, domaines_finaux
        )
        print("\nNote : l'algorithme SCC complet retire aussi (x4, 3) car, une "
              "fois x3 force a 3, aucun couplage maximum ne peut affecter 3 a x4. "
              "L'illustration du sujet, plus simple, ne retire que la valeur 2.")

    print("Nombre d'etapes generees : " + str(len(etapes)))

    if exporter or montrer:
        from pruning.visualisation import (
            creer_dessin_regin, exporter_etapes, lire_etapes,
        )
        dessiner = creer_dessin_regin()
        titre = "Exercice 2 : Regin AllDifferent"

        if exporter:
            fichiers = exporter_etapes(
                etapes, dessiner, titre, DOSSIER_EXPORT, prefixe="regin"
            )
            print("Images exportees : " + str(len(fichiers)) + " fichier(s) dans "
                  + DOSSIER_EXPORT)
        if montrer:
            lire_etapes(etapes, dessiner, titre)

    return domaines_finaux


def main():
    parser = argparse.ArgumentParser(
        description="TP Pruning : visualisation d'AC3 et de Regin (AllDifferent)"
    )
    parser.add_argument(
        "--exercice", type=int, choices=[0, 1, 2], default=0,
        help="1 = AC3, 2 = Regin, 0 = les deux (defaut)",
    )
    parser.add_argument(
        "--export", action="store_true",
        help="Exporter les etapes en PNG dans pruning/exports/",
    )
    parser.add_argument(
        "--no-show", action="store_true",
        help="Ne pas ouvrir la fenetre interactive",
    )
    args = parser.parse_args()

    montrer = not args.no_show

    if args.exercice in (0, 1):
        demo_ac3(montrer=montrer, exporter=args.export)
    if args.exercice in (0, 2):
        demo_regin(montrer=montrer, exporter=args.export)


if __name__ == "__main__":
    main()
