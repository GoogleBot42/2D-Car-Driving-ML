import pygame
from Terrain import Terrain
from Car import Car
import TerrainGenerator
import math
import Box2D
import sys
import random
from datetime import datetime
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

        # car controllers
        controllers = [PlayerController(self), DumbController(), StaticController(self), LearningController(self)]
        self.carController = controllers[int(sys.argv[1])]
        
        self.keys = pygame.key.get_pressed()

        self.simStartTime = pygame.time.get_ticks()
        self.startNewRound()

        # the "car is stuck" timer
        pygame.time.set_timer(pygame.USEREVENT, 3000) # every 3 sec check if car is stuck
        self.ignoreCarCheck = True # during setup and when car isn't running
        self.distanceSinceLastCheck = 0

    def update(self):
        self.ignoreCarCheck = False
        self.keys = pygame.key.get_pressed()
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)

        if self.terrain.tiles[-1].x - self.car.car.position[0] < 2: # reached end of track
            self.carIsDone = True

        if self.carIsDone:
            self.ignoreCarCheck = True
            self.startNewRound(isFirst=False)
            self.carIsDone = False

    def calculateScore(self):
        distanceScore = (self.car.car.position[0] -5) / self.terrain.tiles[-1].x
        timeScore = (pygame.time.get_ticks() - self.simStartTime)
        if timeScore == 0:
            return 0
        return distanceScore**3 / timeScore * 1000000
    
    def displayScore(self):
        text = self.font.render("Score: " + str(self.calculateScore()), True, (255, 255, 255, 255))
        self.screen.blit(text,(0,0))
        
    def BeginContact(self, contact):
        if contact.fixtureA == self.car.car.fixtures[0] or contact.fixtureB == self.car.car.fixtures[0]:
            self.carIsDone = True

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
        self.terrain.draw()
        self.car.draw()
        
        self.displayScore()
        
        pygame.display.flip()
        self.clock.tick(self.TARGET_FPS)

    def startNewRound(self, isFirst=True):
        # python random is terrible
        random.seed(datetime.now())
        if not isFirst:
            print("Car lost", self.calculateScore())
            print("Beginning train.  This could take some time.")
            self.carController.learn()
            self.carController.startNewRound()
            self.car.destroy()
            # self.terrain.destroy()
        else:
            self.terrain = Terrain(self, 0, self.SCREEN_HEIGHT / self.PPM / 3, 1, 200,
                               TerrainGenerator.Composer(0.7, math.pi, offset=(random.random()*math.pi, random.random()*math.pi/2)))
        self.car = Car(self, 5, 20, self.carController)
        self.distanceSinceLastCheck = self.car.car.position[0]
        self.simStartTime = pygame.time.get_ticks()

    def handleEvent(self, event):
        if not self.ignoreCarCheck:
            distance = self.car.car.position[0]
            if distance - self.distanceSinceLastCheck < 1:
                self.carIsDone = True
            self.distanceSinceLastCheck = distance
