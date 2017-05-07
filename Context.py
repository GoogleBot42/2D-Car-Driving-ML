import pygame
from Terrain import Terrain
from Car import Car
import TerrainGenerator
import math
import Box2D
import sys
from random import random
from Controllers.PlayerController import PlayerController
from Controllers.DumbController import DumbController
from Controllers.StaticController import StaticController
from Controllers.LearningController import LearningController


class Context(Box2D.b2.contactListener):

    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

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
        self.carIsDone = False
        
        self.clock = pygame.time.Clock()

        # core objects
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        Box2D.b2.contactListener.__init__(self)
        self.world = Box2D.b2.world(gravity=(0, -9.81), doSleep=True, contactListener=self)

        # world objects
        self.terrain = Terrain(self, 0, self.SCREEN_HEIGHT/self.PPM/3, 1, 200, TerrainGenerator.Composer(0.9, math.pi, offset=random()*math.pi))
        
        controllers = [PlayerController(self), DumbController(), StaticController(self), LearningController(self)]
        self.carController = controllers[int(sys.argv[1])]
        self.car = Car(self, 5, 20, self.carController)
        
        self.keys = pygame.key.get_pressed()
        
        self.simStartTime = pygame.time.get_ticks()

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)
        
        if self.carIsDone:
            print("Car lost", self.calculateScore())
            self.car.destroy()
            self.car = Car(self, 5, 20, self.carController)
            self.simStartTime = pygame.time.get_ticks()
            self.carIsDone = False
    
    def calculateScore(self):
        distanceScore = (self.car.car.position[0] -5) / self.terrain.tiles[-1].x
        timeScore = (pygame.time.get_ticks() - self.simStartTime) 
        return distanceScore**3 / timeScore * 1000000
    
    def displayScore(self):
        text = self.font.render("Score: " + str(self.calculateScore()), True, (255, 255, 255, 255))
        self.screen.blit(text,(0,0))
        
    def BeginContact(self, contact):
        if (contact.fixtureA == self.car.car.fixtures[0] or contact.fixtureB == self.car.car.fixtures[0]):
            self.carIsDone = True

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.terrain.draw()
        self.car.draw()
        
        self.displayScore()
        
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)
