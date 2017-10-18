from State import State
from Relationship import Relationship
from Quantity import Quantity
import Generator

if __name__ == "__main__":
    inflow = Quantity("Inflow", 0, 0, [0, 1], True)
    volume = Quantity("Volume", 0, 0, [0, 1, 2], False)
    outflow = Quantity("Outflow", 0, 0, [0, 1, 2], False)
    quantities = [inflow, volume, outflow]

    R1 = Relationship("I", 1, "Inflow", "Volume")
    R2 = Relationship("I", -1, "Outflow", "Volume")
    R3 = Relationship("P", 1, "Volume", "Outflow")
    R4 = Relationship("VC", 2, "Volume", "Outflow")
    R5 = Relationship("VC", 0, "Volume", "Outflow")


    # todo: how to represent this: VC(Volume(max), Outflow(max)) ?
    # R4 = Relationship(2, "", volume, outflow)
    # R5 = Relationship(2, "", volume, outflow)
    relationships = [R1, R2, R3, R4, R5]

    state = State("Initial", quantities)

    graph = Generator.createGraph(state, relationships)

    # state = State("S0")
    # state.printSelf()
    # exit()


