from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self._add_edges3()

    def _add_edges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.has_conn(u, v):
                    self._grafo.add_edge(u, v)

    def _add_edges2(self):
        for u in self._fermate:
            for conn in DAO.get_vicini(u):
                self._grafo.add_edge(u,self._idMapFermate.get(conn.id_stazA))

    def _add_edges3(self):
        all_edges = DAO.getAllEdges()
        for conn in all_edges:
            self._grafo.add_edge(self._idMapFermate.get(conn.id_stazP), self._idMapFermate.get(conn.id_stazA))

    def get_num_nodi(self):
        return len(self._grafo.nodes)

    def get_num_archi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate