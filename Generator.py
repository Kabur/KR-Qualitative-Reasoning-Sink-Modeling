def getExogenousVars(quantities):
    exogenousArr = []
    for quantity in quantities:
        if quantity.exogenous:
            exogenousArr.append(quantity)

    return exogenousArr


def getPossibleActions(quantity):
    actions = []
    if quantity.derivative == "+":
        actions.append("0")
        actions.append("+")

    elif quantity.derivative == "-":
        actions.append("0")
        actions.append("-")

    else:
        actions.append("0")
        actions.append("+")
        actions.append("-")

    return actions


def isIdentical(state1, state2):
    # todo: this

    return True

def propagateI(relationship, graph):

    if relationship.sign == "+":
        # take Q1 value
        # check sign
        # depending on sign of relation, update Q2 derivate

        """ check if the state already exists in graph """
        for item in graph:
            if isIdentical(state, item):
                found = True
                break # todo: what to do after the break

        # newVolume =


def propagateP(relationship, graph)
    pass


def generateStates(currentState, relationships):
    graph = []
    graph.append(currentState)
    # graph[0].append(neighbourState)

    """ repeat until no more states can be produced """
    while(1):
        exoVars = getExogenousVars(currentState.quantities)

        # there is only 1: Inflow
        for exoVar in exoVars:
            actions = getPossibleActions(exoVar)

            """ Take every possible action"""
            for action in actions:

                """ How that action propagates through other quantities"""
                for relationship in relationships:
                    states = propagateI(relationship, graph)




