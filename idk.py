# Importing libraries in order of usage
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

# Loading the Geo json file
kenya = gpd.read_file("./data/gadm41_KEN_2.json") # Thisgoes down to level 2 not the 3 previously downloaded

# filtering the dataset to select rows with geometry about Nairobi county
nrb_df = kenya[kenya["NAME_1"] == "Nairobi"]
# Original sub-county indexes: Uncomment the line below to see the original indexes of the sub-counties
# print(nrb_df["NAME_2"])

# Resetting the index of nrb_df for easier color mapping later
nrb_df = nrb_df.reset_index(drop=True)
# Displaying the new index for the sub-counties
print(nrb_df["NAME_2"])

# Creating an Adjascency list for each sub-county
neighbours = {}

for i, row in nrb_df.iterrows():
    # initialize each sub-county list
    neighbours[i] = []

    for j, other in nrb_df.iterrows():
        if i!=j and row.geometry.intersects(other.geometry):
            neighbours[i].append(j)

# Check that we're not comparing a sub-county to itself and...
# ... that the geometries of the two sub-counties intersect
# Prefer 'row.geometry.touches(other.geometry)' because '.intersects()' captures borders better

# Initializing an undirected graph copy using the adjacency list above
G = nx.Graph()
# Adding nodes
for i in neighbours.keys():
    G.add_node(i)
# Adding edges
for i, nbrs in neighbours.items():
    for nbr in nbrs:
        G.add_edge(i, nbr)
# Visualizing our new graph to be mapped - Uncomment the following lines
"""
plt.figure(figsize=(10, 10))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title("Graph to be mapped")
plt.show()
"""

# Graph colouring
#colors = nx.coloring.greedy_color(G, strategy="largest_first")
colors = nx.coloring.greedy_color(G, strategy="DSATUR")
colors.values()

# Mapping the graph with distinct colouring back to the...
# ...original one with geometry
nrb_df["color"] = nrb_df.index.map(colors)
# Checking the data types - my own reasons
"""
print(nrb_df["color"].dtype)
print(type(colors))
"""

# Finally plotting the Nairobi sub-countes with distinct colours
# Task 2 done !!
fig, ax = plt.subplots(figsize=(10, 10))

nrb_df.plot(
    column="color",
    cmap="tab20",  # nice categorical colors
    edgecolor="black",
    legend=True,
    ax=ax
)

plt.title("Nairobi Sub-Counties: Now with colors!!")
plt.show()