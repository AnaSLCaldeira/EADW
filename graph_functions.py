import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    #G=nx.Graph()
    G=nx.cubical_graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    #pos = nx.shell_layout(G)
    #pos = nx.spectral_layout(G)
    #pos = nx.random_layout(G) # Funciona melhor
    #pos = nx.circular_layout(G) # Mais ou menos
    pos = nx.fruchterman_reingold_layout(G) # Funciona melhor

    nx.draw(G, pos)
    #nx.draw_networkx(G, pos)

    # show graph
    plt.axis('off')
    plt.show()
