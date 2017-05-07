from Controllers.Controller import Controller


class DumbController(Controller):
    def getNextAction(self, carPos):
        return 5
