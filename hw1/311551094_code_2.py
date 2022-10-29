import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#randomly initialize strategy profile
def initialize_strategy_profile(G, node_num):
    strategy_profile = {}
    for node in range(node_num):
        neighbor_nodes = [-1]   #define null stratrgy as -1
        for neighbor in G.neighbors(node):
            neighbor_nodes.append(neighbor)
        strategy_profile[node] = random.choice(neighbor_nodes)
    nx.set_node_attributes(G, strategy_profile, name='strategy')

    return

#find node set that its strategy is not best response in matching game, store node as key, best response as value
def find_waiting_nodes(G, node_num):
    waiting_nodes = {}
    for node in range(node_num):
        cur_strategy = G.nodes[node]['strategy']

        if cur_strategy == -1 or G.nodes[cur_strategy]['strategy'] != node:   #If it is cuurently not matched
            has_null_neighbor = False
            best_response = -1
            null_neighbor = -1

            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['strategy'] == node:   #If it can have matched pairs
                    best_response = neighbor
                    break
                elif G.nodes[neighbor]['strategy'] == -1:   #Store the information whether it has any neighbor that its strategy is null
                    null_neighbor = neighbor
                    has_null_neighbor = True

            if best_response == -1 and has_null_neighbor:   #It can not find matched pair but has neighbor that its strategy is null
                best_response = null_neighbor

            if cur_strategy != best_response:
                waiting_nodes[node] = best_response
    
    return waiting_nodes

#calculate total number of matched pairs and set pairs' color and edge weight
def calculate_matched_pair(G):
    matched_pair = 0
    for node in G.nodes:
        G.nodes[node]['matched'] = 0

    for edge in G.edges:
        node_1 = edge[0]
        node_2 = edge[1]
        G[node_1][node_2]['weight'] = 1
        G[node_1][node_2]['color'] = 'k'
        if G.nodes[node_1]['strategy'] == node_2 and G.nodes[node_2]['strategy'] == node_1:
            matched_pair += 1
            G[node_1][node_2]['weight'] = 2
            G[node_1][node_2]['color'] = 'r'
            G.nodes[node_1]['matched'] = 1
            G.nodes[node_2]['matched'] = 1

    return matched_pair

#print graph
def print_graph(G):
    weights = [G[u][v]['weight'] for u,v in G.edges]
    edge_colors = [G[u][v]['color'] for u,v in G.edges]
    node_colors = [G.nodes[n]['matched'] for n in G.nodes]
    cmap = colors.ListedColormap(['y','r'])
    pos = nx.circular_layout(G)
    plt.figure(figsize = (7.5, 7.5))
    nx.draw_networkx(G, pos, width = weights, edge_color = edge_colors, node_color = node_colors, cmap = cmap)
    plt.show()

    return

NODE_NUM = 30
LINK_NUM = 4

probability = [p*0.2 for p in range(5)]

"""
hw 1-2
Matching Game
"""
average_move_count = np.zeros(5)
average_matched_pair = np.zeros(5)

for p in range(5):
    for i in range(100):
        #create watts_strogatz model with 30 nodes, 4 links for each node initially
        G = nx.watts_strogatz_graph(n = NODE_NUM, k = LINK_NUM, p = probability[p])
        initialize_strategy_profile(G, NODE_NUM)

        #randomly select a node that its best response is not its strategy, iterate until graph is MIS
        move_count = 0
        while True:
            waiting_nodes = find_waiting_nodes(G, NODE_NUM)
            if not waiting_nodes:
                break
            else:
                player = random.choice(list(waiting_nodes))
                G.nodes[player]['strategy'] = waiting_nodes[player]
                move_count += 1
        
        average_move_count[p] += move_count
        average_matched_pair[p] += calculate_matched_pair(G)

average_move_count /= (100 * NODE_NUM)
average_matched_pair /= 100

plt.figure(figsize = (10, 5))
plt.subplot(1, 2, 1) 
plt.plot(probability,average_matched_pair)
plt.title('Average Number of Matched Pairs')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Average Number of Matched Pairs')

plt.subplot(1, 2, 2)
plt.plot(probability,average_move_count)
plt.title('Average Number of Moves per Node')
plt.xlabel('Link Rewiring Probability')
plt.ylabel('Average Number of Moves per Node')
plt.show()

print_graph(G)