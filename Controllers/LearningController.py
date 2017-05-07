import numpy as np
import lib.neuralnetworksbylayer as nn
from Controllers.Controller import Controller


class LearningController(Controller):
    def __init__(self, context):
        self.context = context
        
        # constants
        self.epsilon = 1
        self.finalEpsilon = 0.01
        self.nTrials = 1000
        self.epsilonDecay = np.exp(np.log(self.finalEpsilon)/self.nTrials)
        self.nSCGIterations = 100
        self.gamma = 0.999
        
        # neural network
        self.nh = [30, 30, 30]
        self.size = 15
        self.qnet = nn.NeuralNetwork([self.size] + self.nh + [1])  # [4, 5, 5, 1]

        self.validActions = np.array([-5, 0, 1, 5, 10, 20])

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
        newScore = self.context.calculateScore()
        newAction = self.decideNextAction(newState)
        if self.lastState is not None:
            self.samples.append(self.lastState.tolist() + [self.lastAction, self.lastScore] + newState.tolist() + [newAction])
        self.lastState = newState
        self.lastScore = newScore
        self.lastAction = newAction

        return int(newAction)

    def decideNextAction(self, state):
        if np.random.rand(1) < self.epsilon:
            # actioni = np.random.randint(self.validActions.shape[0])
            actioni = np.random.choice(np.array([0, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5]))
        else:
            inputs = np.hstack((np.tile(state, (self.validActions.shape[0], 1)), self.validActions.reshape((-1, 1))))
            qs = self.qnet.use(inputs)
            actioni = np.argmax(qs)
        return self.validActions[actioni]
    
    def genState(self, carPos):
        car = self.context.car.car
        tiles = self.context.terrain.getTilesAfter(carPos[0], 10)
        tiles = [t.y - carPos[0] + 3 for t in tiles]
        return np.array([car.angle, car.angularVelocity, car.linearVelocity[0], car.linearVelocity[1]] + tiles)

    def learn(self):
        """
        time to learn something using the data that was collected
        """
        self.samples = np.array(self.samples)
        X = self.samples[:, :self.size]
        R = self.samples[:, self.size:self.size+1]
        nextX = self.samples[:, self.size+1:]
        print(self.samples.shape)
        print(nextX.shape)
        print(nextX)
        nextQ = self.qnet.use(nextX)

        self.qnet.train(X, R + self.gamma * nextQ, nIterations=self.nSCGIterations)

        self.epsilon *= self.epsilonDecay

    def startNewRound(self):
        self.initVars()
