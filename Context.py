import pygame
from Terrain import Terrain
from Car import Car


class Context:

    def __init__(self, physicsWorld):
        pygame.init()

        # constants
        self.PPM = 20.0  # pixels per meter
        self.TARGET_FPS = 60
        self.TIME_STEP = 1.0 / self.TARGET_FPS
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # core objects
        self.world = physicsWorld
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # world objects
        self.terrain = Terrain(self, 0, 0, 2, 0.2, 3)
        self.car = Car()

    def update(self):
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.terrain.draw()
        self.car.draw()
        pygame.display.flip()
        pygame.time.Clock()
