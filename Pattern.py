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
        if coord1 == coord3:
            r = ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5 / 2
            if g_code:
                return coord1[0], coord1[1], "G2 ", coord3[0], coord3[1], r
            else:
                x, y = (coord1[0] + coord2[0])/2, (coord1[1] + coord2[1])/2
                return x - r, y - r, x + r, y + r, 0, 360
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


class Oval (Geometry):
    def __init__(self):  # , depth, *coordinates):
        super().__init__()
        self.number_coordinates = 2
        self.consts = {"R": None, "start": None, "extend": None, "segments": None}

    #    super().__init__(depth)
    #    self.crds = coordinates

    @staticmethod
    def str():
        return "Oval"

    def get_parameters(self):
        return self.number_coordinates, False, self.consts.keys()

    def get_coordinates(self):
        from math import sin, cos, radians
        crd1, crd2 = self.coordinates
        r = self.consts["R"]
        d_x, d_y = crd2[0] - crd1[0], crd2[1] - crd1[1]
        scale = (d_x**2+d_y**2)**0.5/r
        print(f"scale {scale}")
        if d_x and d_y:
            k = d_y/d_x
            print(k)
        start, extend = self.consts["start"] + angle_definition(d_x, d_y), self.consts["extend"]
        extend = ((extend, -360)[extend < -360], 360)[extend > 360]
        end = start + extend
        d_angle = extend/self.consts["segments"]
        count = 0
        coordinates = ()
        while count <= self.consts["segments"]:
            if count == self.consts["segments"]:
                start = end
            count += 1
            x, y = crd1[0] + r * cos(radians(start)), crd1[1] + r * sin(radians(start))
            if not d_x:
                y += (y - crd1[1]) * (scale-1)
            elif not d_y:
                x += (x - crd1[0]) * (scale-1)
            else:
                x0 = (crd1[1]-y+crd1[0]/k+x*k)/(1/k+k)
                y0 = crd1[1]-(x-x0)*k
                x, y = x+(x-x0)*(scale-1), y+(y-y0)*(scale-1)
            coordinates += (x, y),
            start += d_angle
        return coordinates,


objects = (Lines, Circle, Oval, Bezier_curve)


def min_coordinates():
    x_coordinates, y_coordinates = [], []
    for element in our_objects:
        if isinstance(element, Circle):
            continue
            x1, y1, x2, y2 = element.get_coordinates()[:4]
            x_coordinates.append(x1)
            y_coordinates.append(y1)
            x_coordinates.append(x2)
            y_coordinates.append(y2)
        else:
            for line in element.get_coordinates():
                for x, y in line:
                    x_coordinates.append(x)
                    y_coordinates.append(y)
    return min(x_coordinates), min(y_coordinates)


def create_code(k):
    code = ""
    displacement_x, displacement_y = min_coordinates()
    print(displacement_x, displacement_y)
    pos_x, pos_y = 0, 0
    for element in our_objects:
        if isinstance(element, Circle):
            start_x, start_y, command, x, y, r = element.get_coordinates(g_code=True)
            if pos_x == start_x and pos_y == start_y:
                code = code[:-9]
            else:
                code += f"G0 X{round((start_x-displacement_x) * k, 4)} Y{round((start_y-displacement_y) * k, 4)}\n"
                code += "M3\nG1 Z-10\n"
            code += command + f"X{round((x-displacement_x)*k, 4)} Y{round((y-displacement_y)*k, 4)} R{round(r*k, 4)}\n"
            code += "M5\nG0 Z0\n"
        else:
            for line in element.get_coordinates():
                x, y = line[0]
                if x == pos_x and y == pos_y:
                    code = code[:-9]
                else:
                    code += f"G0 X{round((x-displacement_x)*k, 4)} Y{round((y-displacement_y)*k, 4)}\n"
                    code += "M3\nG1 Z-10\n"
                for x, y in line[1:]:
                    code += f"G1 X{round((x-displacement_x)*k, 4)} Y{round((y-displacement_y)*k, 4)}\n"
                code += "M5\nG0 Z0\n"
        pos_x, pos_y = x, y
    return code
