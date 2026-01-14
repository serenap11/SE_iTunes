import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.g = nx.Graph()
        self.albums = []
        self.id_album = {}
        self.playlist = {}

    def carica_album(self, min_durata):
        #carica album con durata totale > min_durata
        self.albums = DAO.get_durata_album(min_durata)
        self.id_album = {a.id: a for a in self.albums}

    def carica_playlist(self):
        self.playlist = DAO.get_playlist(self.albums)

    def costruisci_grafo(self):
        self.g.clear()
        self.g.add_nodes_from(self.albums)

        for i, a1 in enumerate(self.albums):
            for a2 in self.albums[i+1:]:
                if self.playlist[a1] & self.playlist[a2]:
                    self.g.add_edge(a1, a2)

    def get_componente(self, album):
        if album not in self.g:
            return []
        return list(nx.node_connected_component(self.g, album))

    def compute_best_set(self, start_album, max_duration):
        component = self.get_componente(start_album)
        self.soluzione_migliore = []
        self.ricorsione(component, [start_album], start_album.duration, max_duration)
        return self.soluzione_migliore

    def ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_migliore):
            self.soluzione_migliore = current_set[:]

        for album in albums:
            if album in current_set:
                continue
            new_duration = current_duration + album.duration
            if new_duration <= max_duration:
                current_set.append(album)
                self.ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()




