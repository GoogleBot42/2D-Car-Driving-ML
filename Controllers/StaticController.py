from Controllers.Controller import Controller


# does no learning.  runs in only one way
# hand written
class StaticController(Controller):
    nTrials = 0
    def __init__(self, context):
        self.context = context

    def getNextAction(self, carPos):
        tiles = self.context.terrain.getTilesAfter(carPos[0], 10)
        s = 0.0
        for t in tiles: s += t.y - carPos[1] + 3
        return max(1.5,s)