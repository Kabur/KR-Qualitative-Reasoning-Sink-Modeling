import graphviz as gv
import functools


def findStateReasons(graph,end):
    for i in range(end + 1):
        for j in range(1, len(graph[i])):
            isOnlyTime=True
            for quantity in graph[i][j].quantities:
                if quantity.resultOf=="t+a":
                    isOnlyTime=False

            if isOnlyTime:
                graph[i][j].resultOf="T"
            else:
                graph[i][j].resultOf="T+A"


def plotGraph(mygraph, end):
    graph = functools.partial(gv.Graph, format='svg')
    digraph = functools.partial(gv.Digraph, format='svg')

    myStrGraph = [list() for i in range(10000)]
    for i in range(end + 1):
        for j in range(len(mygraph[i])):
            myStrGraph[i].append(mygraph[i][j].toString())

    # print(myStrGraph)
    nodes = []
    edges = []
    findStateReasons(mygraph,end)
    for i in range(end + 1):
        nodes.append((str(mygraph[i][0].id), {'label': mygraph[i][0].toString()}))
        for j in range(1, len(mygraph[i])):
            edges.append(((str(mygraph[i][0].id), str(mygraph[i][j].id)),{'label':mygraph[i][j].resultOf}))

    def add_nodes(graph, nodes):
        for n in nodes:
            if isinstance(n, tuple):
                graph.node(n[0], **n[1])
            else:
                graph.node(n)
        return graph

    def add_edges(graph, edges):
        for e in edges:
            if isinstance(e[0], tuple):
                graph.edge(*e[0], **e[1])
            else:
                graph.edge(*e)
        return graph

    add_edges(add_nodes(digraph(), nodes), edges).render('img/g4')
