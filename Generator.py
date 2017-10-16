
def getExogenousVars(quantities):
    exogenousArr=[]
    for quantity in quantities:
        if quantity.exogenous:
            exogenousArr.append(quantity)

    return exogenousArr


def findPossibleActions(quantity):
    actions=[]
    if quantity.derivative=="+":

        actions.append("0")
        actions.append("+")
    elif quantity.derivative=="-":
        actions.append("0")
        actions.append("-")
    else:
        actions.append("0")
        actions.append("+")
        actions.append("-")

    return actions




class Generator:
    def genNextState(self,currState):

        # exo = getExogenousVars()
        # for exogenous in exo:
        #     actions = findPossibleActions()
        #
        # for action in actions:
        #
        quantities=currState.quantities
        for quantity in quantities:
            if quantity.exogenous==True:
                actions=findPossibleActions(quantity)

                newStates = []
                for action in actions:
                    newStates.append(currState,action)







