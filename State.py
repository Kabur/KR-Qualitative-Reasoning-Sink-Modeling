class State:
    def __init__(self, id, quantities):
        self.id = id
        self.quantities = quantities

    def printSelf(self):
        print("*" * 100)
        for quantity in self.quantities:
            print(quantity.id, ": ", quantity.value, " ", quantity.derivative)

    def toString(self):
        str = ""
        for i in range(len(self.quantities)):
            str += self.quantities[i].id + " " + str(self.quantities[i].value) + " " + str(
                self.quantities[i].derivative) + "\n"

        return str
