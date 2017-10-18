class State:
    def __init__(self, id, quantities):
        self.id = id
        self.quantities = quantities

    def printSelf(self):
        print("*" * 100)
        for quantity in self.quantities:
            print(quantity.id, ": ", quantity.value, " ", quantity.derivative)

    def toString(self):
        foo = ""
        for i in range(len(self.quantities)):
            foo += str(self.quantities[i].name) + " " + str(self.quantities[i].value) + " " + str(
                self.quantities[i].derivative) + "\n"

        return foo
