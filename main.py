# Programme principal : démonstrations de tous les exercices

import argparse

from exercice1.enum_backtrack import (
    enumerer_mots_backtrack_construction,
    enumerer_mots_backtrack_edition,
)
from exercice1.enum_bfs import enumerer_mots_bfs, enumerer_mots_par_distance
from exercice1.enum_cp import enumerer_mots_cp
from exercice1.levenshtein import distance_levenshtein
from exercice2.partitions import afficher_partition, partitions
from exercice2.partitions_backtrack import partitions_backtrack
from exercice3.monnaie import (
    afficher_solution_monnaie,
    rendre_monnaie_backtrack,
    rendre_monnaie_exhaustif,
)
from exercice4.mastermind import (
    afficher_historique_mastermind,
    jouer_mastermind_interactif,
    resoudre_mastermind_backtrack,
    resoudre_mastermind_exhaustif,
)


def demo_exercice1(mot_reference="vato", k=2, ignorer_cp=False):
    print("=" * 60)
    print("Exercice 1 - Mots a distance <= " + str(k) + " de '" + mot_reference + "'")
    print("=" * 60)

    print("\nExemples de distance de Levenshtein :")
    print("  chat / chats -> " + str(distance_levenshtein("chat", "chats")))
    print("  chat / chien -> " + str(distance_levenshtein("chat", "chien")))

    mots_bfs = enumerer_mots_bfs(mot_reference, k)
    mots_back_edition = enumerer_mots_backtrack_edition(mot_reference, k)
    mots_back_construction = enumerer_mots_backtrack_construction(mot_reference, k)

    print("\nNombre de mots trouves :")
    print("  BFS                         : " + str(len(mots_bfs)))
    print("  Backtracking (edition)      : " + str(len(mots_back_edition)))
    print("  Backtracking (construction) : " + str(len(mots_back_construction)))

    if not ignorer_cp:
        mots_cp = enumerer_mots_cp(mot_reference, k)
        print("  CP (contraintes)            : " + str(len(mots_cp)))
        print("  CP identique a BFS ?        : " + str(set(mots_cp) == set(mots_bfs)))

    print("  Backtrack edition = BFS ?   : " + str(set(mots_back_edition) == set(mots_bfs)))
    print("  Backtrack construction = BFS ? : " + str(set(mots_back_construction) == set(mots_bfs)))

    par_distance = enumerer_mots_par_distance(mot_reference, k)
    print("\nRepartition par distance exacte :")
    for distance in sorted(par_distance.keys()):
        print("  distance " + str(distance) + " : " + str(len(par_distance[distance])) + " mot(s)")

    print("\nListe complete (BFS, triee) :")
    print(", ".join(mots_bfs))


def demo_exercice2(n=4):
    print("\n" + "=" * 60)
    print("Exercice 2 - Partitions de " + str(n))
    print("=" * 60)

    parts_recursive = partitions(n)
    parts_backtrack = partitions_backtrack(n)

    print("\nNombre de partitions :")
    print("  Recursif     : " + str(len(parts_recursive)))
    print("  Backtracking : " + str(len(parts_backtrack)))
    print("  Meme resultat ? : " + str(parts_recursive == parts_backtrack))

    print("\nPartitions (backtracking) :")
    for partition in parts_backtrack:
        print("  " + afficher_partition(partition))


def demo_exercice3(valeurs=None, montant=None):
    print("\n" + "=" * 60)
    print("Exercice 3 - Rendu de monnaie")
    print("=" * 60)

    if valeurs is None or montant is None:
        exemples = [
            ([1, 2, 5], 13),
            ([1, 3, 4], 6),
        ]
    else:
        exemples = [(valeurs, montant)]

    for valeurs_courantes, montant_courant in exemples:
        print("\nPieces V = " + str(valeurs_courantes) + ", montant N = " + str(montant_courant))

        solution_bt = rendre_monnaie_backtrack(valeurs_courantes, montant_courant)
        solution_ex = rendre_monnaie_exhaustif(valeurs_courantes, montant_courant)

        print("\n  Methode backtracking :")
        afficher_solution_monnaie(valeurs_courantes, solution_bt)

        print("\n  Methode exhaustive :")
        afficher_solution_monnaie(valeurs_courantes, solution_ex)

        print(
            "  Meme resultat ? "
            + str(solution_bt["repartition"] == solution_ex["repartition"])
        )


def demo_exercice4():
    print("\n" + "=" * 60)
    print("Exercice 4 - Mastermind simplifie")
    print("=" * 60)

    # Petites tailles pour commencer (comme demande dans l'enonce)
    couleurs = ["R", "V", "B"]
    secret = ["R", "V", "B"]

    print("\nCouleurs : " + str(couleurs))
    print("Secret   : " + str(secret))

    resultat_ex = resoudre_mastermind_exhaustif(secret, couleurs)
    print("\nMethode exhaustive :")
    afficher_historique_mastermind(resultat_ex["historique"])
    print("Trouve ? " + str(resultat_ex["trouve"]))
    print("Tentatives : " + str(resultat_ex["tentatives"]))

    secret2 = ["B", "B", "R"]
    print("\nAutre secret : " + str(secret2))

    resultat_bt = resoudre_mastermind_backtrack(secret2, couleurs)
    print("\nMethode backtracking :")
    afficher_historique_mastermind(resultat_bt["historique"])
    print("Trouve ? " + str(resultat_bt["trouve"]))
    print("Tentatives : " + str(resultat_bt["tentatives"]))


def main():
    parser = argparse.ArgumentParser(description="Exercices de programmation par contrainte")
    parser.add_argument("--m", default="vato", help="Mot de reference (exercice 1)")
    parser.add_argument("--k", type=int, default=2, help="Distance maximale (exercice 1)")
    parser.add_argument("--n", type=int, default=4, help="Entier a partitionner (exercice 2)")
    parser.add_argument(
        "--skip-cp",
        action="store_true",
        help="Ne pas lancer la methode CP (exercice 1, plus lente)",
    )
    parser.add_argument(
        "--exercice",
        type=int,
        choices=[1, 2, 3, 4, 0],
        default=0,
        help="Lancer un seul exercice (0 = tous)",
    )
    parser.add_argument(
        "--monnaie-v",
        default="1,2,5",
        help="Valeurs de pieces separees par des virgules (exercice 3)",
    )
    parser.add_argument(
        "--monnaie-n",
        type=int,
        default=13,
        help="Montant a rendre (exercice 3)",
    )
    parser.add_argument(
        "--mastermind-interactif",
        action="store_true",
        help="Lancer Mastermind en mode interactif (exercice 4)",
    )
    parser.add_argument(
        "--mastermind-couleurs",
        default="R,V,B",
        help="Couleurs Mastermind separees par des virgules",
    )
    parser.add_argument(
        "--mastermind-longueur",
        type=int,
        default=3,
        help="Longueur du code secret Mastermind",
    )
    args = parser.parse_args()

    if args.mastermind_interactif:
        couleurs = args.mastermind_couleurs.split(",")
        jouer_mastermind_interactif(couleurs, args.mastermind_longueur)
        return

    if args.exercice in (0, 1):
        demo_exercice1(args.m, args.k, ignorer_cp=args.skip_cp)
    if args.exercice in (0, 2):
        demo_exercice2(args.n)
    if args.exercice in (0, 3):
        if args.exercice == 0:
            demo_exercice3()
        else:
            valeurs = []
            for partie in args.monnaie_v.split(","):
                valeurs.append(int(partie.strip()))
            demo_exercice3(valeurs, args.monnaie_n)
    if args.exercice in (0, 4):
        demo_exercice4()


if __name__ == "__main__":
    main()
