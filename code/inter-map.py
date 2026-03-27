# Importing libraries
import geopandas as gpd
import networkx as nx
# for the interactive map
import folium

# A redo of the code in idk.py to loosy couple it's dependency
# Loading the data json file
kenya = gpd.read_file("./data/gadm41_KEN_2.json") # Thisgoes down to level 2 not the 3 previously downloaded
# filtering the dataset to select rows with geometry about Nairobi county
nrb_df = kenya[kenya["NAME_1"] == "Nairobi"]
nrb_df = nrb_df.reset_index(drop=True)

neighbours = {}
for i, row in nrb_df.iterrows():
    # initialize each sub-county list
    neighbours[i] = []

    for j, other in nrb_df.iterrows():
        if i!=j and row.geometry.intersects(other.geometry):
            neighbours[i].append(j)

G = nx.Graph()
for i in neighbours.keys():
    G.add_node(i)
for i, nbrs in neighbours.items():
    for nbr in nbrs:
        G.add_edge(i, nbr)

colors = nx.coloring.greedy_color(G, strategy="DSATUR")
colors.values()
nrb_df["color"] = nrb_df.index.map(colors)


# The real work to be done in this file
itr_mp = folium.Map(location=[-1.286389, 36.817223], zoom_start=11)

folium.GeoJson(
    nrb_df,
    style_function=lambda feature: {
        "fillColor": feature["properties"]["color"],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["NAME_2"],
        aliases=["Sub-County:"]
    ),
    popup=folium.GeoJsonPopup(
        fields=["NAME_2"],
        aliases=["Sub-County:"]
    )
).add_to(itr_mp)

itr_mp.save("./output/nrb_itr_map.html")