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
    inflow = Quantity("Inflow", 0, 0, [0, 1], True, "G")
    volume = Quantity("Volume", 0, 0, [0, 1, 2], False, "G")
    outflow = Quantity("Outflow", 0, 0, [0, 1, 2], False, "G")
    pressure = Quantity("Pressure", 0, 0, [0, 1, 2], False, "G")
    height = Quantity("Height", 0, 0, [0, 1, 2], False, "G")

    quantities = [inflow, volume, outflow]
    extendedQuantities = [inflow, volume, outflow, pressure, height]

    initialState = State(0, quantities)
    extendedInitialState = State(0, extendedQuantities)

    R1 = Relationship("I", 1, "Inflow", "Volume")
    R2 = Relationship("I", -1, "Outflow", "Volume")
    R3 = Relationship("P", 1, "Volume", "Outflow")
    R4 = Relationship("VC", 2, "Volume", "Outflow")
    R5 = Relationship("VC", 0, "Volume", "Outflow")

    E1 = Relationship("P", 1, "Volume", "Pressure")
    E2 = Relationship("P", 1, "Volume", "Height")
    E3 = Relationship("VC", 2, "Volume", "Pressure")
    E4 = Relationship("VC", 0, "Volume", "Pressure")
    E5 = Relationship("VC", 2, "Volume", "Height")
    E6 = Relationship("VC", 0, "Volume", "Height")

    relationships = [R1, R2, R3, R4, R5]
    extendedRelationships = [R1, R2, R3, R4, R5, E1, E2, E3, E4, E5, E6]

    graph, end = Generator.createGraph(initialState, relationships)
    graph2, end2 = Generator.createGraph(extendedInitialState, extendedRelationships)

    prettyPrint.printGraph(graph, end, "graph_basic.txt")
    prettyPrint.createTrace(graph, end)
    prettyPrint.printTrace(graph, end, "trace_basic.txt")

    prettyPrint.printGraph(graph2, end2, "graph_extended.txt")
    prettyPrint.createTrace(graph2, end2)
    prettyPrint.printTrace(graph2, end2, "trace_extended.txt")

    plotGraph(graph, end, "graph_basic")
    plotGraph(graph2, end2, "graph_extended")

    # prettyPrint.printGraph(graph)
