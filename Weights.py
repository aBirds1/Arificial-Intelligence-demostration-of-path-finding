from Assignment.main import *

vec = pg.math.Vector2


class Weights():
    def __init__(self):
        super().__init__()
        self.weights = {}

    def cost(self, startnode, goalnode):
        if (vec(goalnode) - vec(startnode)).length_squared() == 1:
            num= self.weights.get(goalnode, 0) + 10
            print('cost is:',num)
            return num
        else:
            num2= self.weights.get(goalnode, 0) + 14
            print('num2 is :',num2)
            return num2
