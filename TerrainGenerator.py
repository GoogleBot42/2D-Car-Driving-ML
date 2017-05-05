import math


class Composer:
    def __init__(self, amplitude, period):
        self.amplitude = amplitude
        self.period = period
        self.offset = 0

    def compute(self, x):
        return self.amplitude * math.sin(self.offset + x / self.period)


class Decomposer:
    def __init__(self):
        pass
