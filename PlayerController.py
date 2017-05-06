import pygame


class PlayerController:
    def __init__(self, context):
        self.context = context

    def getNextAction(self, carX):
        if self.context.keys[pygame.K_RIGHT]:
            return 50
        elif self.context.keys[pygame.K_LEFT]:
            return -50
        else:
            return 0