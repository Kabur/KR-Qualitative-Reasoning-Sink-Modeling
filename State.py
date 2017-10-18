class State:
    def __init__(self, name, quantities):
        self.name = name
        self.quantities = quantities

    def printSelf(self):
        print("*"*100)
        for quantity in self.quantities:
            print(quantity.name, ": ", quantity.value, " ", quantity.derivative)


