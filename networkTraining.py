import networkx as nx  
import matplotlib.pyplot as plt
G=nx.DiGraph()
G.add_node(0),G.add_node(1),G.add_node(2),G.add_node(3),G.add_node(4)
G.add_edge(0, 1),G.add_edge(1, 2),G.add_edge(0, 2),G.add_edge(1, 4),G.add_edge(1, 3),G.add_edge(3, 2),G.add_edge(3,1),G.add_edge(4,3)
nx.draw(G, with_labels=True, font_weight='bold')


for cycle in nx.simple_cycles(G):
	print(cycle)

plt.show()


