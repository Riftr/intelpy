import pickle
import networkx as nx
import json


# pickle externals universe data

def convert_data(universe):
    edges = []            # List of tuples containing links between systems
    node_names = []       # Basic list of nodes
    extract_value = []    # Used to store tuple data temp
    system_name = {}      # Attributes
    system_sec = {}
    system_reg = {}
    system_to_ids = {}
    ids_to_system = {}    # Other way around

    # Edges
    for edge_item in universe["edges"]:
        extract_value.clear()
        for key, value in edge_item.items():
            extract_value.append(value)
        edge_tuple = (str(extract_value[0]), str(extract_value[1]))
        edges.append(edge_tuple)
    print("Len of edges: " + str(len(edges)))

    # Nodes
    node_dict = {}
    for node_item in universe["nodes"]:
        node_dict[node_item] = universe["nodes"][node_item]
        node_names.append(node_item)  # Just items list for NetworkX
        system_name_upper = str(universe["nodes"][node_item]["name"]).upper()
        system_to_ids[system_name_upper] = node_item
        ids_to_system[node_item] = system_name_upper

    # Access them (THIS IS NOT IN THE NETWORK)
    print(node_dict["30000001"])
    print(node_dict["30000001"]["name"])
    print(node_dict["30000001"]["security"])
    print(node_dict["30000001"]["region"])
    print("Len of node dict: " + str(len(node_dict)))

    print(node_names)

    # Add attributes
    for node in node_names:
        system_name[node] = node_dict[node]["name"]
        system_sec[node] = node_dict[node]["security"]
        system_reg[node] = node_dict[node]["region"]

    print("Attb dicts")
    print("Systems: " + str(len(system_name)))
    print("Security: " + str(len(system_sec)))
    print("Region: " + str(len(system_reg)))
    print(system_name)
    print(system_sec)
    print(system_reg)
    print("---")

    # Load data into a networkX graph
    eve_graph = nx.Graph()
    eve_graph.add_nodes_from(node_names)
    eve_graph.add_edges_from(edges)
    nx.set_node_attributes(eve_graph, system_name, 'system')
    nx.set_node_attributes(eve_graph, system_sec, 'security')
    nx.set_node_attributes(eve_graph, system_reg, 'region')
    eve_graph.name = "Eve_Universe"

    # Note: looping over them will fail, as wormhole nodes contain no edges
    # for n in eve_graph.nodes():
    #     print(n, eve_graph.nodes[n]['system'])
    print("Should print Jita: " + eve_graph.nodes["30000142"]["system"])
    assert(eve_graph.nodes["30000142"]["system"] == "Jita")  # Fail if we don't get Jita, means there is prob with data
    assert(system_to_ids["JITA"] == "30000142")
    assert(ids_to_system["30000142"] == "JITA")

    # Dump graph for use in app
    pickle.dump(eve_graph, open("../resources/evedata.p", "wb"))
    # Dump system to id dict
    pickle.dump(system_to_ids, open("../resources/systems.p", "wb"))

    # Dump id to system dict
    pickle.dump(ids_to_system, open("../resources/idtosystems.p", "wb"))

    # Print some info about the import
    print(nx.info(eve_graph))

    # Print list of nodes
    for n in eve_graph.nodes():
        print(n, eve_graph.nodes[n]["system"])

# Starts here
def main():
    # This used Fuzzwork's data dumps, see https://www.fuzzwork.co.uk/dump/
    try:
        with open("universe_pretty.json", "r") as universe_file:
            universe_reader = json.load(universe_file)   # Outer edge dict. returns nodes(dict) and edges(dict)
    except IOError as e:
        print("Could not read universe.json file")
        print(str(e))
        exit(1)
    print(len(universe_reader))  # Should be 2 x Dict
    assert len(universe_reader) == 2
    convert_data(universe_reader) # Process data

if __name__ == '__main__':
    main()
