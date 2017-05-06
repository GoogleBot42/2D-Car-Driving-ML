import pygame
from Terrain import Terrain
from Car import Car
import TerrainGenerator
import math
import Box2D
import sys
from Controllers.PlayerController import PlayerController
from Controllers.DumbController import DumbController
from Controllers.StaticController import StaticController


class Context:

    def __init__(self):
        pygame.init()

        # constants
        self.PPM = 20.0  # pixels per meter
        self.TARGET_FPS = 60
        self.TIME_STEP = 1.0 / self.TARGET_FPS
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        
        self.screenSize = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.zoom = 1.0
        self.offset = [0, 0]
        self.viewCenter = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)
        
        self.clock = pygame.time.Clock()

        # core objects
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.world = Box2D.b2.world(gravity=(0, -9.81), doSleep=True)

        # world objects
        self.terrain = Terrain(self, 0, self.SCREEN_HEIGHT/self.PPM/3, 1, 200, TerrainGenerator.Composer(0.9, math.pi))
        
        
        controllers = [PlayerController(self), DumbController(), StaticController(self)]
        self.carController = controllers[int(sys.argv[1])]
        self.car = Car(self, 25, 20, self.carController)
        
        self.keys = pygame.key.get_pressed()

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.terrain.draw()
        self.car.draw()
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)
