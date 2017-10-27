class State:

    def __init__(self, id, quantities,reason=""): #, parent, reason):
        self.id = id
        self.quantities = quantities
        self.reasons=[reason]
        # self.parents = [parent]
        # self.reasons = [reason]



    def printSelf(self):
        print("*" * 100)
        for quantity in self.quantities:
            print(quantity.id, ": ", quantity.value, " ", quantity.derivative)

    def toString(self):
        foo = ""
        # foo+= "State " + str(self.id)+"\n"
        for i in range(len(self.quantities)):
            foo += (str(self.quantities[i].name) + " " + str(self.quantities[i].value) + " " + str(
                self.quantities[i].derivative) + "\n").replace("1", "+").replace("-1", "-").replace("2", "Max")

        return foo


    def toString2(self):
        foo = ""
        foo+= "State " + str(self.id)+"\n"
        for i in range(len(self.quantities)):
            foo += (str(self.quantities[i].name) + " " + str(self.quantities[i].value) + " " + str(
                self.quantities[i].derivative) + "\n").replace("1", "+").replace("-1", "-").replace("2", "Max")

        return foo

    def joinReasons(self):
        foo = ""
        for reason in self.reasons:
            foo += reason

        return foo