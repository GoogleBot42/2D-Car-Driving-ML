class Controller:
    def getNextAction(self, carPos):
        return 0 # a sensible default that doesn't move

    def learn(self):
        """
        Called after the car crashes, fails, or finishes a run 
        """
        pass

    def startNewRound(self):
        """
        start new round is always called after learn.  a new round can be started manually by user so learn is skipped
        this function is meant to reset state that is should not be kept between rounds (or "trials")
        """
        pass
