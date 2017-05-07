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
        self.ROUNDS_TO_SKIP = 25
        self.roundsLeftToSkip = 0
        
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
        pygame.time.set_timer(pygame.USEREVENT, 100) # every 3 sec check if car is stuck
        self.ignoreCarCheck = True # during setup and when car isn't running
        self.distanceSinceLastCheck = 0
        self.shouldSkipNextCheck = False
        self.eventCounter = 0
        
        self.lastScore = 0

    def update(self):
        self.ignoreCarCheck = False
        self.keys = pygame.key.get_pressed()
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)

        if self.terrain.tiles[-1].x - self.car.car.position[0] < 30: # reached end of track
            self.terrain.add()

        if self.carIsDone:
            self.ignoreCarCheck = True
            self.shouldSkipNextCheck = True
            self.startNewRound(isFirst=False)
            self.carIsDone = False

    def calculateScore(self):
        distanceScore = (self.car.car.position[0] -5) / self.terrain.tiles[-1].x
        timeScore = (pygame.time.get_ticks() - self.simStartTime)
        if timeScore == 0:
            return 0
        return distanceScore**3 / timeScore * 1000000
    
    def calculateRelativeScore(self):
        """
        How is the car doing since was last asked?
        """
        score = self.calculateScore()
        relativeScore = score - self.lastScore
        self.lastScore = score
        return relativeScore
    
    def displayScore(self):
        text = self.font.render("Score: " + str(self.calculateScore()), True, (255, 255, 255, 255))
        self.screen.blit(text,(0,0))
        
    def BeginContact(self, contact):
        if contact.fixtureA == self.car.car.fixtures[0] or contact.fixtureB == self.car.car.fixtures[0]:
            self.carIsDone = True

    def draw(self):
        if self.roundsLeftToSkip == 0:
            self.screen.fill((0, 0, 0, 0))
            self.terrain.draw()
            self.car.draw()
        
            self.displayScore()
        
            pygame.display.flip()
            # self.clock.tick(self.TARGET_FPS)

    def startNewRound(self, isFirst=True):
        # python random is terrible
        random.seed(datetime.now())
        if not isFirst:
            print("Car lost", self.calculateScore())
            print("Distance", self.car.car.position[0], "Time", (pygame.time.get_ticks() - self.simStartTime))
            print("Beginning train.  This could take some time.")
            self.carController.learn()
            print("Done")
            self.carController.startNewRound()
            self.car.destroy()
            # self.terrain.destroy()
            if self.roundsLeftToSkip == 0:
                self.roundsLeftToSkip = self.ROUNDS_TO_SKIP
            else:
                self.roundsLeftToSkip -= 1
            print("Rounds left", self.roundsLeftToSkip)
        else:
            self.roundsLeftToSkip = 0
            self.terrain = Terrain(self, 0, self.SCREEN_HEIGHT / self.PPM / 3, 1, 300,
                               TerrainGenerator.Composer(0.9, math.pi, offset=(random.random()*math.pi, random.random()*math.pi/2)))
        self.car = Car(self, 5, 20, self.carController)
        self.distanceSinceLastCheck = self.car.car.position[0]
        self.simStartTime = pygame.time.get_ticks()

    def handleEvent(self, event):
        if self.roundsLeftToSkip == 0: # if running in gui take 30 times longer to say car failed
            self.eventCounter += 1
            if self.eventCounter != 30:
                return
            else:
                self.eventCounter = 0
        if not self.ignoreCarCheck:
            if self.shouldSkipNextCheck:
                self.shouldSkipNextCheck = False
            else:
                distance = self.car.car.position[0]
                if distance - self.distanceSinceLastCheck < 1:
                    self.carIsDone = True
                self.distanceSinceLastCheck = distance
