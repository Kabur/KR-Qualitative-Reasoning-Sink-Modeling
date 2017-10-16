
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

    exo=getExogenousVars()
    for exogenous in exo:
        actions=findPossibleActions()





