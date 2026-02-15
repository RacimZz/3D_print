import struct
from math import isclose
from minigeo.segment import Segment
from minigeo.utils import fenetre_tournante


class Facette:
    """
    un triangle en 3d.
    """

    def __init__(self, points):
        self.points = points

    def est_horizontale(self):
        """
        renvoie si la facette est horizontale
        """
        z1, z2, z3 = (p[2] for p in self.points)
        return isclose(z1, z2) and isclose(z2, z3)

    def zmin_et_zmax(self):
        """
        renvoie les hauteurs min et max de la facette.
        """
        zmin = min(z for _, _, z in self.points)
        zmax = max(z for _, _, z in self.points)
        return zmin, zmax

    def intersection_plan_horizontal(self, hauteur):
        """
        renvoie un tuple contenant le segments obtenu en intersectant
        la facette avec un plan horizontal a la hauteur donnee.
        pre-condition: la facette n'est pas horizontale.
        """
        intersections = []
        for p1, p2 in fenetre_tournante(self.points):
            if isclose(p1[2], hauteur) and isclose(p2[2], hauteur):
                return (Segment(p1[0:2], p2[0:2]),)

            intersection = intersection_segment_plan_horizontal(p1, p2, hauteur)
            if intersection is not None:
                intersections.append(intersection)

        if len(intersections) == 2:
            return (Segment(*intersections),)

        return ()


def intersection_segment_plan_horizontal(p1, p2, hauteur):
    """
    intersecte un segment 3d non horizontal avec un plan horizontal.
    renvoie un point ou None.
    ne renvoie rien si le segment est horizontal.
    """
    if p1 > p2:
        p1, p2 = p2, p1  # on symmetrise
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    if z1 == z2:
        return None

    alpha = (hauteur - z1) / (z2 - z1)
    if not 0 < alpha < 1:  # on exclut les extremites
        return None

    ix = x1 + alpha * (x2 - x1)
    iy = y1 + alpha * (y2 - y1)

    return (ix, iy)


def facettes_stl_binaire(nom_fichier):
    """
    itere sur toutes les facettes d'un fichier stl binaire
    """
    with open(nom_fichier, "rb") as fichier_stl:
        fichier_stl.read(80)
        taille_binaire = fichier_stl.read(4)
        if not taille_binaire:
            raise IOError
        struct_taille = struct.Struct("I")
        taille = struct_taille.unpack(taille_binaire)[0]
        struct_facette = struct.Struct("12fh")
        for _ in range(taille):
            facette_binaire = fichier_stl.read(4 * 3 * 4 + 2)
            # chaque facette : 4 vecteurs de 3 flottants + 2 octets inutilises
            # le premier vecteur est la normale, qu'on jette
            coordonnees = struct_facette.unpack(facette_binaire)
            points_facette = [
                tuple(coordonnees[3 + 3 * i : 6 + 3 * i]) for i in range(3)
            ]
            yield Facette(points_facette)
