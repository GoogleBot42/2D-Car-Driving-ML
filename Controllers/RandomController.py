from Controllers.Controller import Controller
import random

class RandomController(Controller):
    nTrials = 0
    def __init__(self, context):
        self.context = context

    def getNextAction(self, carPos):
        rand = random.random()
        if rand < 0.1:
            return -5
        elif rand < 0.2:
            return 0
        else:
            return 40

