#!/usr/bin/env python3
from sys import argv

from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre


def bornes_z_globales(facettes):
    """
    Calcule les bornes globales (z_min, z_max) parmi toutes les facettes.

    Paramètre:
    - facettes: list [Facette]

    Retour:
    - (z_min_global, z_max_global): tuple (float, float)

    Complexité:
    - Temps: O(N) où N = nombre de facettes.
    """
    z_min_global, z_max_global = facettes[0].zmin_et_zmax()
    for facette in facettes[1:]:
        z_min, z_max = facette.zmin_et_zmax()
        if z_min < z_min_global:
            z_min_global = z_min
        if z_max > z_max_global:
            z_max_global = z_max
    return z_min_global, z_max_global


def construire_tranches(facettes, hauteurs_coupe, epaisseur, indice_par_hauteur):
    """
    Construit toutes les tranches (segments 2D) pour des plans z = hauteur.

    Paramètres:
    - facettes: list [Facette]
    - hauteurs_coupe: list [float], toutes les hauteurs z à traiter (triées).
    - epaisseur: float, pas en z (distance entre deux tranches).
    - indice_par_hauteur: dict[float, int], map hauteur -> index dans hauteurs_coupe.

    Retour:
    - tranches: list[list[Segment]], tranches[i] = segments 2D à z = hauteurs_coupe[i].

    Complexité:
    - Temps: O(N*H) au pire, où N = nb facettes et H = nb tranches,
      car une facette peut être testée contre beaucoup de hauteurs. 
    """
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
    """
    Découpe un ensemble de facettes 3D en tranches horizontales z = k*epaisseur.

    Paramètres:
    - facettes: list[Facette]
    - epaisseur: float

    Retour:
    - list[list[Segment]]: une liste de tranches (de la plus basse à la plus haute).

    Complexité (directe):
    - Temps: O(N*H) au pire, avec
      N = nb facettes, H ≈ (z_max_global - z_min_global)/epaisseur.  
    """
    z_min_global, z_max_global = bornes_z_globales(facettes)

    hauteurs_coupe = list(multiples_entre(z_min_global, z_max_global, epaisseur))
    indice_par_hauteur = {hauteurs_coupe[i]: i for i in range(len(hauteurs_coupe))}

    return construire_tranches(facettes, hauteurs_coupe, epaisseur, indice_par_hauteur)


def main():
    """
    Charge un STL binaire, filtre les facettes horizontales, découpe puis affiche chaque tranche.

    Complexité:
    - Temps: découpe domine (≈ O(N*H) au pire)
    """
    if len(argv) != 3:
        print("donnez un nom de fichier stl, une epaisseur de tranches")
        exit()

    chemin_stl = argv[1]
    epaisseur = float(argv[2])

    facettes = [f for f in facettes_stl_binaire(chemin_stl) if not f.est_horizontale()]
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)

    for tranche in tranches:
        affiche(tranche)


if __name__ == "__main__":
    main()
