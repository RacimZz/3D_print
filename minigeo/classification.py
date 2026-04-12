from minigeo.polygone import Polygone
from minigeo.affichable import affiche
from os import system


class Noeud:
    def __init__(self, contenu):
        self.contenu = contenu
        self.enfants = []

    def affiche_dot(self, dot):
        nom = "PLAN" if isinstance(self.contenu, str) else f"n{id(self.contenu)}"
        for fils in self.enfants:
            print(f"{nom} -> n{id(fils.contenu)};", file=dot)
            fils.affiche_dot(dot)

    def affichage(self):
        """
        creation d'un fichier dot, conversion en png et affichage dans kitty
        """
        with open("test.dot", "w") as dot:
            print("digraph g {", file=dot)
            self.affiche_dot(dot)
            print("}", file=dot)
        system("dot -Tpng test.dot -o test.png")
        system("kitty +kitten icat test.png")

    def ajout_polygone(self, poly):
        for fils in self.enfants:
            if fils.contenu.contient(poly):
                fils.ajout_polygone(poly)
                break
        else:
            fils_restants = []
            fils_contenus = []
            for fils in self.enfants:
                if poly.contient(fils.contenu):
                    fils_contenus.append(fils)
                else:
                    fils_restants.append(fils)
            nouveau_fils = Noeud(poly)
            nouveau_fils.enfants = fils_contenus
            self.enfants = fils_restants
            self.enfants.append(nouveau_fils)


def arbre_inclusion(polygones):
    """
    prend un ensemble de polygones qui ne s'intersectent pas (hormis sur leur bord).
    renvoie un arbre (le noeud racine etant le plan) indiquant qui est inclu dans qui.
    pre-condition: pas de doublons, pas d'intersections hors bordures.
    """
    racine = Noeud("PLAN")
    for poly in polygones:
        racine.ajout_polygone(poly)
    return racine


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
