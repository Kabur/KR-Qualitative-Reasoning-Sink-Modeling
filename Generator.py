import itertools
from Quantity import Quantity
from State import State


def isIdentical(state1, state2):
    for i, Q1 in enumerate(state1.quantities):
        if not (Q1.value == state2.quantities[i].value and Q1.derivative == state2.quantities[i].derivative):
            return False

    return True


def propagateVC(states, relationships):
    for relationship in relationships:
        if relationship.type == "VC":
            # print("PROPAGATING VC")
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
    # print("PROPAGATING P")

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
    # print("PROPAGATING I's")
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
                """ removed because value is going from point to range value -> cannot take an action inbetween """
                # combinations[i].append(Quantity(quantity.name, 1, 0, quantity.range, quantity.exogenous))
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

def takeActions(state):
    states1=[]
    states2=[]
    for quantity in state.quantities:

        if quantity.exogenous:
            if quantity.derivative == -1:
                # tempQuantities = state.quantities
                # tempQuantities
                states1.append(State("meh",Quantity("name",quantity.value,0,quantity.range,True)))
                states2.append(State("meh",Quantity("name",quantity.value,quantity.derivative,quantity.range,True)))
            elif quantity.derivative==0:
                states1.append(State("meh", Quantity("name", quantity.value, -1, quantity.range, True)))
                states2.append(State("meh", Quantity("name", quantity.value, 1, quantity.range, True)))
            elif quantity.derivative==1:
                states1.append(State("meh", Quantity("name", quantity.value, 0, quantity.range, True)))
                states2.append(State("meh",Quantity("name",quantity.value,quantity.derivative,quantity.range,True)))

        else:
            states1.append(State("meh", Quantity("name", quantity.value, quantity.derivative, quantity.range, True)))
            states2.append(State("meh", Quantity("name", quantity.value, quantity.derivative, quantity.range, True)))
    return [states1,states2]


def createGraph(initialState, relationships):
    N = 100
    end = 0
    graph = [list() for i in range(N)]
    graph[0].append(initialState)
    i = 0
    id = initialState.id

    while 1:
        currentState = graph[i][0]

        freshStates = generateStates(currentState, relationships)

        for state in freshStates:
            graph[i].append(state)
            identical = False

            for j in range(end + 1):
                if isIdentical(graph[j][0], state):
                    print("-" * 150, " found identical")
                    state.id = graph[j][0].id
                    identical = True
                    break
            if identical is False:
                end += 1  # end is initialized as 0
                id += 1
                state.id = id
                graph[end].append(state)


        if i == end:
            break

        i += 1

    return graph, end
