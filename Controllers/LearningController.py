import numpy as np


class LearningController:
    def __init__(self, context):
        self.context = context
        
        # constants
        self.epsilon = 1
        self.finalEpsilon = 0.01
        self.epsilonDecay = np.exp(np.log(finalEpsilon)/(nTrials))
        self.nSCGIterations = 30
        
        # neural network
        self.nh = [8,8]
        self.qnet = nn.NeuralNetwork([15] + nh + [1])  # [4, 5, 5, 1]
        
        self.samples = []
        self.lastState = genState(context.car.car.position[0])

    def getNextAction(self, carPos):
        newState = genState(carPos)
        samples.append(self.lastState,
    
    def genState(self, carPos):
        car = self.context.car.car
        return np.array(
            [car.angle, car.angularVelocity, car.linearVelocity[0], car.linearVelocity[1]] + self.terrain.getTilesAfter(carPos, 10)
        )