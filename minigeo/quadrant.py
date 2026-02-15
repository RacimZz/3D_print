from minigeo.affichable import calcul_dimensions


class Quadrant:
    """
    delimite une zone rectangulaire du plan.
    """

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def decoupe(self):
        milieu_x = (self.xmin + self.xmax) / 2
        milieu_y = (self.ymin + self.ymax) / 2
        q1 = Quadrant(self.xmin, milieu_x, self.ymin, milieu_y)
        q2 = Quadrant(self.xmin, milieu_x, milieu_y, self.ymax)
        q3 = Quadrant(milieu_x, self.xmax, milieu_y, self.ymax)
        q4 = Quadrant(milieu_x, self.xmax, self.ymin, milieu_y)
        return [q1, q2, q3, q4]
