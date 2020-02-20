import networkx as nx
import resources.evedata as evedata
import pickle

universe = None
system_to_ids = []

try:
    with open("../resources/evedata.p", "rb") as datafile:
        universe = pickle.load(datafile)

    with open("../resources/systems.p", "rb") as systemfile:
        systems_to_ids = pickle.load(systemfile)

except IOError as e:
    print("Could not read data file")
    print(str(e))
    raise

# Print info about the map
print(nx.info(universe))
home_system = systems_to_ids["NIDJ-K"]
print("Got home system ID: " + home_system)

# print list of node names from the universe network
for n in universe.nodes():
    print(n, universe.nodes[n]["system"])
assert(universe.nodes["30000142"]["system"] == "Jita")

# Get neighbours
neighbour_graph = set(nx.ego_graph(universe, home_system, radius=5))
print(neighbour_graph)
