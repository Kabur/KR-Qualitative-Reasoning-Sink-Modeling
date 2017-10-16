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


def generateStates(quantities, relationships):

    exoVars = getExogenousVars(quantities)

    # there is only 1: Inflow
    for exoVar in exoVars:
        actions = getPossibleActions(exoVar)

        for action in actions:
            for relationship in relationships:



