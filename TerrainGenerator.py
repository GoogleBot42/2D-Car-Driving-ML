import math


class Composer:
    def __init__(self, amplitude, period, offset=0):
        self.amplitude = amplitude
        self.period = period
        self.offset = offset

    def compute(self, x):
        s1 = self.amplitude * math.sin(self.offset + x * x / self.period)
        s2 = self.amplitude / 8 * math.sin(self.offset + math.pi + x / self.period)
        return s1 + s2

class Decomposer:
    def __init__(self):
        pass
