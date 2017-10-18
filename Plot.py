import graphviz as gv
import functools

def plotGraph(mygraph,end):
    graph = functools.partial(gv.Graph, format='svg')
    digraph = functools.partial(gv.Digraph, format='svg')

    myStrGraph= [list() for i in range(10000)]
    for i in range(end):
        if len(mygraph[i])==1:
            break
        for j in  range(len(mygraph[i])):
            myStrGraph[i].append(mygraph[i][j].toString())

    print(myStrGraph)
    nodes=[]
    edges=[]
    mygraph
    for i in range(end):
        nodes.append(mygraph[i][0])
        for state in mygraph[i][1:]:
            edges.append((mygraph[i][0],state))


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