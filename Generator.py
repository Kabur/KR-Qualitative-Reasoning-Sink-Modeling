from Quantity import Quantity
import State


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


# class Generator:
#     def genNextState(self, currState):
#
#         # exo = getExogenousVars()
#         # for exogenous in exo:
#         #     actions = findPossibleActions()
#         #
#         # for action in actions:
#         #
#         quantities = currState.quantities
#         for quantity in quantities:
#             if quantity.exogenous == True:
#                 actions = getPossibleActions(quantity)
#
#                 newStates = []
#                 for action in actions:
#                     newStates.append(currState, action)


def isIdentical(state1, state2):
    print(state1)

    # if len(state1)==0 or len(state2)==0:
    #     return False
    for quantity1 in state1.quantities:
        flag = False
        for quantity2 in state2.quantities:
            if quantity1 == quantity2:
                flag = True
        if not flag:
            return False

    return True


def propagateI(relationship, currentState):
    # take Q1 value
    # check sign
    # depending on sign of relation, update Q2 derivate

    source = relationship.source
    currStateQuantities = currentState.quantities
    for quantity in currStateQuantities:
        if quantity.name == source:
            value = quantity.value
    target = relationship.target

    NewQuantities = []
    for quantity in currStateQuantities:

        if quantity.name == target:
            newDerivative = relationship.sign * value
            NewQuantities.append(
                Quantity(quantity.name, quantity.value, newDerivative, quantity.range, quantity.exogenous))

        else:
            NewQuantities.append(
                Quantity(quantity.name, quantity.value, quantity.derivative, quantity.range, quantity.exogenous))

    NewState = State("blah", NewQuantities)
    return NewState


def propagateP(relationship, currentState):
    # take Q1 value
    # check sign
    # depending on sign of relation, update Q2 derivate

    source = relationship.source
    currStateQuantities = currentState.quantities
    for quantity in currStateQuantities:
        if quantity.name == source:
            value = quantity.derivative
    target = relationship.target

    NewQuantities = []
    for quantity in currStateQuantities:

        if quantity.name == target:
            if value == 2:
                value = 1
            elif value == -1:
                value = -1
            newDerivative = relationship.sign * value

            NewQuantities.append(
                Quantity(quantity.name, quantity.value, newDerivative, quantity.range, quantity.exogenous))

        else:
            NewQuantities.append(
                Quantity(quantity.name, quantity.value, quantity.derivative, quantity.range, quantity.exogenous))

    NewState = State("blah", NewQuantities)
    return NewState
    #
    # """ check if the state already exists in graph """
    # for item in graph:
    #     if isIdentical(state, item):
    #         found = True
    #         break

    # newVolume =


def propagateVC(relationship, currentState):
    # take Q1 value
    # check sign
    # depending on sign of relation, update Q2 derivate

    source = relationship.source
    currStateQuantities = currentState.quantities
    for quantity in currStateQuantities:
        if quantity.name == source:
            value = quantity.value
    target = relationship.target

    NewQuantities = []
    for quantity in currStateQuantities:

        if quantity.name == target:
            newvalue = value
            NewQuantities.append(
                Quantity(quantity.name, newvalue, quantity.derivative, quantity.range, quantity.exogenous))

        else:
            NewQuantities.append(
                Quantity(quantity.name, quantity.value, quantity.derivative, quantity.range, quantity.exogenous))

    NewState = State("blah", NewQuantities)
    return NewState


def propagateRelationships(state, relationships):
    states = []
    for relationship in relationships:
        if relationship.type == "I":
            states = propagateI(relationship, state)
        elif relationship.type == "P":
            states = propagateP(relationship, state)
        elif relationship.type == "VC":
            states = propagateVC(relationship, state)
        states.append(state)
    return states


def propagateTime(state):
    ''' so here we need the time to pass to generate some states from the current state'''
    newQuantities = []
    states = [[], [], []]

    for quantity in state.quantities:
        if quantity.derivative == 1:
            # if quantity.value==2: #if value is max 2=max
            #     states[0].append(Quantity(quantity.name, 2, quantity.derivative, quantity.range, quantity.exogenous))
            if quantity.value == 1:
                states[0].append(Quantity(quantity.name, 2, 0, quantity.range, quantity.exogenous))
                states[1].append(Quantity(quantity.name, 1, quantity.derivative, quantity.range, quantity.exogenous))
            elif quantity.value == 0:
                states[0].append(Quantity(quantity.name, 1, quantity.derivative, quantity.range, quantity.exogenous))

        elif quantity.derivative == -1:
            if quantity.value == 2:  # if value is max 2=max
                states[0].append(
                    Quantity(quantity.name, 1, quantity.derivative, quantity.range, quantity.exogenous))
            elif quantity.value == 1:
                states[0].append(
                    Quantity(quantity.name, 0, 0, quantity.range, quantity.exogenous))
                states[1].append(
                    Quantity(quantity.name, 1, quantity.derivative, quantity.range, quantity.exogenous))
                # elif quantity.value == 0:
                #     states[0].append(
                #         Quantity(quantity.name, 0, quantity.derivative, quantity.range, quantity.exogenous))

        elif quantity.derivative == 0:
            if quantity.value == 2:  # if value is max 2=max
                states[0].append(
                    Quantity(quantity.name, 2, quantity.derivative, quantity.range, quantity.exogenous))
            elif quantity.value == 1:
                states[0].append(
                    Quantity(quantity.name, 1, quantity.derivative, quantity.range, quantity.exogenous))
            elif quantity.value == 0:
                states[0].append(
                    Quantity(quantity.name, 0, quantity.derivative, quantity.range, quantity.exogenous))

    return states


# def findUnexpanded(graph):
#     for i in range(len(graph)):
#         if len(graph[i]) == 1:
#             return i
#     return -10


# def createFuturestates(graph):
#     statesToAppend = []
#
#     for potentialState in graph[0]:
#         flag = False
#         for motherState in graph[0:]:
#             if isIdentical(potentialState, motherState):
#                 flag = True
#         if flag == False:
#             statesToAppend.append(potentialState)
#     for state in statesToAppend:
#         graph.append(state)
#     return graph


def checkState(state):
    """ True if the state does not include [0 +] or [Max -] in any quantity """
    for quantity in state.quantities:
        if quantity.value == 0 and quantity.derivative == 1:
            return False
        if quantity.value == 2 and quantity.derivative == -1:
            return False

    return True


def generateStates(initialState, relationships):
    """
    1. Prop time 
    2. Take immediate actions 
        - if the current state has [0 +] or [Max -] -> DON'T take immediate actions
    3. Take actions after time prop
    
    Propagate the relationships for every new state
    """
    N = 100
    end = 1
    graph = [list() for i in range(N)]
    graph[0].append(initialState)
    print(graph)
    exit()
    i = 0

    while 1:
        currentState = graph[i][0]
        freshStates1 = []
        freshStates2 = []
        freshStates3 = []

        # todo: THIS NEEDS TO RETURN LIST OF STATES
        #todo: each of these 3 need to propagate the relationships as well
        freshStates1 = propagateTime(currentState)

        if checkState(currentState):
            freshStates2 = takeActions(currentState)

        for state in freshStates1:
            freshStates3.append(takeActions(state))

        # flatten
        freshStates3 = [j for i in freshStates3 for j in i]


        """ add the freshstates as the currentState's neighbours
            and add each fresh state to the graph if it wasn't expanded yet """
        for state in freshStates1:
            graph[i].append(state)
            for j in range(i):
                if not isIdentical(graph[j][0], state):
                    graph[i + end].append(state)
                    end += 1

        for state in freshStates2:
            graph[i].append(state)
            for j in range(i):
                if not isIdentical(graph[j][0], state):
                    graph[i + end].append(state)
                    end += 1

        for state in freshStates3:
            graph[i].append(state)
            for j in range(i):
                if not isIdentical(graph[j][0], state):
                    graph[i + end].append(state)
                    end += 1

        i += 1

        # while 1:
        #     # i = findUnexpanded(graph)
        #     # if i == -10:
        #     #     break
        #
        #     graph[i].append(expandStateRelations(currentState, relationships))
        #
        #     '''let some time pass so we generate consequence states'''
        #     freshStates = letTimePass(currentState)
        #     print("f", freshStates)
        #     for state in freshStates:
        #
        #         if len(state) != 0:
        #             for freshState in state:
        #                 flag = False
        #                 for state in graph:
        #                     if isIdentical(freshState, state):
        #                         flag = True
        #                 if not flag:
        #                     graph[i].append(freshState)
        #
        #             graph = createFuturestates(graph)
        #
        #     print(graph)
        #     i += 1

        #
        # '''expand anexpanded nodes'''
        # while (1):
        #
        #
        #
        #
        # """ repeat until no more states can be produced """
        # while(1):
        #     exoVars = getExogenousVars(currentState.quantities)
        #
        #     # there is only 1: Inflow
        #     for exoVar in exoVars:
        #         actions = getPossibleActions(exoVar)
        #
        #
        #
        #
        #
        #
        #         """ Take every possible action"""
        #         for action in actions:
        #
        #             """ How that action propagates through other quantities"""
        #             for relationship in relationships:
        #                 if relationship.type=="I":
        #                     states = propagateI(relationship, currentState)
        #                 elif relationship.type=="P":
        #                     states = propagateP(relationship, currentState)
        #                 elif relationship.type == "VC":
        #                     states = propagateVC(relationship, currentState)
        #
        #                 graph[-1].append(states)
        #
