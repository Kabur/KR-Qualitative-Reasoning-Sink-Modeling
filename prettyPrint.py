def printGraph(graph, end):
    for i in range(end + 1):
        id_array = []
        for j in range(len(graph[i])):
            id_array.append(graph[i][j].id)

        print(id_array[0], " --> ", id_array[1:])

    for i in range(end + 1):
        print(graph[i][0].toString2())


def printTrace(graph, end, filename="temp"):
    with open("out/" + filename, "w") as f:

        for i in range(end + 1):
            f.write("*" * 100 + '\n')
            parent = graph[i][0]
            f.write("From State " + str(parent.id) + '\n')
            f.write(parent.toString() + '\n')
            f.write("Following states have been generated: " + '\n')

            for j in range(1, len(graph[i])):
                child = graph[i][j]
                f.write("-" * 50 + '\n')
                f.write("State " + str(child.id) + '\n')
                f.write(child.toString() + '\n')
                for k, reason in enumerate(child.reasons[1:]):
                    f.write(child.quantities[k].name + ": " + reason + '\n')

            f.write("*" * 100 + '\n')


def createTrace(graph, end):
    for idx in range(end + 1):
        parent = graph[idx][0]

        for j in range(1, len(graph[idx])):  # only the children
            child = graph[idx][j]

            for i, Q2 in enumerate(child.quantities):
                Q1 = parent.quantities[i]

                if Q2.exogenous:
                    """ Inflow """
                    if Q2.derivative == parent.quantities[i].derivative:
                        child.reasons.append("No action was taken on the exogenous variable {}".format(Q2.name))
                    else:
                        child.reasons.append("Action was taken on the exogenous variable {}".format(Q2.name))

                elif Q2.name == "Outflow" or Q2.name == "Height" or Q2.name == "Pressure":
                    child.reasons.append(
                        "{0} is equal to Volume in derivative and magnitude because of P+(Volume, {0}) and VC(Volume("
                        "Max), {0}(Max)) and VC(Volume(0), {0}(0))".format(Q2.name))

                elif Q2.name == "Volume":
                    """ Volume """
                    # reason = "Volume: "
                    if Q1.value == 0 and Q1.derivative == 0:
                        if Q2.value == 0 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitudes of Inflow and Outflow are equal, Volume magnitude and derivative stayed "
                                "at 0")
                        if Q2.value == 0 and Q2.derivative == 1:
                            child.reasons.append(
                                "Magnitude of Inflow is greater than magnitude of Inflow, therefore the derivative "
                                "changed to +")

                    if Q1.value == 0 and Q1.derivative == 1:
                        if Q2.value == 1 and Q2.derivative == 1:
                            child.reasons.append(
                                "Magnitude was a point, derivative non-zero, therefore the magnitude changed to a "
                                "range value")

                    if Q1.value == 1 and Q1.derivative == 0:
                        if Q2.value == 1 and Q2.derivative == 1:
                            child.reasons.append(
                                "Magnitude of Inflow is greater than magnitude of Outflow, therefore derivative of "
                                "Volume changed to +")
                        if Q2.value == 1 and Q2.derivative == -1:
                            child.reasons.append(
                                "Magnitude of Inflow is lower than magnitude of Outflow, therefore derivative of "
                                "Volume changed to -")
                        if Q2.value == 1 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitudes of Inflow and Outflow stayed the same, therefore nothing changed for Volume")

                    if Q1.value == 1 and Q1.derivative == 1:
                        if Q2.value == 1 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitude of Inflow was greater than the magnitude of outflow, therefore changing "
                                "the Volume derivative from + to 0")
                        if Q2.value == 2 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitude of Volume reached Maximum, therefore the derivative automatically changed "
                                "from + to 0")
                        if Q2.value == 1 and Q2.derivative == 1:
                            child.reasons.append(
                                "Time passed, but influences of Inflow and Outflow were not such that the derivative "
                                "would change")

                    if Q1.value == 2 and Q1.derivative == -1:
                        if Q2.value == 1 and Q2.derivative == -1:
                            child.reasons.append("Magnitude of Volume dropped from point value Max to +, "
                                                 "the derivative stayed the same becuase magnitude of Outflow is "
                                                 "still greater than magnitude of Inflow")
                        if Q2.value == 1 and Q2.derivative == 0:
                            child.reasons.append("Magnitude of Volume dropped from point value Max to + and the "
                                                 "derivative changed to 0 because the magnitude of Inflow and Outflow"
                                                 " are equal")

                    if Q1.value == 2 and Q1.derivative == 0:
                        if Q2.value == 2 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitudes of Inflow and Outflow are equal, therefore the derivative of Volume "
                                "stayed the same")
                        if Q2.value == 2 and Q2.derivative == -1:
                            child.reasons.append(
                                "Magnitude of Inflow is lower than magnitude of Outflow, therefore the derivative of "
                                "VOlume decreased to -")

                    if Q1.value == 1 and Q1.derivative == -1:
                        if Q2.value == 1 and Q2.derivative == -1:
                            child.reasons.append(
                                "Time passed, but influences of Inflow and Outflow were not such that the derivative "
                                "would change")
                        if Q2.value == 1 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitude of Inflow influenced the derivative such that it changed from - to 0")
                        if Q2.value == 0 and Q2.derivative == 0:
                            child.reasons.append(
                                "Magnitude dropped to 0 because of the negative derivative in the previous state, "
                                "therefore automatically putting the derivative to 0")
