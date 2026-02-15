import minigeo.point as point
from itertools import pairwise
from math import isclose, pi, cos, sin
from random import random


class Segment:
    """
    un segment (oriente) dans le plan
    """

    def __init__(self, debut, fin):
        self.debut = debut
        self.fin = fin

    @classmethod
    def aleatoire(cls):
        return cls(point.point_aleatoire(), point.point_aleatoire())

    @classmethod
    def aleatoire_avec_taille(cls, taille):
        debut = point.point_aleatoire()
        x, y = debut
        angle = random() * pi * 2.0
        fin = (x + cos(angle) * taille, y + sin(angle) * taille)
        return cls(debut, fin)

    def intersection_droite_verticale(self, x):
        """
        renvoie la coordonnee y de l'intersection d'une droite
        verticale d'ordonnee x avec nous.
        None si nous sommes vertical ou s'il n'y a pas d'intersections
        """
        x1, y1 = self.debut
        x2, y2 = self.fin
        if x < min(x1, x2):
            return None
        if x > max(x1, x2):
            return None
        if isclose(x1, x2):
            return None
        if isclose(x, x1):
            return y1
        if isclose(x, x2):
            return y2

        pente = (y2 - y1) / (x2 - x1)
        y = y1 + pente * (x - x1)
        return y

    def points(self):
        yield self.debut
        yield self.fin

    def renverse(self):
        return Segment(self.fin, self.debut)

    def __eq__(self, autre):
        return self.debut == autre.debut and self.fin == autre.fin

    def __hash__(self):
        return hash((self.debut, self.fin))

    def __repr__(self):
        return f"[{self.debut} -> {self.fin}]"

    def __lt__(self, autre):
        return tuple(self.points()) < tuple(autre.points())

    def mise_a_jour_dimensions(self, dimensions):
        return point.mise_a_jour_dimensions(
            point.mise_a_jour_dimensions(dimensions, self.fin), self.debut
        )

    def autre_point_que(self, point):
        """
        renvoie le point qui n'est pas celui donne.
        attention, on utilise l'id et pas les coordonnees.
        """
        if self.debut is point:
            return self.fin
        elif self.fin is point:
            return self.debut
        raise Exception("point inconnu")

    def code_svg(self):
        x1, y1 = self.debut
        x2, y2 = self.fin
        return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}'/>"

    def rotation(self, angle):
        return Segment(*(point.rotation(p, angle) for p in self.points()))

    def intersection_avec_segment(self, autre):
        """
        intersecte deux segments.
        ne renvoie le point que s'il est inclu sur les deux segments
        """
        if self < autre:  # pour eviter les problemes de commutativite
            self, autre = autre, self

        i = self.intersection_avec_ligne(autre)
        if i is None:
            return None  # lignes //

        if self.contient(i) and autre.contient(i):
            return i
        else:
            return None

    def longueur(self):
        return point.distance(self.debut, self.fin)

    def contient(self, p):
        """
        est-ce que le point p est a l'interieur de nous ?
        """
        somme_distances = sum(point.distance(p, q) for q in self.points())
        return isclose(somme_distances, self.longueur())

    def intersection_avec_ligne(self, autre):
        """
        renvoie le point d'intersection des deux lignes passant par les deux segments
        ou aucun si les deux lignes sont quasi-paralleles
        """
        # on resout :
        # intersection = debut de self + alpha * direction de self
        # intersection = debut de autre + beta * direction de autre
        dir_self, dir_autre = (point.moins(s.fin, s.debut) for s in (self, autre))
        denominateur = produit_croix(dir_self, dir_autre)
        if isclose(denominateur, 0.0):
            # lignes //
            return None
        diff_debuts = point.moins(autre.debut, self.debut)
        alpha = produit_croix(diff_debuts, dir_autre) / denominateur
        return point.plus(self.debut, point.fois(dir_self, alpha))


def produit_croix(v, w):
    a, b = v
    c, d = w
    return -b * c + a * d
