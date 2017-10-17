import graphviz as gv
import functools
graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')


g3 = graph()
mygraph=[list(["A","A","B","C","D"]),list(["B","E","F"]),list(["C","G","H","A"])]

nodes=[]
edges=[]

for stateslist in mygraph:
    nodes.append(stateslist[0])
    for state in stateslist[1:]:
        edges.append((stateslist[0],state))


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




add_edges(add_nodes(digraph(),nodes),edges).render('img/g4')