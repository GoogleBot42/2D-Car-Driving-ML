from Controllers.Controller import Controller


class DumbController(Controller):
    nTrials = 0
    def getNextAction(self, carPos):
        return 40
