import pygame
import math
pygame.init()


class Hero:
    def __init__(self, window, path, speed, degrees, images, pos):
        self.window = window
        self.degrees = degrees
        self.speed = speed
        self.image = pygame.image.load(path).convert_alpha()
        self.images = images
        self.rect = self.image.get_rect(topleft=pos)
        self.rotation = list()
        self.counter = 0

    def _collision(self, map, angle) -> bool:
        x, y = self.speed * math.cos(math.radians(angle)), self.speed * math.sin(math.radians(angle))
        funcx = lambda posx, posy: (posx-self.rect.centerx)*math.cos(math.radians(angle)) - (posy-self.rect.centery)*math.sin(math.radians(angle)) + self.rect.centerx
        funcy = lambda posx, posy: (posx-self.rect.centerx)*math.sin(math.radians(angle)) + (posy-self.rect.centery)*math.cos(math.radians(angle)) + self.rect.centery
        try: return all([map[int(funcy(self.rect.bottomright[0]+2, self.rect.bottomright[1]+2)+y)//32][int(funcx(self.rect.bottomright[0]+2, self.rect.bottomright[1]+2)+x)//32] != '1', map[int(funcy(self.rect.topright[0]+2, self.rect.topright[1]-2)+y)//32][int(funcx(self.rect.topright[0]+2, self.rect.topright[1]-2)+x)//32] != '1'])
        except IndexError: return False

    def _animation(self, speed: int):
        self.count = len(self.images) * speed
        if self.counter < self.count: ct, self.counter = self.counter // speed, self.counter + 1
        else: ct, self.counter = 0, 0
        return self.images[ct]

    def move(self, map):
        self.image = self._animation(9)
        if self.rotation != []:
            if self._collision(map, self.rotation[0]): self.degrees = self.rotation[0]
        x, y = self.speed * math.cos(math.radians(self.degrees)), self.speed * math.sin(math.radians(self.degrees))
        if self._collision(map, self.degrees):
            if self.rect.x > self.window.get_size()[0]: self.rect.x = -30
            if self.rect.x < -30: self.rect.x = self.window.get_size()[0] - 10
            self.rect.x, self.rect.y = self.rect.x+x, self.rect.y+y
        self.image = pygame.transform.rotate(self.image, -self.degrees)
        self.window.blit(self.image, self.rect)


class AStar:
    def __init__(self, matrix):
        self.matrix = matrix
        self.stp, self.ep = tuple(), tuple()
        self.open_list, self.close_list = dict(), dict()
        self.path = []

    def calc(self, point, prop):
        self.close_list[point] = prop
        for x, y in zip([point[0], *range(point[0]-1, point[0]+2), point[0]], [point[1]-1, *[point[1] for _ in range(3)], point[1]+1]):
            if (x, y) not in self.close_list and self.matrix[y][x] != '1':
                Hcost = sorted([abs(x-self.ep[0]), abs(y-self.ep[1])])[0]*14 + abs(abs(x-self.ep[0]) - abs(y-self.ep[1]))*10
                if (x, y) in self.open_list.keys():
                    if prop[1] + (14 if abs(x - point[0]) - abs(y - point[1]) == 0 else 10) <= self.open_list.get((x, y))[1]: Gcost, point1 = prop[1] + (14 if abs(x - point[0]) - abs(y - point[1]) == 0 else 10), point
                    else: Gcost, point1 = self.open_list.get((x, y))[1], self.open_list.get((x, y))[3]
                else: Gcost, point1 = prop[1] + (14 if abs(x - point[0]) - abs(y - point[1]) == 0 else 10), point
                self.open_list[(x, y)] = [Hcost, Gcost, Hcost + Gcost, point1]

        try:
            pointed = sorted(list(self.open_list.items()), key=lambda x: x[1][2])[0]
            if pointed[0] != self.ep:del self.open_list[pointed[0]]; self.calc(*pointed)
            else:self.close_list[pointed[0]] = pointed[1]; self._path(self.close_list, self.ep)
        except IndexError: return

    def _path(self, path, key):
        self.path.append(key)
        if path.get(key)[3] != self.stp:
            new_key = path.get(key)[3]
            del path[key]
            self._path(path, new_key)


class Enemy:
    def __init__(self, window, path, speed, images, pos):
        self.window = window
        self.image = pygame.image.load(path).convert_alpha()
        self.speed = speed
        self.images = images
        self.rect = self.image.get_rect(topleft=pos)
        self.ct = 0
        self.check = True
        self.path = list()
        self.stp = pos

    def get_path(self, points, path):
        if self.check:
            for point in points:path.stp, path.ep = point, tuple(map(lambda p: p // 32, self.stp)); path.calc(path.stp, [0, 0, 0, path.stp]); self.path.extend(path.path); path.open_list, path.close_list, path.path = dict(), dict(), list(); self.stp = tuple(map(lambda p: p * 32 + 3, point))
            else: self.check = False

    def move(self):
        if (length := math.dist(self.rect.topleft, tuple(map(lambda p: p*32+3, self.path[self.ct]))))>1:
            self.rect.x += (speedx := self.speed * math.cos(math.acos((self.path[self.ct][0]*32+3-self.rect.x)/length)))
            self.rect.y += (speedy := self.speed * math.sin(math.asin((self.path[self.ct][1]*32+3-self.rect.y)/length)))
            self.image = self.images.get(int(math.degrees(math.acos(int(speedx)//self.speed))) if int(speedx)//self.speed != 0 else int(math.degrees(math.asin(int(speedy)//self.speed))))
        else:
            if self.ct+1 < len(self.path): self.ct += 1
            else: self.ct, self.path, self.check = 0, [], True

    def draw(self):
        self.window.blit(self.image, self.rect)
