from State import State
from Relationship import Relationship
from Quantity import Quantity
from Generator import generateStates

if __name__ == "__main__":
    inflow = Quantity("Inflow", "0", "0", {"0", "+"}, True)
    volume = Quantity("Volume", "0", "0", {"0", "+", "max"}, False)
    outflow = Quantity("Outflow", "0", "0", {"0", "+", "max"}, False)
    quantities = [inflow, volume, outflow]

    R1 = Relationship(0, "+", inflow, volume)
    R2 = Relationship(0, "-", outflow, volume)
    R3 = Relationship(1, "+", volume, outflow)
    # VC(Volume(max), Outflow(max)):
    # R4 = Relationship(2, "", volume, outflow)
    # R5 = Relationship(2, "", volume, outflow)
    relationships = [R1, R2, R3]

    state = State("Initial", quantities)

    states = generateStates(state, relationships)

    # state = State("S0")
    # state.printSelf()
    # exit()


