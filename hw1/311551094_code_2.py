import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#randomly initialize strategy profile
def initialize_strategy_profile(G, node_num):
    """strategy_profile = {}
    for node in range(node_num):
        strategy_profile[node] = random.randint(0,1)
    nx.set_node_attributes(G, strategy_profile, name='strategy')"""

    return

#print graph
def print_graph(G):
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
hw2
Matching Game
"""
average_move_count = np.zeros(5)
#average_total_weight = np.zeros(5)

for p in range(5):
    for i in range(100):
        #create watts_strogatz model with 30 nodes, 4 links for each node initially
        G = nx.watts_strogatz_graph(n = NODE_NUM, k = LINK_NUM, p = probability[p])
        initialize_strategy_profile(G, NODE_NUM)

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
        #average_total_weight[p] += calculate_total_weight(G, NODE_NUM)

average_move_count /= (100 * NODE_NUM)
#average_total_weight /= 100

"""plt.figure(figsize = (10, 5))
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

print_graph(G)"""