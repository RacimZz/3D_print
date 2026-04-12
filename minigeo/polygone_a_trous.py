from collections import defaultdict
from itertools import chain, batched
from minigeo.classification import arbre_inclusion
from minigeo.segment import Segment
from minigeo.affichable import affiche


class PolygoneATrou:
    def __init__(self, polygone_externe, trous):
        self.polygone_externe = polygone_externe
        self.trous = list(trous)

    def mise_a_jour_dimensions(self, dimensions):
        return self.polygone_externe.mise_a_jour_dimensions(dimensions)

    def code_svg(self):
        return "".join(
            p.code_svg() for p in chain((self.polygone_externe,), self.trous)
        )

    def decoupe(self, ecartement):
        lignes = defaultdict(list)
        self.polygone_externe.detection_points_decoupes(lignes, ecartement)
        for trou in self.trous:
            trou.detection_points_decoupes(lignes, ecartement)

        a_remplir = []
        for x, points_ligne in lignes.items():
            if len(points_ligne) % 2 == 1:
                raise Exception("ligne invalide")
            points_ligne.sort()
            a_remplir.extend(Segment(*c) for c in batched(points_ligne, 2))
        return a_remplir


def noeuds_et_profondeurs(racine):
    a_voir = [(racine, 0)]
    while a_voir:
        courant, profondeur_courante = a_voir.pop()
        yield courant, profondeur_courante
        a_voir.extend((e, profondeur_courante + 1) for e in courant.enfants)


def construction_polygones_a_trous(polygones):
    racine = arbre_inclusion(polygones)
    polygones_a_trous = []
    # tous les noeuds a profondeur impaire contiennent une enveloppe externe
    # et ceux a profondeur pair contiennent un trou
    noeuds_profondeurs = noeuds_et_profondeurs(racine)
    noeuds_impairs = (n for n, p in noeuds_profondeurs if p % 2 == 1)
    polygones_a_trous = (
        PolygoneATrou(n.contenu, (e.contenu for e in n.enfants)) for n in noeuds_impairs
    )
    return list(polygones_a_trous)
