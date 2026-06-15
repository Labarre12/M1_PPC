# Lot 3 : Filtre de Bloom
#
# Un filtre de Bloom est une structure de donnees probabiliste qui repond
# a la question : "est-ce que cet element a deja ete vu ?".
#
# - Il utilise un tableau de m bits, tous a 0 au depart.
# - Pour ajouter un element, on calcule k positions (avec k fonctions de
#   hachage) et on met ces bits a 1.
# - Pour tester un element, on regarde si TOUS ses k bits sont a 1.
#
# Particularite :
# - si le test dit "absent", l'element est vraiment absent (jamais d'erreur),
# - si le test dit "present", l'element est PROBABLEMENT present : il peut y
#   avoir des faux positifs (mais jamais de faux negatifs).
#
# Avantage : tres econome en memoire (un bit par case, pas la donnee entiere).

import hashlib
import math


class FiltreBloom:
    """Filtre de Bloom simple base sur hashlib."""

    def __init__(self, taille_bits, nb_hachages):
        self.taille_bits = taille_bits
        self.nb_hachages = nb_hachages
        # bytearray : un octet par case (0 ou 1). Simple a comprendre.
        self.bits = bytearray(taille_bits)
        self.nb_elements = 0

    def _positions(self, element):
        """
        Calcule les k positions (bits) associees a un element.
        On utilise md5 avec un sel different pour chaque fonction de hachage.
        """
        positions = []
        for numero in range(self.nb_hachages):
            texte = str(numero) + "_" + str(element)
            empreinte = hashlib.md5(texte.encode("utf-8")).hexdigest()
            valeur = int(empreinte, 16)
            position = valeur % self.taille_bits
            positions.append(position)
        return positions

    def ajouter(self, element):
        """Insere un element dans le filtre."""
        for position in self._positions(element):
            self.bits[position] = 1
        self.nb_elements = self.nb_elements + 1

    def contient(self, element):
        """
        Teste l'appartenance.
        Retourne False si l'element est surement absent,
        True s'il est probablement present (faux positif possible).
        """
        for position in self._positions(element):
            if self.bits[position] == 0:
                return False
        return True

    def taux_remplissage(self):
        """Proportion de bits a 1 (utile pour estimer la saturation)."""
        bits_a_un = 0
        for bit in self.bits:
            if bit == 1:
                bits_a_un = bits_a_un + 1
        return bits_a_un / self.taille_bits


def taille_optimale(nb_elements, proba_faux_positif):
    """
    Calcule les bons parametres d'un filtre de Bloom.
    Retourne (m, k) :
      m = nombre de bits conseille
      k = nombre de fonctions de hachage conseille

    Formules classiques :
      m = - n * ln(p) / (ln 2)^2
      k = (m / n) * ln 2
    """
    if nb_elements <= 0:
        return 1, 1

    m = -(nb_elements * math.log(proba_faux_positif)) / (math.log(2) ** 2)
    m = int(math.ceil(m))

    k = (m / nb_elements) * math.log(2)
    k = int(round(k))
    if k < 1:
        k = 1

    return m, k


def proba_faux_positif_theorique(m, k, n):
    """
    Estime le taux de faux positifs theorique d'un filtre.
    Formule : (1 - e^(-k n / m))^k
    """
    if m == 0:
        return 1.0
    interne = 1 - math.exp(-k * n / m)
    return interne ** k
