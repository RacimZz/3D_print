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

def construire_segment_tranches(facettes, tuple_multiples,epaisseur, index_par_hauteur) :
    """
    Renvoie un vecteur qui contient des vecteurs de segment 
    pour chaque hauteur parmis les multiples de l'epaisseur
    """
    tranches = [[] for _ in range(len(tuple_multiples))]
    for idx_facette in range(len(facettes)):
        z_min, z_max = facettes[idx_facette].zmin_et_zmax()
        for hauteur in multiples_entre(z_min, z_max, epaisseur) :
            tup = facettes[idx_facette].intersection_plan_horizontal(hauteur)
            if tup == ():
                continue
            tranches[index_par_hauteur[hauteur]].append(tup[0])
    return tranches

def decoupe(facettes, epaisseur):
    """
    renvoie un vecteur de vecteurs de segments.
    chaque vecteur interne contient tous les segments 2d d'une seule tranche.
    le vecteur externe contient toutes les coupes de tranches de la plus basse (x minimal)
    a la plus haute (x maximal).
    """
    z_min, z_max = z_min_z_max(facettes)
    tuple_multiples = list(multiples_entre(z_min, z_max, epaisseur))
    index_par_hauteur = {tuple_multiples[i]:i for i in range(len(tuple_multiples))}
    return construire_segment_tranches(facettes,tuple_multiples,epaisseur, index_par_hauteur)

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
