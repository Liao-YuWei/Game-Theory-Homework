import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

#add random node weight to the WS model
def add_node_weight(G):
    weights = {}
    for i in range(30):
        weights[i] = random.randint(1,10)
    nx.set_node_attributes(G, weights, name='weight')

    return weights

#calculate prioity for each node 
def calculate_node_priority(G):
    priorities = {}
    for i in range(30):
        neighors_weight = 0
        for neighbor in G.neighbors(i):
            neighors_weight += G.nodes[neighbor]['weight']
        priorities[i] = G.nodes[i]['weight'] / (G.nodes[i]['weight'] + neighors_weight)
    nx.set_node_attributes(G, priorities, name='priority')

    return priorities

#randomly initialize independent set
def initialize_independent_set(G):
    set = {}
    for i in range(30):
        set[i] = random.randint(0,1)
    nx.set_node_attributes(G, set, name='independent_set')

    return set

#print graph
def print_graph(G):
    labels = {n: str(n) + ': ' + str(G.nodes[n]['weight']) for n in G.nodes}
    pos = nx.circular_layout(G)
    plt.figure(figsize = (6, 6))
    nx.draw_networkx(G, pos, labels = labels)
    plt.show()

    return

#create watts_strogatz model with 30 nodes, 4 links for each node initially
G = nx.watts_strogatz_graph(n = 30, k = 4, p = 0.5)
adjacency = nx.to_numpy_array(G)
node_weight = add_node_weight(G)
node_priority = calculate_node_priority(G)
independent_set = initialize_independent_set(G)


#print_graph(G)