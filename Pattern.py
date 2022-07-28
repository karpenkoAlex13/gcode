our_objects = []


class Geometry:
    def __init__(self):  # , depth):
        self.coordinates = []
        self.additional_coord = 0
        self.consts = {}

    #    self.depth = depth
    def coordinates_received(self): return len(self.coordinates) == self.number_coordinates + self.additional_coord

    def id_object(self): return len(self.coordinates) >= self.number_coordinates and None not in self.consts.values()


class Lines(Geometry):
    def __init__(self):  # , depth, *coordinates):
        super().__init__()
        self.number_coordinates = 2

    #    super().__init__(depth)
    #    self.crds = coordinates

    @staticmethod
    def str():
        return "Lines"

    def get_parameters(self): return self.number_coordinates, True, self.consts.keys()

    def get_coordinates(self): return tuple(self.coordinates),


def angle_definition(x, y):
    if x == 0:
        if y > 0:
            return 90
        return 270
    else:
        from math import degrees, atan
        angle = degrees(atan(y / x))
    if x < 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle


def modul(number):
    if number >= 0:
        return number
    else:
        return -number


class Circle(Geometry):
    def __init__(self):  # , depth, *coordinates):
        super().__init__()
        self.number_coordinates = 3

    #    super().__init__(depth)
    #    self.crds = coordinates

    @staticmethod
    def str():
        return "Circle"

    def get_parameters(self):
        return self.number_coordinates, False, self.consts.keys()

    def get_coordinates(self, g_code=False):
        coord1, coord2, coord3 = self.coordinates
        pos1, pos2 = ((coord1[0] + coord2[0]) / 2, (coord1[1] + coord2[1]) / 2), \
                     ((coord2[0] + coord3[0]) / 2, (coord2[1] + coord3[1]) / 2)
        if not coord2[1] - coord1[1] or coord1 == coord2 or coord2 == coord3 or coord3 == coord1:
            y = coord2[1]
            x = (coord2[0] + coord1[0]) / 2
        elif not coord3[1] - coord2[1]:
            y = coord2[1]
            x = (coord3[0] + coord3[0]) / 2
        else:
            k1, k2 = -(coord2[0] - coord1[0]) / (coord2[1] - coord1[1]), -(coord3[0] - coord2[0]) / (
                    coord3[1] - coord2[1])
            x = (pos2[0] * k2 - pos1[0] * k1 + pos1[1] - pos2[1]) / (k2 - k1)
            y = pos1[1] + (x - pos1[0]) * k1
        r = ((x - coord1[0]) ** 2 + (y - coord1[1]) ** 2) ** 0.5
        a1 = angle_definition(coord1[0] - x, y - coord1[1])
        a2 = angle_definition(coord2[0] - x, y - coord2[1])
        a3 = angle_definition(coord3[0] - x, y - coord3[1])
        if g_code:
            if a3 > a2 > a1 or a1 > a2 > a3:
                if modul(a3 - a1) > 180:
                    r *= -1
            else:
                if modul(a3 - a1) < 180:
                    r *= -1
            return coord1[0], coord1[1], ("G3 ", "G2 ")[a3 > a2 > a1 or a1 > a3 > a2 or a2 > a1 > a3], coord3[0], coord3[1], r
        else:
            return x - r, y - r, x + r, y + r, a1, ((a3 - a1 + 360, a3 - a1 - 360)[a3 - a1 > 0], a3 - a1)[
                a1 < a2 < a3 or a1 > a2 > a3]


class Bezier_curve(Geometry):
    def __init__(self):  # , depth, *coordinates):
        super().__init__()
        self.number_coordinates = 3
        self.consts = {"segments": None}

    #    super().__init__(depth)
    #    self.crds = coordinates

    @staticmethod
    def str():
        return "Curve"

    def get_parameters(self):
        return self.number_coordinates, True, self.consts.keys()

    def get_coordinates(self):
        coordinates = ()
        k = 0
        step = 1 / self.consts["segments"]
        while int(k) < 1:
            crds = self.coordinates[:]
            while len(crds) != 1:
                for i in range(1, len(crds)):
                    crds[i - 1] = (crds[i - 1][0] + (crds[i][0] - crds[i - 1][0]) * k,
                                   crds[i - 1][1] + (crds[i][1] - crds[i - 1][1]) * k)
                del crds[-1]
            coordinates += (crds[0],)
            k += step
        coordinates += (self.coordinates[-1],)
        return coordinates,


objects = (Lines, Circle, Bezier_curve)


def create_code(k):
    code = ""
    for element in our_objects:
        if isinstance(element, Circle):
            start_x, start_y, command, x, y, r = element.get_coordinates(g_code=True)
            code += f"G0 X{round(start_x * k, 4)} Y{round(start_y * k, 4)}\n"
            code += "G1 Z-10\n"
            code += command + f"X{round(x*k, 4)}, Y{round(y*k, 4)} R{round(r*k, 4)}\n"
            code += "G0 Z0\n"
        else:
            for line in element.get_coordinates():
                x, y = line[0]
                code += f"G0 X{round(x*k, 4)} Y{round(y*k, 4)}\n"
                code += "G1 Z-10\n"
                for x, y in line[1:]:
                    code += f"G1 X{round(x*k, 4)} Y{round(y*k, 4)}\n"
                code += "G0 Z0\n"
    return code
