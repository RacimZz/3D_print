from minigeo.segment import Segment
from minigeo.affichable import affiche
from collections import defaultdict
from math import isclose


def clef_ligne(segment):
    """
    renvoie un identifiant de la ligne sur laquelle se trouve le segment
    """
    x1, y1 = segment.debut
    x2, y2 = segment.fin
    if isclose(x1, x2):
        return format(x1, ".2f")
    pente = (y2 - y1) / (x2 - x1)
    ordonne_a_origine = y2 - pente * x2
    return format(pente, ".2f"), format(ordonne_a_origine, ".2f")


def suppression_doublons(segments):
    """
    toutes les parties superposees par un nombre pair de segments disparaissent
    """
    # on commence par repartir les segments entre leurs lignes supports
    lignes = defaultdict(list)
    for s in segments:
        lignes[clef_ligne(s)].append(s)

    # on peut maintenant calculer independamment ce qui reste dans chaque ligne
    reste = []
    for segments_ligne in lignes.values():
        diff_comptes = defaultdict(int)
        for segment in segments_ligne:
            debut = min(segment.points())
            fin = max(segment.points())
            diff_comptes[debut] += 1
            diff_comptes[fin] -= 1

        compte_courant = 0
        point_prec = None
        for point in sorted(diff_comptes.keys()):
            nouveau_compte = compte_courant + diff_comptes[point]
            if nouveau_compte % 2 != 1 and compte_courant % 2 == 1:
                # fin d'un segment a garder
                segment_garde = Segment(point_prec, point)
                reste.append(segment_garde)
            if nouveau_compte % 2 == 1 and compte_courant % 2 != 1:
                # debut d'un segment a garder
                point_prec = point
            compte_courant = nouveau_compte
    return reste
