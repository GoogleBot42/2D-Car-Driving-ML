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
from Controllers.RandomController import RandomController


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
        self.ROUNDS_TO_SKIP = 100
        self.roundsLeftToSkip = 0
        self.difficulty = 0.4
        self.testRounds = 10

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
        
        self.roundsTrained = 0
        self.currentController = 0

        # car controllers
        # PlayerController(self)
        self.controllers = [LearningController(self,20,[10,100,100,10],30), LearningController(self,100,[10],30)]
        self.testControllers = self.controllers + [DumbController(), StaticController(self), RandomController(self)]
        self.names = ["l1","l2","dc","sc","rc"]
        self.testScores = [0] * len(self.testControllers)

        self.keys = pygame.key.get_pressed()

        self.simStartTime = pygame.time.get_ticks()
        self.isTesting = False
        self.startNewRound()

        # the "car is stuck" timer
        pygame.time.set_timer(pygame.USEREVENT, 100) # every 3 sec check if car is stuck
        self.ignoreCarCheck = True # during setup and when car isn't running
        self.distanceSinceLastCheck = 0
        self.shouldSkipNextCheck = False
        self.eventCounter = 0

        self.score = 0
        
        self.terrainController = None

    def update(self):
        self.ignoreCarCheck = False
        self.keys = pygame.key.get_pressed()
        self.terrain.update()
        self.car.update()
        self.world.Step(self.TIME_STEP, 10, 10)

        if self.car.car.position[0] < 5:
            self.score = 0
            self.carIsDone = True

        if self.terrain.tiles[-1].x - self.car.car.position[0] < 200: # reached end of track
            self.score = 1
            self.carIsDone = True

        if self.carIsDone:
            self.ignoreCarCheck = True
            self.shouldSkipNextCheck = True
            self.startNewRound(isFirst=False)
            self.carIsDone = False
            self.score = 0

    def calculateScore(self):
        distanceScore = (self.car.car.position[0] -5)
        return self.score

    def calculateRelativeScore(self):
        """
        How is the car doing since was last asked?
        """
        return self.score

    def displayScore(self):
        text = self.font.render("Score: " + str(self.car.car.position[0] - 5), True, (255, 255, 255, 255))
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
            print("Score for this run", self.calculateScore())
            print("Distance", self.car.car.position[0], "Time", (pygame.time.get_ticks() - self.simStartTime))
            print("Beginning train.  This could take some time.")
            if self.isTesting:
                self.roundsLeftToSkip = 1
                print(self.names[self.currentController-1])
                self.testScores[self.currentController-1] += self.calculateScore()
            else:
                self.carController.learn()
            print("Done")
            self.carController.startNewRound()
            self.car.destroy()
            self.terrain.destroy()
            if self.roundsLeftToSkip == 0:
                self.roundsLeftToSkip = self.ROUNDS_TO_SKIP
            else:
                self.roundsLeftToSkip -= 1
            print("Rounds left", self.roundsLeftToSkip)
        else:
            self.roundsLeftToSkip = 0
        self.carController, self.terrainController = self.getControllers()
        self.terrain = Terrain(self, 0, self.SCREEN_HEIGHT / self.PPM / 3, 1, 300, self.terrainController)
        self.car = Car(self, 6, 16, self.carController)
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
     
    def getControllers(self):
        if self.isTesting:
            if self.currentController == len(self.testControllers):
                self.terrainController = TerrainGenerator.Composer(self.difficulty, math.pi, offset=(random.random()*math.pi, random.random()*math.pi/2))
                self.currentController = 0
                self.testRounds -= 1
                if self.testRounds == 0:
                    print("Final scores")
                    print(self.testScores)
                    quit()
            controller = self.testControllers[self.currentController]
            controller.startingTestMode()
            self.currentController += 1
            return controller, self.terrainController
        else:
            controller = self.controllers[self.currentController]
            if self.roundsTrained >= controller.nTrials:
                self.currentController += 1
                self.roundsTrained = 0
                if self.currentController == len(self.controllers):
                    self.currentController = len(self.testControllers)
                    self.isTesting = True
                    return self.getControllers()
            self.roundsTrained += 1
            return self.controllers[self.currentController], TerrainGenerator.Composer(self.difficulty, math.pi, offset=(random.random()*math.pi, random.random()*math.pi/2))
