def printGraph(graph, end):
    for i in range(end + 1):
        id_array = []
        for j in range(len(graph[i])):
            id_array.append(graph[i][j].id)

        print(id_array[0], " --> ", id_array[1:])

    for i in range(end + 1):
        # print("State {}".format(graph[i][0].id))
        print(graph[i][0].toString())

    # exit()
