import pygame
from Controllers.Controller import Controller


class PlayerController(Controller):
    def __init__(self, context):
        self.context = context

    def getNextAction(self, carX):
        if self.context.keys[pygame.K_RIGHT]:
            return 40
        elif self.context.keys[pygame.K_LEFT]:
            return -5
        else:
            return 0
