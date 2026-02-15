import minigeo.point as point
from minigeo.segment import Segment

from itertools import cycle
from os import system

COULEURS = (
    "red",
    "green",
    "blue",
    "purple",
    "orange",
    "darkolivegreen",
    "cadetblue",
    "pink",
    "goldenrod",
    "beige",
    "plum",
)
NUMERO_IMAGE = 0


def est_point(objet):
    return (
        isinstance(objet, tuple)
        and (isinstance(objet[0], float) or isinstance(objet[0], int))
        and (isinstance(objet[1], float) or isinstance(objet[1], int))
    )


def est_iterable(objet):
    return hasattr(objet.__class__, "__iter__") and callable(
        getattr(objet.__class__, "__iter__")
    )


def marche(objet_s):
    """
    parcourt recursivement tout ce qui est dans l'objet_s
    """
    if not est_point(objet_s) and est_iterable(objet_s):
        for objet in objet_s:
            yield from marche(objet)
    else:
        yield objet_s


def calcul_dimensions(affichables):
    """
    calcule les dimensions du rectangle de surface minimal contenant tous les objets donnes
    """
    dimensions = (float("inf"), float("-inf"), float("inf"), float("-inf"))
    for affichable in marche(affichables):
        if est_point(affichable):
            dimensions = point.mise_a_jour_dimensions(dimensions, affichable)
        else:
            dimensions = affichable.mise_a_jour_dimensions(dimensions)
    return dimensions


def ajustement_dimensions(dimensions):
    """
    rectifie les dimensions pour eviter les images monodimensionnelles
    """
    xmin, xmax, ymin, ymax = dimensions
    if xmin == float("inf"):
        return None
    if xmin == xmax and ymin == ymax:
        return None
    if xmin == xmax:
        dimension = ymax - ymin
        xmax += dimension / 2
        xmin -= dimension / 2
    if ymin == ymax:
        dimension = xmax - xmin
        xmax += dimension / 2
        xmin -= dimension / 2
    return xmin, xmax, ymin, ymax


def affiche(*affichables):
    """
    calcule le svg correspondant a tous les objets donnes en argument
    et l'affiche dans kitty.
    """
    dimensions = calcul_dimensions(affichables)
    dimensions = ajustement_dimensions(dimensions)
    if dimensions is None:
        return

    xmin, xmax, ymin, ymax = dimensions
    global NUMERO_IMAGE
    nom_image = f"img_{NUMERO_IMAGE}.svg"
    with open(nom_image, "w") as svg:
        print(
            f"<svg width='800' height='600' viewBox='{xmin} {ymin} {xmax - xmin} {ymax - ymin}'>",
            file=svg,
        )
        print(
            f"<g stroke-width='1%' transform='translate(0, {ymin + ymax}) scale(1,-1)'>",
            file=svg,
        )
        for groupe, couleur in zip(affichables, cycle(COULEURS)):
            print(f"<g fill='{couleur}' stroke='{couleur}'>", file=svg)
            for affichable in marche(groupe):
                if est_point(affichable):
                    print(point.code_svg(affichable), file=svg)
                else:
                    print(affichable.code_svg(), file=svg)
            print("</g>", file=svg)
        print("</g>", file=svg)
        print("</svg>", file=svg)
    print(NUMERO_IMAGE)
    system(f"kitty +kitten icat {nom_image}")
    NUMERO_IMAGE += 1


def main():
    trucs = [(1, 2), Segment((2, 3), (4, 2)), [(0, 0), (3, 3)]]
    affiche(*trucs)


if __name__ == "__main__":
    main()
