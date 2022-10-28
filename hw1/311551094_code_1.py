#from logging.handlers import WatchedFileHandler
#from operator import truediv
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#add random node weight to the WS model
def add_node_weight(G, node_num):
    weights = {}
    for node in range(node_num):
        weights[node] = random.randint(0,node_num-1)
    nx.set_node_attributes(G, weights, name='weight')

    return weights

#calculate prioity for each node 
def calculate_node_priority(G, node_num):
    priorities = {}
    for node in range(node_num):
        neighors_weight = G.nodes[node]['weight']
        for neighbor in G.neighbors(node):
            neighors_weight += G.nodes[neighbor]['weight']
        if neighors_weight != 0:
            priorities[node] = G.nodes[node]['weight'] / neighors_weight
        else:
            priorities[node] = 0
    nx.set_node_attributes(G, priorities, name='priority')

    return priorities

#randomly initialize strategy profile
def initialize_strategy_profile(G, node_num):
    profile = {}
    for node in range(node_num):
        profile[node] = random.randint(0,1)
    nx.set_node_attributes(G, profile, name='strategy')

    return profile

#find node set that its strategy is not best response in weighted MIS, store node as key, best response as value
def find_waiting_node_MIS(G, node_num):
    waiting_nodes = {}
    for node in range(node_num):
        priority = G.nodes[node]['priority']
        strategy = G.nodes[node]['strategy']
        best_response = 1
        for neighbor in G.neighbors(node):
            if G.nodes[neighbor]['priority'] > priority and G.nodes[neighbor]['strategy'] == 1:
                best_response = 0
                break
        if strategy != best_response:
            waiting_nodes[node] = best_response
    
    return waiting_nodes

#calculate total weight of selected nodes in MIS
def calculate_total_weight(G, node_num):
    total_weight = 0
    for node in range(node_num):
        if G.nodes[node]['strategy'] == 1:
            total_weight += G.nodes[node]['weight']

    return total_weight

def find_waiting_node_MDS_based_IDS(G, node_num):
    waiting_nodes = {}
    for node in range(node_num):
        strategy = G.nodes[node]['strategy']
        best_response = 1
        
        #check dominate
        dominate_condition = 1
        vj = 0
        for neighbor_node in G.neighbors(node):
           vj += G.nodes[neighbor_node]['strategy']

        if vj == 0:
            dominate_condition = 0
        else:
            for neighbor_node in G.neighbors(node):
                vj = 0
                for neighbor_p in G.neighbors(neighbor_node):
                    vj += G.nodes[neighbor_p]['strategy']
                if vj == 0:
                    dominate_condition = 0
                    break
        
        #check independence
        independence_condition = 0
        for neighbor_node in G.neighbors(node):
           if G.nodes[neighbor_node]['strategy'] == 1:
                independence_condition = 1
                break
        
        #best response
        if dominate_condition or independence_condition:
            best_response = 0

        if strategy != best_response:
            waiting_nodes[node] = best_response
    
    return waiting_nodes

def calculate_cardinality(G, node_num):
    total_node = 0
    for node in range(node_num):
        if G.nodes[node]['strategy'] == 1:
            total_node += 1

    return total_node

#print weighted MIS graph
def print_graph_MIS(G):
    label = {n: str(n) + ': ' + str(G.nodes[n]['weight']) for n in G.nodes}
    color = [G.nodes[n]['strategy'] for n in G.nodes]
    cmap = colors.ListedColormap(['g','r'])
    pos = nx.circular_layout(G)
    plt.figure(figsize = (7.5, 7.5))
    nx.draw_networkx(G, pos, labels = label, node_color = color, cmap = cmap)
    plt.show()

    return

#print symmetric MDS-based IDS graph
def print_graph_MDS_based_IDS(G):
    color = [G.nodes[n]['strategy'] for n in G.nodes]
    cmap = colors.ListedColormap(['g','r'])
    pos = nx.circular_layout(G)
    plt.figure(figsize = (7.5, 7.5))
    nx.draw_networkx(G, pos, node_color = color, cmap = cmap)
    plt.show()

    return

NODE_NUM = 30
LINK_NUM = 4

probability = [p*0.2 for p in range(5)]

"""
hw1-1
Weighted MIS Game
"""
average_move_count = np.zeros(5)
average_total_weight = np.zeros(5)

for p in range(5):
    for i in range(100):
        #create watts_strogatz model with 30 nodes, 4 links for each node initially
        G = nx.watts_strogatz_graph(n = NODE_NUM, k = LINK_NUM, p = probability[p])
        adjacency = nx.to_numpy_array(G)
        node_weight = add_node_weight(G, NODE_NUM)
        node_priority = calculate_node_priority(G, NODE_NUM)
        strategy_profile = initialize_strategy_profile(G, NODE_NUM)

        #randomly select a node that its best response is not its strategy, iterate until graph is MIS
        move_count = 0
        while True:
            waiting_nodes = find_waiting_node_MIS(G, NODE_NUM)
            if not waiting_nodes:
                break
            else:
                player = random.choice(list(waiting_nodes))
                G.nodes[player]['strategy'] = waiting_nodes[player]
                move_count += 1
        
        average_move_count[p] += move_count
        average_total_weight[p] += calculate_total_weight(G, NODE_NUM)

average_move_count /= (100 * NODE_NUM)
average_total_weight /= 100

plt.figure(figsize = (10, 5))
plt.subplot(1, 2, 1) 
plt.plot(probability,average_total_weight)
plt.title('Average total weight')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Average total weight')

plt.subplot(1, 2, 2)
plt.plot(probability,average_move_count)
plt.title('Average number of moves per node')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Average number of moves per node')
plt.show()

print_graph_MIS(G)

"""
hw1-2
Symmetric MDS-based IDS Game
"""
average_move_count = np.zeros(5)
average_cardinality = np.zeros(5)

for p in range(5):
    for i in range(100):
        #create watts_strogatz model with 30 nodes, 4 links for each node initially
        G = nx.watts_strogatz_graph(n = NODE_NUM, k = LINK_NUM, p = probability[p])
        adjacency = nx.to_numpy_array(G)
        node_weight = add_node_weight(G, NODE_NUM)
        strategy_profile = initialize_strategy_profile(G, NODE_NUM)

        #randomly select a node that its best response is not its strategy, iterate until graph is MIS
        move_count = 0
        while True:
            waiting_nodes = find_waiting_node_MDS_based_IDS(G, NODE_NUM)
            if not waiting_nodes:
                break
            else:
                player = random.choice(list(waiting_nodes))
                G.nodes[player]['strategy'] = waiting_nodes[player]
                move_count += 1
        
        average_move_count[p] += move_count
        average_cardinality[p] += calculate_cardinality(G, NODE_NUM)

average_move_count /= (100 * NODE_NUM)
average_cardinality /= 100

plt.figure(figsize = (10, 5))
plt.subplot(1, 2, 1) 
plt.plot(probability,average_cardinality)
plt.title('Average Size of Symmetric MDS-based IDS')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Cardinality of Symmetric MDS-based IDS')

plt.subplot(1, 2, 2)
plt.plot(probability,average_move_count)
plt.title('Average number of moves per node')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Average number of moves per node')
plt.show()

print_graph_MDS_based_IDS(G)