import minigeo.point
from minigeo.affichable import affiche
from minigeo.segment import Segment
from minigeo.segment import produit_croix
from minigeo.utils import fenetre_tournante
from collections import defaultdict
from itertools import chain, pairwise
from functools import reduce
from math import isclose


class Polygone:
    def __init__(self, points):
        self.points = points
        assert len(self.points) >= 3

    @classmethod
    def carre(cls, centre, cote):
        x, y = centre
        p1 = (x - cote, y - cote)
        p2 = (x - cote, y + cote)
        p3 = (x + cote, y + cote)
        p4 = (x + cote, y - cote)
        return cls([p1, p2, p3, p4])

    def surface(self):
        return (
            sum(produit_croix(p1, p2) for p1, p2 in fenetre_tournante(self.points)) / 2
        )

    def mise_a_jour_dimensions(self, dimensions):
        return reduce(minigeo.point.mise_a_jour_dimensions, self.points, dimensions)

    def code_svg(self):
        svg_points = " ".join(f"{x},{y}" for x, y in self.points)
        return f"<polygon points='{svg_points}' stroke='none' opacity='0.8'/>"

    def contient(self, autre):
        """
        est-ce que l'autre polygone est dans moi ?
        note : si l'autre n'est PAS dans moi, je ne suis PAS FORCEMENT dans l'autre.
        pre-condition: pas d'intersections sauf sur les bords
        """
        # on calcule la range des x de l'autre
        xmin_autre = min(p[0] for p in autre.points)
        xmax_autre = max(p[0] for p in autre.points)
        # on va prendre le plus gros intervalle entre 2 coordonnees x
        # qui soit dans la range de l'autre
        coordonnees_x = (p[0] for p in chain(self.points, autre.points))
        coordonnees_x_dans_autre = sorted(
            filter(lambda x: xmin_autre <= x <= xmax_autre, coordonnees_x)
        )
        x1, x2 = max(pairwise(coordonnees_x_dans_autre), key=lambda t: t[1] - t[0])
        # on prend le milieu de l'intervalle pour essayer d'eviter les problemes d'arrondis
        x_interne = (x1 + x2) / 2
        # on regarde tous les points de l'autre sur ce x
        autres_y = filter(
            None,
            (s.intersection_droite_verticale(x_interne) for s in autre.segments()),
        )
        # ils doivent tous etre dans self
        return all(self.contient_point((x_interne, y)) for y in autres_y)

    def contient_point(self, point_a_tester):
        """
        renvoie si nous contenons le point donne.
        """
        # d'abord si on est sur un bord, c'est bon.
        if any(s.contient(point_a_tester) for s in self.segments()):
            return True

        x, y = point_a_tester

        # on va faire l'algo classique de lancer de rayons.
        # on compte le nombre de frontieres que l'on traverse en partant du point et en avancant
        # tout droit. si pair, on est dehors, si impair dedans.
        # il y a une subtilite si le rayon passe exactement sur un point i du polygone.
        # dans ce cas la deux cas : soit les 2 segments de i
        # sont du meme cote et ca ne compte pas
        #
        #       .
        #      /|
        #     i | poly
        #      \|
        #       .              ici p n'est pas dans le poly
        #                  meme si le rayon vertical partant de p touche i
        #     p
        #
        # soit ils passent d'un cote a l'autre et c'est bien une frontiere
        compte_frontieres = 0
        segments_non_verticaux = (s for s in self.segments() if s.debut[0] != s.fin[0])
        for s1, s2 in fenetre_tournante(segments_non_verticaux):
            i = s1.fin
            if isclose(minigeo.point.distance(i, point_a_tester), 0):
                if s1.debut[0] < x != s2.fin[0] < x:
                    compte_frontieres += 1  # pas du meme cote
            else:
                intersection = s1.intersection_droite_verticale(x)
                if intersection is not None and intersection > y:
                    compte_frontieres += 1

        return compte_frontieres % 2 == 1

    def segments(self):
        return (Segment(*points) for points in fenetre_tournante(self.points))

    def __repr__(self):
        coords_points = " ".join(f"{x},{y}" for x, y in self.points)
        return f"P[{coords_points}]"

    def normalisation(self):
        """
        on oriente le polygone et on commence par le point min.
        """
        if self.surface() < 0:
            self.points.reverse()
        indice_point_min = min(enumerate(self.points), key=lambda t: t[1])[0]
        points_reordonnes = (
            self.points[indice_point_min:] + self.points[:indice_point_min]
        )
        self.points = points_reordonnes


def construction_voisins(segments):
    voisins = defaultdict(list)

    for s in segments:
        voisins[s.debut].append(s.fin)

    for point, voisins_du_point in voisins.items():
        voisins_du_point.sort(key=lambda p: minigeo.point.angle(point, p))

    return voisins


def construction_polygone(voisins, segments_restants, premier_segment):
    depart = premier_segment.debut
    segments_restants.remove(premier_segment)
    segment_courant = premier_segment
    points = [depart]
    while True:
        segment_suivant = trouve_suite(voisins, segment_courant)
        if segment_suivant == premier_segment:
            if len(points) > 2:
                nouveau_polygone = Polygone(points)
                if isclose(nouveau_polygone.surface(), 0.0):
                    raise Exception("polygone vide")
                else:
                    return nouveau_polygone
            else:
                return None
        segment_courant = segment_suivant
        segments_restants.remove(segment_courant)
        points.append(segment_courant.debut)


def trouve_suite(voisins, segment):
    voisins_courant = voisins[segment.fin]
    for p1, p2 in fenetre_tournante(voisins_courant):
        if p1 == segment.debut:
            return Segment(segment.fin, p2)
    raise Exception("pas de voisin")


def construction_polygones(segments):
    segments_tous_sens = list(chain(segments, (s.renverse() for s in segments)))
    voisins = construction_voisins(segments_tous_sens)
    segments_restants = set(segments_tous_sens)
    polygones = []
    while segments_restants:
        premier_segment = next(iter(segments_restants))
        nouveau_polygone = construction_polygone(
            voisins, segments_restants, premier_segment
        )
        polygones.append(nouveau_polygone)
    # on elimine tous ceux qui ont une aire negative
    polygones = [p for p in polygones if p.surface() > 0.0]
    return polygones


def main():
    p1 = (0, 0)
    p2 = (1, 0)
    p3 = (2, 0)
    p4 = (1, 1)
    p5 = (2, 1)
    segments = [
        Segment(p1, p2),
        Segment(p2, p4),
        Segment(p4, p1),  # petit triangle
        Segment(p2, p3),
        Segment(p3, p4),  # second triangle
        Segment(p4, p5),
        Segment(p5, p3),  # 3eme triangle
    ]
    polys = construction_polygones(segments)
    print(polys)
    affiche(polys, p1, p2, p3, p4, p5)


if __name__ == "__main__":
    main()
