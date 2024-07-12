import flet as ft
from networkx import bfs_edges, node_connected_component


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        #pulisco per nuovi outup quelli vecchi
        self._view.txt_result.clean()#pulisco finestra risultati per nuova iterazione in caso ce ne fossero gia state altre prima

        if self._view._txtInDurata is None or self._view._txtInDurata=="":
            self._view.txt_result.controls.append(ft.Text(f"inserisci la durata"))
            self._view.update_page()
            return
        #d:int
        try:
            d= int(self._view._txtInDurata.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"la durata deve essere un valore numerico"))
            self._view.update_page()
            return

        d=d*60000 #trasformo minuti in millisecondi come indicata durata canzoni nei dati della tabella

        self._model.creaGrafo(d)
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.numeroNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.numeroArchi()}"))
        self.fillDD()
        self._view.update_page()

    def fillDD(self):
        self._view._ddAlbum.clean()
        for nodo in self._model._grafo.nodes():
            self._view._ddAlbum.options.append(ft.dropdown.Option(nodo.Title))
    #non lo chiam nel load_interface della view perchè quella è la prima cosa che viene eseguita dal main
    #e all'inizio non ho ancora la selezione con cui riempiire il dropdown; ma ce l'ho dopo che qualcuno ha schiacciato
    #il bottone per creare il grafo lanciato handleCreaGrafo del controller e quindi dato che dopo quel
    #metodo voglio il dd pieno pronto per selezionare qualcosa lo faccio riempire proprio da handleCreaGrafo del controller
    #chiamando fillDD a fine della definizione di quel metodo prima di aggiornare la pagina del view

    def getSelectedAlbum(self, e):
        pass


    def handleAnalisiComp(self, e):
        for nodo in self._model._grafo.nodes():
            self._view._ddAlbum.options.append(ft.dropdown.Option(nodo.Title))
        if self._view._ddAlbum.value is None:
            self._view.txt_result.controls.append(ft.Text(f"selezionare un album"))
            return
        albumSelezionato= None
        for nodo in self._model._grafo.nodes():
            if nodo.Title==self._view._ddAlbum.value:
                albumSelezionato=nodo
                continue
        self._view.txt_result.clean()#perchè output è voluto senza outup del bottone precedente
        self._view.txt_result.controls.append(ft.Text(f"album selezionato: {self._view._ddAlbum.value}"))

        print()
        print(albumSelezionato)
        setNodiComponenteConnessa=node_connected_component(self._model._grafo, albumSelezionato)

        self._view.txt_result.controls.append(ft.Text(f"numero nodi appartenenti alla componente connessa: {len(setNodiComponenteConnessa)}"))


        #setNodiComponenteConnessa.add(nodo)
        durataComponenteConnessa=self._model.getDurataComponenteConnessa(setNodiComponenteConnessa)
        self._view.txt_result.controls.append(ft.Text(f"durata componente connessa: {durataComponenteConnessa}"))



        self._view.update_page()




    def handleGetSetAlbum(self, e):
        pass