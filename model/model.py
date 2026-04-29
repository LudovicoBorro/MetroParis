from datetime import datetime
from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        nodiBFS = []
        for u, v in archi:
            nodiBFS.append(v)
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        # tic = datetime.now()
        # self._add_edges()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc-tic)

        # tic = datetime.now()
        # self._add_edges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc-tic)

        tic = datetime.now()
        self._add_edges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc-tic)

    def _add_edges(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.has_conn(u, v):
                    self._grafo.add_edge(u, v)

    def _add_edges2(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.get_vicini(u):
                self._grafo.add_edge(u,self._idMapFermate.get(conn.id_stazA))

    def _add_edges3(self):
        self._grafo.clear_edges()
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