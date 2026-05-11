from datetime import datetime
import geopy.distance
from database.DAO import DAO
import networkx as nx

def getPesoTempoPercorrenza(u, v, vel):
    dist = geopy.distance.distance((u.coordX, u.coordY), (v.coordX, v.coordY)).km
    time = dist/vel * 60 # minuti
    return time

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getShortestPath(self, u, v):
        return nx.single_source_dijkstra(self._grafo, u, v)

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesatiTempi()

    def addEdgesPesatiTempi(self):
        """Questo metodo crea degli archi, in cui il peso è pari al tempo di percorrenza di quell'arco,
        ottenuto come rapporto fra la distanza fra due stazioni e la velocità di percorrenza."""
        self._grafo.clear_edges()
        all_edges_vel = DAO.getAllEdgesVel()
        for e in all_edges_vel:
            u = self._idMapFermate.get(e[0])
            v = self._idMapFermate.get(e[1])
            peso = getPesoTempoPercorrenza(u, v, e[2])
            self._grafo.add_edge(u, v, weight = peso)

    def addEdgesPesati(self):
        # Riutilizzare il principio di funzionamento del metodo add_edges3,
        # ma contando quante volte provo ad aggiungere l'arco.
        self._grafo.clear_edges()
        all_edges = DAO.getAllEdges()
        for conn in all_edges:
            u = self._idMapFermate.get(conn.id_stazP)
            v = self._idMapFermate.get(conn.id_stazA)

            if self._grafo.has_edge(u,v):
                self._grafo[u][v]["weight"] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)

    def addEdgesPesatiV2(self):
        # Delega il calcolo del peso a query SQL, per semplificarci la vita in python
        self._grafo.clear_edges()
        allEdgesWPeso = DAO.getAllEdgesPesati()
        # (id_stazP, id_stazA, peso)
        for e in allEdgesWPeso:
            u = self._idMapFermate.get(e[0])
            v = self._idMapFermate.get(e[1])
            peso = e[2]
            self._grafo.add_edge(u, v, weight = peso)

    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True)

        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])['weight'] > 1:
                edgesMaggiori.append(e)

        return edgesMaggiori

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