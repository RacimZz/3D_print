from minigeo.polygone import Polygone
from minigeo.affichable import affiche
from os import system

class Noeud:
    def __init__(self, contenu):
        self.contenu = contenu
        self.fils = []

    def affichage(self):
        """
        creation d'un fichier dot, conversion en png et affichage dans kitty
        """

        with open("arbre.dot","w",encoding="utf-8") as f:
            f.write("digraph g {\n")
            afficher_noeud_fils(self,f)
            f.write("}")
        system("dot -Tpng arbre.dot -o arbre.png")
        system(f"kitty +kitten icat arbre.png")

        


def afficher_noeud_fils(noeud,f):
    for fils in noeud.fils:
        if noeud.contenu == "PLAN":
            f.write(f"nPLAN -> n{id(fils.contenu)};\n")
            continue
        f.write(f"n{id(noeud.contenu)} -> n{id(fils.contenu)};\n")
    for fils in noeud.fils:
        afficher_noeud_fils(fils,f)
"""
- construire un dico avec {polygone : poly qui contiennent polygone}
- si polygone : []  donc c'est le fils de "PLAN"
- sinon : trouver le plus petit polygone parmis les poly (son pere)
    pour pouvoir constuire un dicà = {polygone : son pere}
"""
def construire_hash(polygones):
    hash_polygones = {polygone:None for polygone in polygones}

    for cle in polygones:
        for contient_cle in polygones:
            if contient_cle == cle :
                continue # on skip quand ca compare le meme poly

            if contient_cle.contient(cle) and hash_polygones[cle] is None:
                hash_polygones[cle] = contient_cle # pour initialiser le premier potentiel parent
                continue 

            if contient_cle.contient(cle) and hash_polygones[cle].contient(contient_cle):
                hash_polygones[cle] = contient_cle # on a trouver plus petit
        if hash_polygones[cle] is None :
            hash_polygones[cle] = "PLAN"
    return hash_polygones


# ----------------- fin des fonctions auxiliaire --------------------------------------

def arbre_inclusion(polygones):
    """
    prend un ensemble de polygones qui ne s'intersectent pas (hormis sur leur bord).
    renvoie un arbre (le noeud racine etant le plan) indiquant qui est inclu dans qui.
    pre-condition: pas de doublons, pas d'intersections hors bordures.
    """
    racine = Noeud("PLAN")
    hash_polygones = construire_hash(polygones)
    # j'ai maintenant un dictionnaire fils : pere
    inclusion_rec(racine,hash_polygones)
    return racine

    
def inclusion_rec(noeud,hash_polygones):
    noeud.fils = [Noeud(cle) for cle, valeur in hash_polygones.items() if valeur == noeud.contenu]
    for fils in noeud.fils:
        inclusion_rec(fils,hash_polygones)


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
