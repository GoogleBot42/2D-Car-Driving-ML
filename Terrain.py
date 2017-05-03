import Box2D.b2
import math
import pygame


class Terrain:
    class Tile:
        def __init__(self, context, x, y, w, h):
            self.context = context
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.body = context.world.CreateStaticBody(
                position=(x, y),
                shapes=Box2D.b2.polygonShape(box=(w, h)),
                angle=math.pi
            )

        def update(self):
            pass

        def draw(self):
            for fixture in self.body.fixtures:
                shape = fixture.shape
                vertices = [(self.body.transform * v) * self.context.PPM for v in shape.vertices]
                vertices = [(v[0], self.context.SCREEN_HEIGHT - v[1]) for v in vertices]
                pygame.draw.polygon(self.context.screen, (127, 127, 127, 255), vertices)

    def __init__(self, context, startX, startY, tileWidth, tileHeight, length):
        self.context = context
        self.tiles = []
        self.x = startX + tileWidth/2
        self.y = startY + tileHeight/2
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        for i in range(length):
            self.add()

    def add(self):
        self.tiles.append(Terrain.Tile(self.context, self.x, self.y, self.tileWidth/2, self.tileHeight/2))
        self.x += self.tileWidth
        self.y += self.tileHeight

    def update(self):
        pass

    def draw(self):
        for tile in self.tiles:
            tile.draw()
