import random
import numpy as np

class Ant:
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta
        self.route = []
        self.visited = set()

    def reset(self, start_city):
        self.route = [start_city]
        self.visited = {start_city}


class AlphaAnt(Ant):
    def __init__(self):
        super().__init__(alpha=0, beta=1)