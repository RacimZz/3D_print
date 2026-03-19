from minigeo.polygone import Polygone
from minigeo.affichable import affiche


class Noeud:
    def __init__(self, contenu):
        self.contenu = contenu
        self.enfants = []

    def affichage(self):
        """
        creation d'un fichier dot, conversion en png et affichage dans kitty
        """
        pass

class Arbre:
    def __init__(self,racine):
        self.racine = racine
        
def arbre_inclusion(polygones):
    """
    prend un ensemble de polygones qui ne s'intersectent pas (hormis sur leur bord).
    renvoie un arbre (le noeud racine etant le plan) indiquant qui est inclu dans qui.
    pre-condition: pas de doublons, pas d'intersections hors bordures.
    """
    racine = Noeud("PLAN")
    arbre = Arbre(racine)
    arbre_inclusion_iter(racine,polygones)
    pass

def arbre_inclusion_iter(noeud,polygones):
    """
    construit les fils de la racine en mettant des polygones comme contenu des 
    noeuds
    """
    if noeud is None:
        return

    pass

def est_maximal(poly,polygones):
    for polygone in polygones:
        if polygone != poly and polygone.contient(poly) :
            return False
    return True

"""
- construire un dico avec {polygone : poly qui contiennent polygone}
- si polygone : []  donc c'est le fils de "PLAN"
- sinon : trouver le plus petit polygone parmis les poly (son pere)
    pour pouvoir constuire un dicà = {polygone : son pere}
"""
def construire_hash(polygones):
    hash_polygones = {polygone:[] for polygone in polygones}
    for cle in polygones:
        for contient_cle in polygones:
            if contient_cle != cle and contient_cle.contient(cle):
                hash_polygones[cle].append(contient_cle)
    return hash_polygones

def associer_pere(poly_fils, hash_polygones):
    if hash_polygones[poly_fils] == [] :
        hash_polygones[poly_fils] = "PLAN"
        return 
    hash_polygones[poly_fils] = trouver_plus_petit_poly(hash_polygones[poly_fils])
     

def trouver_plus_petit_poly(polygones):
    for poly_petit in polygones:
        petit = True
        for contient_petit in polygones:
            if poly_petit != contient_petit and not contient_petit.contient(poly_petit) :
                petit = False
                break
        if petit : return poly_petit
    return None 
    # n'arrivera jamais vu que les polygones ne s'intersectent pas donc il existe un petit


def main():
    p1 = Polygone.carre((0, 0), 10)
    p2 = Polygone.carre((0, 0), 8)
    p3 = Polygone.carre((-2, -2), 2)
    p4 = Polygone.carre((2, 2), 1)
    p5 = Polygone.carre((15, 15), 5)
    polygones = [p1, p4, p3, p2, p5]
    affiche(*polygones)
    racine = arbre_inclusion(polygones)
    racine.affichage()


if __name__ == "__main__":
    main()
