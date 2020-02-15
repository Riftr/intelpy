import networkx as nx
import pickle


class EveData:
    def __init__(self, network_file="evedata.p", system_file="systems.p",
                 id_to_systems_file="idtosystems.p"):
        self.network_file = network_file
        self.system_file = system_file
        self.id_to_systems_file = id_to_systems_file

        try:
            with open(self.network_file, "rb") as datafile:
                self.universe = pickle.load(datafile)

            with open(self.system_file, "rb") as systemfile:
                self.systems_to_ids = pickle.load(systemfile)

            with open(self.id_to_systems_file, "rb") as idfile:
                self.ids_to_systems = pickle.load(idfile)

        except IOError as e:
            print("Could not read data file")
            print(str(e))
            raise

    def is_valid_system(self, system):
        if system in self.systems_to_ids:
            return True
        else:
            return False

    def shortest_path_length(self, source, destination):
        return nx.shortest_path_length(self.universe, source, destination)

    def get_system_name(self, id_code):
        # Get name from ID code
        return self.ids_to_systems[id_code]

    def get_id_code(self, name):
        # Get ID code from name
        return self.systems_to_ids[name]

    def get_neighbours_within(self, id_code, jumps):
        # Get nodes within X edges, returns a 'set' which we then make a list
        neighbour_graph = set(nx.ego_graph(self.universe, id_code, radius=jumps))
        #print(neighbour_graph)
        return list(neighbour_graph)




