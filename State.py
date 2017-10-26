class State:

    def __init__(self, id, quantities,resultOf=None): #, parent, reason):
        self.id = id
        self.quantities = quantities
        self.resultOf=resultOf
        # self.parents = [parent]
        # self.reasons = [reason]



    def printSelf(self):
        print("*" * 100)
        for quantity in self.quantities:
            print(quantity.id, ": ", quantity.value, " ", quantity.derivative)

    def toString(self):
        foo = ""
        foo+=str(self.id)+"\n"
        for i in range(len(self.quantities)):
            foo += str(self.quantities[i].name) + " " + str(self.quantities[i].value) + " " + str(
                self.quantities[i].derivative) + "\n"

        return foo
