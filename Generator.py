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


def propagateI(states, relationships, parentState):
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

        """ attempt at QR calculus """
        # if a > 0 and a < b then c can be anything
        if a > 0 and b >= 0:
            if not c > 0:
                states.remove(state)
                continue
        if a < 0 and b <= 0:
            if not c < 0:
                states.remove(state)
                continue
        if a == 0:
            if b > 0:
                if not c > 0:
                    states.remove(state)
                    continue
            if b == 0:
                if not c == 0:
                    states.remove(state)
                    continue
            if b < 0:
                if not c < 0:
                    states.remove(state)
                    continue

        """ Here comes the heavy hardcoding... I'm sorry it had to be done >{ """
        """ if the parent state is in equilibrium """

        if parentState.quantities[1].derivative == 0:
            if parentState.quantities[0].derivative == 1 and Q3_target.value != 2:
                if c != 1:
                    states.remove(state)
                    continue
            elif parentState.quantities[0].derivative == 1 and Q3_target.value == 2:
                if c != 0:
                    states.remove(state)
                    continue

            if parentState.quantities[0].derivative == 0:
                if c != 0:
                    states.remove(state)
                    continue

            if parentState.quantities[0].derivative == -1 and Q3_target.value != 2:
                if c != -1:
                    states.remove(state)
                    continue
            elif parentState.quantities[0].derivative == -1 and Q3_target.value == 2:
                if c != 0 and c != -1:
                    states.remove(state)
                    continue

    return states


def propagateConstraint(states, parentState):
    """ the constraint: when transitioning from point to range value in any quantity, action cannot be taken """
    apply = False

    # check if we need to apply the constraint at all
    for Q in parentState.quantities:
        if (Q.value == 0 and Q.derivative == 1) or (Q.value == 2 and Q.derivative == -1):
            apply = True

    if apply is True:
        for state in states[:]:
            for i, Q in enumerate(state.quantities):
                # We can only take action on exo variables
                if Q.exogenous:
                    # if the derivative of the exo quantity changed(==we took an action), remove the state
                    if Q.derivative != parentState.quantities[i].derivative:
                        states.remove(state)

    return states, apply


def generateStates(state, relationships):
    """ Generates children states for a state """
    """1. resolve time: update the values given the derivatives in every possible combination"""
    """2. For every value combination, take all possible combinations of derivatives -> pu them in states """
    """3. Check all states with all relationships and discard those that are invalid """

    N = len(state.quantities)  # for our case it's always 3
    combinations = [list() for i in range(N)]
    reason = ""
    for i, Q in enumerate(state.quantities):
        if Q.derivative == 0:
            if Q.value == 0:
                combinations[i].append(Quantity(Q.name, 0, 0, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 0, 1, Q.range, Q.exogenous, reason))
            if Q.value == 1:
                combinations[i].append(Quantity(Q.name, 1, 0, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 1, 1, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 1, -1, Q.range, Q.exogenous, reason))

            if 2 in Q.range:
                if Q.value == 2:
                    combinations[i].append(Quantity(Q.name, 2, 0, Q.range, Q.exogenous, reason))
                    combinations[i].append(Quantity(Q.name, 2, -1, Q.range, Q.exogenous, reason))

        elif Q.derivative == -1:
            if Q.value == 1:
                combinations[i].append(Quantity(Q.name, 1, -1, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 1, 0, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 0, 0, Q.range, Q.exogenous, reason))

            if 2 in Q.range:
                if Q.value == 2:
                    # """ removed because point magnitude has to change if there is a derivative """
                    # combinations[i].append(Quantity(Q.name, 2, -1, Q.range, Q.exogenous, reason))
                    combinations[i].append(Quantity(Q.name, 1, -1, Q.range, Q.exogenous, reason))
                    # """ also removed, I dont even know why anymore but it should not happen """
                    # combinations[i].append(Quantity(Q.name, 1, 0, Q.range, Q.exogenous, reason))

        elif Q.derivative == 1:
            if Q.value == 0:
                combinations[i].append(Quantity(Q.name, 1, 1, Q.range, Q.exogenous, reason))
                # """ removed because value is going from point to range value -> cannot take an action inbetween """
                # combinations[i].append(Quantity(Q.name, 1, 0, Q.range, Q.exogenous))
            if Q.value == 1:
                combinations[i].append(Quantity(Q.name, 1, 1, Q.range, Q.exogenous, reason))
                combinations[i].append(Quantity(Q.name, 1, 0, Q.range, Q.exogenous, reason))
                if 2 in Q.range:
                    combinations[i].append(Quantity(Q.name, 2, 0, Q.range, Q.exogenous, reason))

    states = []
    """ Get all permutations of states """
    permutations = list(itertools.product(*combinations))
    for permutation in permutations:
        tempState = State(-1, permutation)
        states.append(tempState)

    """ Check each state with all the relationships, add to the list if valid """
    states = propagateVC(states, relationships)
    states = propagateP(states, relationships)
    states = propagateI(states, relationships, state)
    states, _ = propagateConstraint(states, state)

    return states


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
