#!/usr/bin/env python3

from sys import argv
from collections import defaultdict

import minigeo.point as point
from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre
from minigeo.doublons import suppression_doublons
from minigeo.polygone import construction_polygones
from minigeo.polygone_a_trous import construction_polygones_a_trous
from minigeo.segment import Segment


def bornes_z_globales(facettes):
    z_min_global, z_max_global = facettes[0].zmin_et_zmax()
    for facette in facettes[1:]:
        z_min, z_max = facette.zmin_et_zmax()
        if z_min < z_min_global:
            z_min_global = z_min
        if z_max > z_max_global:
            z_max_global = z_max
    return z_min_global, z_max_global


def construire_tranches(facettes, hauteurs_coupe, epaisseur, indice_par_hauteur):
    tranches = [[] for _ in range(len(hauteurs_coupe))]

    for facette in facettes:
        z_min, z_max = facette.zmin_et_zmax()

        for hauteur in multiples_entre(z_min, z_max, epaisseur):
            intersection = facette.intersection_plan_horizontal(hauteur)
            if intersection == ():
                continue

            segment_2d = intersection[0]
            tranches[indice_par_hauteur[hauteur]].append(segment_2d)

    return tranches


def decoupe(facettes, epaisseur):
    z_min_global, z_max_global = bornes_z_globales(facettes)

    hauteurs_coupe = list(multiples_entre(z_min_global, z_max_global, epaisseur))
    indice_par_hauteur = {hauteurs_coupe[i]: i for i in range(len(hauteurs_coupe))}

    return construire_tranches(facettes, hauteurs_coupe, epaisseur, indice_par_hauteur)


def construire_graphe(segments):
    graphe = defaultdict(list)

    for segment in segments:
        graphe[segment.debut].append(segment)
        graphe[segment.fin].append(segment)

    return graphe


def autre_extremite(segment, sommet):
    if segment.debut == sommet:
        return segment.fin
    if segment.fin == sommet:
        return segment.debut
    raise Exception("sommet non incident au segment")


def degre(sommet, graphe):
    return len(graphe[sommet])


def composantes_connexes(graphe):
    deja_vus = set()
    composantes = []

    for sommet_depart in graphe:
        if sommet_depart in deja_vus:
            continue

        composante = set()
        a_voir = [sommet_depart]

        while a_voir:
            sommet = a_voir.pop()

            if sommet in deja_vus:
                continue

            deja_vus.add(sommet)
            composante.add(sommet)

            for segment in graphe[sommet]:
                voisin = autre_extremite(segment, sommet)
                if voisin not in deja_vus:
                    a_voir.append(voisin)

        composantes.append(composante)

    return composantes


def sommets_impairs(graphe):
    return [sommet for sommet in graphe if degre(sommet, graphe) % 2 == 1]


def cle_liaison(p1, p2):
    d = point.distance(p1, p2)
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return (round(d, 10), round(dx, 10), round(dy, 10))


def meilleur_couple_entre_ensembles(ensemble1, ensemble2):
    meilleur_p1 = None
    meilleur_p2 = None
    meilleure_cle = None

    for p1 in ensemble1:
        for p2 in ensemble2:
            cle = cle_liaison(p1, p2)
            if meilleure_cle is None or cle < meilleure_cle:
                meilleure_cle = cle
                meilleur_p1 = p1
                meilleur_p2 = p2

    return meilleur_p1, meilleur_p2, meilleure_cle


def rendre_connexe(segments):
    segments = list(segments)
    graphe = construire_graphe(segments)
    composantes = composantes_connexes(graphe)

    while len(composantes) > 1:
        meilleur_p1 = None
        meilleur_p2 = None
        meilleure_cle = None
        idx1, idx2 = -1, -1

        for i in range(len(composantes)):
            for j in range(i + 1, len(composantes)):
                p1, p2, cle = meilleur_couple_entre_ensembles(
                    composantes[i], composantes[j]
                )
                if meilleure_cle is None or cle < meilleure_cle:
                    meilleure_cle = cle
                    meilleur_p1 = p1
                    meilleur_p2 = p2
                    idx1 = i
                    idx2 = j

        segments.append(Segment(meilleur_p1, meilleur_p2))
        
        nouvelle_composante = composantes[idx1].union(composantes[idx2])
        composantes.pop(max(idx1, idx2))
        composantes.pop(min(idx1, idx2))
        composantes.append(nouvelle_composante)

    return segments


def rendre_degres_pairs(segments):
    segments = list(segments)
    graphe = construire_graphe(segments)
    impairs = sommets_impairs(graphe)

    while impairs:
        meilleur_s1 = None
        meilleur_s2 = None
        meilleure_cle = None
        idx1, idx2 = -1, -1

        for i in range(len(impairs)):
            for j in range(i + 1, len(impairs)):
                s1 = impairs[i]
                s2 = impairs[j]
                cle = cle_liaison(s1, s2)
                if meilleure_cle is None or cle < meilleure_cle:
                    meilleure_cle = cle
                    meilleur_s1 = s1
                    meilleur_s2 = s2
                    idx1 = i
                    idx2 = j

        segments.append(Segment(meilleur_s1, meilleur_s2))
        
        impairs.pop(max(idx1, idx2))
        impairs.pop(min(idx1, idx2))

    return segments


def cycle_eulerien(segments):
    if not segments:
        return []

    graphe = construire_graphe(segments)

    depart = next(iter(graphe))
    pile_sommets = [depart]
    pile_segments = []
    cycle = []

    while pile_sommets:
        sommet = pile_sommets[-1]

        if graphe[sommet]:
            segment = graphe[sommet].pop()
            voisin = autre_extremite(segment, sommet)
            graphe[voisin].remove(segment)

            pile_sommets.append(voisin)
            pile_segments.append(Segment(sommet, voisin))
        else:
            pile_sommets.pop()
            if pile_segments:
                cycle.append(pile_segments.pop())

    cycle.reverse()
    return cycle


def animer_cycle(cycle, fond_segments):
    """
    Affiche le parcours d'impression.
    On colore les segments du cycle en vert pour les distinguer de la forme.
    """
    for segment in cycle:
        # On assigne les deux attributs habituels pour s'assurer que minigeo le prenne en compte
        segment.color = "green"
        segment.couleur = "green"

    for i in range(1, len(cycle) + 1):
        affiche(fond_segments + cycle[:i])


def traitement_tranche(segments, buse):
    segments_dedoublonnes = suppression_doublons(segments)
    affiche(segments_dedoublonnes)

    polygones = construction_polygones(segments_dedoublonnes)
    print(f"on a {len(polygones)} polygones")
    affiche(polygones)

    polygones_a_trous = construction_polygones_a_trous(polygones)
    print(f"on a {len(polygones_a_trous)} polygones a trous")
    affiche(polygones_a_trous)

    segments_remplissage = []
    for poly in polygones_a_trous:
        segments_remplissage.extend(poly.decoupe(buse))

    print(f"on a {len(segments_remplissage)} segments de remplissage")
    affiche(segments_remplissage)

    graphe_initial = construire_graphe(segments_remplissage)
    print("composantes initiales :", len(composantes_connexes(graphe_initial)))
    print("sommets impairs initiaux :", len(sommets_impairs(graphe_initial)))

    segments_completes = rendre_connexe(segments_remplissage)
    segments_completes = rendre_degres_pairs(segments_completes)

    print(f"on a {len(segments_completes)} segments apres completion")
    affiche(segments_completes)

    graphe_final = construire_graphe(segments_completes)
    print("composantes finales :", len(composantes_connexes(graphe_final)))
    print("sommets impairs finaux :", len(sommets_impairs(graphe_final)))

    cycle = cycle_eulerien(segments_completes)
    print(f"longueur du cycle : {len(cycle)}")

    # On dessine les bordures et les trous en fond pour l'animation !
    animer_cycle(cycle, segments_dedoublonnes)


def main():
    if len(argv) != 5:
        print(
            "donnez un nom de fichier stl, une epaisseur de tranches, un diametre de buse, un numero de tranche a traiter"
        )
        exit()

    fichier_stl = argv[1]
    epaisseur = float(argv[2])
    buse = float(argv[3])
    tranche_cible = int(argv[4])

    facettes = list(
        f for f in facettes_stl_binaire(fichier_stl) if not f.est_horizontale()
    )
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)
    traitement_tranche(tranches[tranche_cible], buse)


if __name__ == "__main__":
    main()