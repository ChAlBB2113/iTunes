import networkx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listaNodi=[]
        self._listaArchi=[]
        self._grafo=networkx.Graph()
        self._dizionarioNodi={}

    def creaGrafo(self, d):
        self._listaNodi.clear()
        self._listaArchi.clear()
        self._grafo.clear()
        self._dizionarioNodi={}#inizializza/reinizializza

        self._listaNodi=DAO.getNodi(d)
        self._grafo.add_nodes_from(self._listaNodi)


        for album in self._listaNodi:
            self._dizionarioNodi[album.AlbumId]=album
        self._listaArchi= DAO.getArchi(self._dizionarioNodi)
        self._grafo.add_edges_from(self._listaArchi)

    def getDurataComponenteConnessa(self, setNodiComponenteConnessa):
        sumTot=0
        listaTracks=DAO.getTrack()
        for nodo in setNodiComponenteConnessa:
            sumAlbum=0
            for track in listaTracks:
                if track.AlbumId==nodo.AlbumId:
                    sumAlbum+=track.Milliseconds
            sumTot+=sumAlbum
        return sumTot/60000


    def numeroNodi(self):
        return len(self._grafo.nodes())
    def numeroArchi(self):
        return len(self._grafo.edges())