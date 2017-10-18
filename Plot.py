import graphviz as gv
import functools

def plotGraph(mygraph, end):
    graph = functools.partial(gv.Graph, format='svg')
    digraph = functools.partial(gv.Digraph, format='svg')

    myStrGraph = [list() for i in range(10000)]
    for i in range(end):
        # if len(mygraph[i]) == 1:
        #
        #     break
        for j in range(len(mygraph[i])):
            myStrGraph[i].append(mygraph[i][j].toString())

    print(myStrGraph)
    nodes = []
    edges = []

    for i in range(end):
        nodes.append((str(mygraph[i][0].id),{'label':mygraph[i][0].toString()}))
        for j in range(1,len(mygraph[i])):
            edges.append((str(mygraph[i][0].id), str(mygraph[i][j].id)))




    # for i in range(end):
    #     nodes.append(str(mygraph[i][0].id))
    #     for state in mygraph[i][1:]:
    #         edges.append((mygraph[i][0].id, state.id))

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
# =======
# graph = functools.partial(gv.Graph, format='svg')
# digraph = functools.partial(gv.Digraph, format='svg')
#
#
# g3 = graph()
# mygraph=[list(["A","A","B","C","D"]),list(["B","E","F"]),list(["C","G","H","A"])]
#
# nodes=[]
# edges=[]
#
# for stateslist in mygraph:
#     nodes.append(stateslist[0])
#     for state in stateslist[1:]:
#         edges.append((stateslist[0],state))
#
#
# def add_nodes(graph, nodes):
#     for n in nodes:
#         if isinstance(n, tuple):
#             graph.node(n[0], **n[1])
#         else:
#             graph.node(n)
#     return graph
#
# def add_edges(graph, edges):
#     for e in edges:
#         if isinstance(e[0], tuple):
#             graph.edge(*e[0], **e[1])
#         else:
#             graph.edge(*e)
#     return graph
#
#
#
#
# add_edges(add_nodes(digraph(),nodes),edges).render('img/g4')
# >>>>>>> a96e1326cee93b771ed75cba58998619080095f2
