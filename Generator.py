import itertools
from Quantity import Quantity
from State import State


def getExogenousVars(quantities):
    exogenousArr = []
    for quantity in quantities:
        if quantity.exogenous:
            exogenousArr.append(quantity)

    return exogenousArr


def getPossibleActions(quantity):
    actions = []
    if quantity.derivative == 1:
        actions.append(0)
        actions.append(1)

    elif quantity.derivative == -1:
        actions.append(0)
        actions.append(-1)


    else:
        actions.append(0)
        actions.append(1)
        actions.append(-1)

    return actions


def isIdentical(state1, state2):
    for quantity1 in state1.quantities:
        flag = False
        for quantity2 in state2.quantities:
            if quantity1 == quantity2:
                flag = True
        if not flag:
            return False

    return True


def propagateVC(states, relationships):

    for relationship in relationships:
        if relationship.type == "VC":
            print("PROPAGATING VC")
            Q1_name = relationship.source
            Q2_name = relationship.target

            for state in states[:]:

                for quantity in state.quantities:
                    if quantity.name == Q1_name:
                        Q1 = quantity
                    if quantity.name == Q2_name:
                        Q2 = quantity

                v = relationship.sign

                if not ((Q1.value == v and Q2.value == v) or (Q1.value != v and Q2.value != v)):
                    states.remove(state)

    return states


def propagateP(states, relationships):
    print("PROPAGATING P")

    for relationship in relationships:
        if relationship.type == "P":
            Q1_name = relationship.source
            Q2_name = relationship.target

            for state in states[:]:
                for quantity in state.quantities:

                    if quantity.name == Q1_name:
                        Q1 = quantity
                    if quantity.name == Q2_name:
                        Q2 = quantity

                # P rule: derivate of source, multiply by sign of P
                if not (Q1.derivative * relationship.sign == Q2.derivative):
                    states.remove(state)

    return states


def propagateI(states, relationships):
    print("PROPAGATING I's")
    list1 = []
    relationship1 = relationships[0]
    relationship2 = relationships[1]

    Q1_source_name = relationship1.source
    Q2_source_name = relationship2.source
    Q3_target_name = relationship1.target

    for state in states[:]:
        for quantity in state.quantities:
            if quantity.name == Q1_source_name:
                Q1_source = quantity
            if quantity.name == Q2_source_name:
                Q2_source = quantity
            if quantity.name == Q3_target_name:
                Q3_target = quantity

        a = Q1_source.value * relationship1.sign
        b = Q2_source.value * relationship2.sign
        c = Q3_target.derivative


        # if a > 0 and a < b then c can be anything
        if a > 0 and b >= 0:
            if not c > 0:
                states.remove(state)
        if a < 0 and b <= 0:
            if not c < 0:
                states.remove(state)
        if a == 0:
            if b > 0:
                if not c > 0:
                    states.remove(state)
            if b == 0:
                if not c == 0:
                    states.remove(state)
            if b < 0:
                if not c < 0:
                    states.remove(state)

    return states

def generateStates(state, relationships):
    """"""
    """1. resolve time: update the values given the derivatives in every possible combination"""
    """2. For every value combination, take all possible combinations of derivatives -> pu them in states """
    """3. Check all states with all relationships and discard those that are invalid """
    N = len(state.quantities)  # for our case it's always 3
    combinations = [list() for i in range(N)]

    for i, quantity in enumerate(state.quantities):
        if quantity.derivative == 0:
            if quantity.value == 0:
                combinations[i].append(Quantity(quantity.name, 0, 0, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 0, 1, quantity.range, quantity.exogenous))
            if quantity.value == 1:
                combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 1, 1, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 1, -1, quantity.range, quantity.exogenous))

            # if not quantity.exogenous:
            if 2 in quantity.range:
                if quantity.value == 2:
                    combinations[i].append(Quantity(quantity.name, 2, 0, quantity.range, quantity.exogenous))
                    combinations[i].append(Quantity(quantity.name, 2, -1, quantity.range, quantity.exogenous))

        elif quantity.derivative == -1:
            if quantity.value == 1:
                combinations[i].append(Quantity(quantity.name, 1, -1, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 0, 0, quantity.range, quantity.exogenous))

            # if not quantity.exogenous:
            if 2 in quantity.range:
                if quantity.value == 2:
                    combinations[i].append(Quantity(quantity.name, 2, -1, quantity.range, quantity.exogenous))
                    combinations[i].append(Quantity(quantity.name, 1, -1, quantity.range, quantity.exogenous))
                    combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))

        elif quantity.derivative == 1:
            if quantity.value == 0:
                combinations[i].append(Quantity(quantity.name, 1, 1, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))
            if quantity.value == 1:
                combinations[i].append(Quantity(quantity.name, 1, 1, quantity.range, quantity.exogenous))
                combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))
                # if not quantity.exogenous:
                if 2 in quantity.range:
                    combinations[i].append(Quantity(quantity.name, 2, 0, quantity.range, quantity.exogenous))

    states = []
    """ Get all permutations of states """
    permutations = list(itertools.product(*combinations))
    for permutation in permutations:
        state = State("", permutation)
        states.append(state)
        # state.printSelf()

    """ Check each state with all the relationships, add to the list if valid """
    states = propagateVC(states, relationships)
    states = propagateP(states, relationships)
    states = propagateI(states, relationships)

    return states


# def checkState(state):
#     """ True if the state does not include [0 +] or [Max -] in any quantity """
#     for quantity in state.quantities:
#         if quantity.value == 0 and quantity.derivative == 1:
#             return False
#         if quantity.value == 2 and quantity.derivative == -1:
#             return False
#
#     return True
#
# def takeActions():
#     pass

def createGraph(initialState, relationships):
    N = 100
    end = 1
    graph = [list() for i in range(N)]
    graph[0].append(initialState)
    i = 0
    while 1:

        currentState = graph[i][0]
        freshStates1 = []
        freshStates2 = []
        freshStates3 = []

        """ test scenario1 """
        # inflow = Quantity("Inflow", 1, -1, [0, 1], True)
        # volume = Quantity("Volume", 1, 1, [0, 1, 2], False)
        # outflow = Quantity("Outflow", 1, 1, [0, 1, 2], False)
        """ test scenario2 """
        inflow = Quantity("Inflow", 0, 1, [0, 1], True)
        volume = Quantity("Volume", 0, 0, [0, 1, 2], False)
        outflow = Quantity("Outflow", 0, 0, [0, 1, 2], False)
        quantities = [inflow, volume, outflow]

        currentState = State("test", quantities)
        freshStates1 = generateStates(currentState, relationships)

        print("Fresh States: ")
        for state in freshStates1:
            state.printSelf()
        exit()

        # # flatten
        # freshStates3 = [j for i in freshStates3 for j in i]

        """ add the freshstates as the currentState's neighbours
            and add each fresh state to the graph if it wasn't expanded yet """
        for state in freshStates1:
            graph[i].append(state)
            for j in range(i):
                if not isIdentical(graph[j][0], state):
                    graph[end].append(state)
                    end += 1

        i += 1

        #todo: break this loop at some point xD
        #todo: test plotting
        #todo: test on more scenarios (or just plot and verify the plotted graph)

    return graph
