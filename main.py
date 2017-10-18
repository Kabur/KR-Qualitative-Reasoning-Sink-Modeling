from Plot import plotGraph
import prettyPrint
from State import State
from Relationship import Relationship
from Quantity import Quantity
import Generator

if __name__ == "__main__":
    """ test scenario1 """
    # inflow = Quantity("Inflow", 1, -1, [0, 1], True)
    # volume = Quantity("Volume", 1, 1, [0, 1, 2], False)
    # outflow = Quantity("Outflow", 1, 1, [0, 1, 2], False)
    """ test scenario2 """
    inflow = Quantity("Inflow", 0, 0, [0, 1], True)
    volume = Quantity("Volume", 0, 0, [0, 1, 2], False)
    outflow = Quantity("Outflow", 0, 0, [0, 1, 2], False)
    quantities = [inflow, volume, outflow]
    initialState = State(0, quantities)

    R1 = Relationship("I", 1, "Inflow", "Volume")
    R2 = Relationship("I", -1, "Outflow", "Volume")
    R3 = Relationship("P", 1, "Volume", "Outflow")
    R4 = Relationship("VC", 2, "Volume", "Outflow")
    R5 = Relationship("VC", 0, "Volume", "Outflow")

    relationships = [R1, R2, R3, R4, R5]

    graph, end = Generator.createGraph(initialState, relationships)

    plotGraph(graph, end)

    # prettyPrint.printGraph(graph)


