import numpy as np
import lib.neuralnetworksbylayer as nn
from Controllers.Controller import Controller


class LearningController(Controller):
    def __init__(self, context, nTrials, nh, nSCGIterations):
        self.context = context
        self.nTrials = nTrials
        self.nh = nh
        self.nSCGIterations = nSCGIterations


        # constants
        self.epsilon = 1
        self.finalEpsilon = 0.01
        self.epsilonDecay = np.exp(np.log(self.finalEpsilon)/self.nTrials)
        self.gamma = 0.999

        # neural network
        self.size = 17
        self.qnet = nn.NeuralNetwork([self.size] + self.nh + [1])  # [4, 5, 5, 1]

        self.validActions = np.array([-5,0,10,40])

        self.samples = []
        self.lastState = None
        self.lastScore = None
        self.lastAction = None

    def initVars(self):
        self.samples = []
        self.lastState = None
        self.lastScore = None
        self.lastAction = None

    def getNextAction(self, carPos):
        newState = self.genState(carPos)
        newScore = self.context.calculateRelativeScore()
        newAction = self.decideNextAction(newState)
        if self.lastState is not None:
            self.samples.append(self.lastState.tolist() + [self.lastAction, self.lastScore] + newState.tolist() + [newAction])
        self.lastState = newState
        self.lastScore = newScore
        self.lastAction = newAction

        return int(newAction)

    def decideNextAction(self, state):
        if np.random.rand(1) < self.epsilon:
            #actioni = np.random.randint(self.validActions.shape[0])
            actioni = self.pickRandom()
        else:
            inputs = np.hstack((np.tile(state, (self.validActions.shape[0], 1)), self.validActions.reshape((-1, 1))))
            # weird error case
            if inputs.shape == (3,2):
                #actioni = np.random.randint(self.validActions.shape[0])
                actioni = self.pickRandom()
            else:
                qs = self.qnet.use(inputs)
                actioni = np.argmax(qs)
        return self.validActions[actioni]

    def pickRandom(self):
        rand = np.random.rand(1)
        if rand < 0.1:
            return 0
        elif rand < 0.2:
            return 1
        elif rand < 0.35:
            return 2
        else:
            return 3

    def genState(self, carPos):
        car = self.context.car.car
        tiles = self.context.terrain.getTilesAfter(carPos[0] - 5, 15)
        tiles = [t.y - carPos[1] + 3 for t in tiles]
        return np.array([car.angle]+tiles)

    def learn(self):
        """
        time to learn something using the data that was collected
        """
        self.samples = np.array(self.samples)
        X = self.samples[:, :self.size]
        R = self.samples[:, self.size:self.size+1]
        nextX = self.samples[:, self.size+1:]
        nextQ = self.qnet.use(nextX)

        self.qnet.train(X, R + self.gamma * nextQ, nIterations=self.nSCGIterations)

        self.epsilon *= self.epsilonDecay

    def startNewRound(self):
        self.initVars()
    
    def startingTestMode(self):
        self.epsilon = 0.0
