

class Quantity:
    def __init__(self, name, value, derivative, range, exogenous,resultOf):
        self.name = name
        self.value = value
        self.derivative = derivative
        self.range = range
        self.exogenous = exogenous
        self.resultOf=resultOf



    def printSelf(self):
        print("*"*100)
        print("name: ", self.name)
        print("value: ", self.value)
        print("derivative: ", self.derivative)
        print("range: ", self.range)
        print("exogenous: ", self.exogenous)
