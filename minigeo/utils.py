from itertools import pairwise
from math import floor, ceil


def dedup(iterable):
    iterateur = iter(iterable)
    try:
        premier = next(iterateur)
    except StopIteration:
        return
    yield premier
    prec = premier
    for e in iterateur:
        if prec != e:
            yield e
        prec = e


def fenetre_tournante(iterable):
    iterateur = iter(iterable)

    try:
        premier = next(iterateur)
    except StopIteration:
        return

    courant = premier
    for e in iterateur:
        yield courant, e
        courant = e

    yield courant, premier


def recherche_deux_mins(iterable):
    """
    pre-condition: l'iterable contient au moins 2 elements differents
    """
    iterateur = iter(iterable)
    min = next(iterateur)
    second_min = next(iterateur)
    while second_min == min:
        second_min = next(iterateur)
    for e in iterateur:
        if e < min:
            second_min = min
            min = e
        elif e < second_min:
            second_min = e
    return min, second_min


def multiples_entre(debut, fin, facteur):
    assert debut <= fin
    debut_indices = ceil(debut / facteur)
    fin_indices = floor(fin / facteur) + 1
    return (i * facteur for i in range(debut_indices, fin_indices))


class IterateurConsultable:
    def __init__(self, iterable):
        self.iterateur = iter(iterable)
        try:
            self.courant = next(self.iterateur)
            self.fini = False
        except StopIteration:
            self.courant = None
            self.fini = True

    def apercu(self):
        if self.fini:
            raise Exception("vide")
        return self.courant

    def __iter__(self):
        return self

    def __next__(self):
        if self.fini:
            raise StopIteration
        courant = self.courant
        try:
            self.courant = next(self.iterateur)
        except StopIteration:
            self.fini = True
        return courant


def fusion(iterable1, iterable2, clef):
    i1 = IterateurConsultable(iterable1)
    i2 = IterateurConsultable(iterable2)
    while not (i1.fini and i2.fini):
        if i1.fini:
            yield from i2
            return
        elif i2.fini:
            yield from i1
            return
        if clef(i1.apercu()) < clef(i2.apercu()):
            yield next(i1)
        else:
            yield next(i2)
