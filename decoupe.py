#!/usr/bin/env python3
from sys import argv
from minigeo.stl import facettes_stl_binaire
from minigeo.affichable import affiche
from minigeo.utils import multiples_entre

def z_min_z_max(facettes):
    z_min, z_max = facettes[0].zmin_et_zmax()
    for i in range(1,len(facettes)):
        z_min_current, z_max_current = facettes[i].zmin_et_zmax()
        if z_min_current < z_min:
            z_min = z_min_current
        
        if z_max_current > z_max:
            z_max = z_max_current
    return z_min, z_max

def decoupe(facettes, epaisseur):
    """
    renvoie un vecteur de vecteurs de segments.
    chaque vecteur interne contient tous les segments 2d d'une seule tranche.
    le vecteur externe contient toutes les coupes de tranches de la plus basse (x minimal)
    a la plus haute (x maximal).
    """
    z_min, z_max = z_min_z_max(facettes)
    tuple_multiples = multiples_entre(z_min, z_max, epaisseur)
    



def main():
    if len(argv) != 3:
        print("donnez un nom de fichier stl, une epaisseur de tranches")
        exit()
    fichier_stl = argv[1]
    epaisseur = float(argv[2])

    facettes = list(
        f for f in facettes_stl_binaire(fichier_stl) if not f.est_horizontale()
    )
    print("on a charge", len(facettes), "facettes")

    tranches = decoupe(facettes, epaisseur)

    for tranche in tranches:
        affiche(tranche)


if __name__ == "__main__":
    main()
