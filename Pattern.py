our_objects = []


class Geometry:
    pass
    # def __init__(self, depth):
    #    self.depth = depth

    # def drawParams(self):
    #   print('drawParams', self)


class Lines(Geometry):
    def __init__(self):#, depth, *coordinates):
        self.coordinates = []
        self.number_coordinates = 2
    #    super().__init__(depth)
    #    self.crds = coordinates

    @staticmethod
    def str():
        return "Lines"

    def Parameters(self):
        return self.number_coordinates, None

    def append_coordinates(self, coord):
        self.coordinates.append(coord)
        print(self, self.coordinates)

    def translation(self, file):
        for coord in self.crds:
            x, y = coord
            file.write(f"G1 X{x}, Y{y}")


objects = (Lines,)
