import Box2D.b2
import math
import pygame


class Terrain:
    class Tile:
        def __init__(self, context, x, y, x2, y2):
            self.context = context
            self.x = x
            self.y = y
            o = y2 - y
            a = x2 - x
            self.w = math.sqrt(o**2 + a**2)
            self.h = 0.2
            self.rotation = math.atan2(o, a)
            self.body = context.world.CreateStaticBody(
                position=(self.x+a/2, self.y+o/2),
                angle=self.rotation,
            )
            self.body.CreatePolygonFixture(box=(self.w/2, self.h/2), friction=0.9, density=2.0)

        def update(self):
            pass

        def draw(self):
            for fixture in self.body.fixtures:
                shape = fixture.shape
                vertices = [(self.body.transform * v) * self.context.PPM for v in shape.vertices]
                vertices = [(v[0], self.context.SCREEN_HEIGHT - v[1]) for v in vertices]
                pygame.draw.polygon(self.context.screen, (127, 127, 127, 255), vertices)

    def __init__(self, context, startX, startY, stepSize, length, composer):
        self.context = context
        self.tiles = []
        self.x = startX
        self.y = startY
        self.composer = composer
        self.stepSize = stepSize
        for i in range(length):
           self.add()

    def add(self):
        newX = self.x + self.stepSize
        newY = self.y + self.composer.compute(newX)
        self.tiles.append(Terrain.Tile(self.context, self.x, self.y, newX, newY))
        self.x = newX
        self.y = newY

    def update(self):
        pass

    def draw(self):
        for tile in self.tiles:
            tile.draw()
