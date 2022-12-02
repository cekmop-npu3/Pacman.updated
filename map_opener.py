class Map:
    def __init__(self, window, path, images: dict):
        self.window = window
        self.path = path
        self.map, self.poses = list(), list()
        self.images = images
        self.pos = tuple()
        self._create()

    def _create(self):
        with open(self.path) as file:
            for line in file: self.map.append(list(line.strip()))
        for x in range(25):
            for y in range(25):
                if self.map[y][x] == '1': self.images.get(self.map[y][x])[1].append((x*32, y*32))
                if self.map[y][x] == '3': self.pos = (x*32+3, y*32+3)
                if self.map[y][x] == '4': self.poses.append((x*32+3, y*32+3))

    def draw(self):
        for obj in list(self.images.values()):
            for pos in obj[1]: self.window.blit(obj[0], pos)
