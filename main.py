from State import State
from Relationship import Relationship
from Quantity import Quantity
from Generator import generateStates

if __name__ == "__main__":
    inflow = Quantity("Inflow", "0", "0", {"0", "+"}, True)
    volume = Quantity("Volume", "0", "0", {"0", "+", "max"}, False)
    outflow = Quantity("Outflow", "0", "0", {"0", "+", "max"}, False)
    quantities = [inflow, volume, outflow]

    relationship1 = Relationship(0, "+", inflow, volume)
    relationships = [relationship1]

    state = State("Initial", quantities)

    states = generateStates(state, relationships)

    # state = State("S0")
    # state.printSelf()
    # exit()


