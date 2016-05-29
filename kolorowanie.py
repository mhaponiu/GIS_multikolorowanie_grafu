from graph_tool.all import random_graph, Graph, load_graph, graph_draw
from Errors import CiagloscError

class Sprawdzenie(object):
    def __init__(self, graph):
        # type: (Graph)
        self.graph = graph

    def sprawdz(self):
        # type: () -> bool
        pass

    def _ciaglosc_przedzialu(self, lista):
        return sorted(lista) == range(min(lista), max(lista)+1)

    def _przypisane_kolory(self, wezel):
        dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
        #dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        dobra_lista = []
        for i in dziwna_lista:
            try:
                dobra_lista.append(int(i))
            except ValueError:
                continue
        return dobra_lista

    def _sprawdz_sasiadow(self, wezel):
        pass

    def dlugosc_dziur_grafu(self):
        pass

    def min_kolor(self):
        pass

    def max_kolor(self):
        pass


class Kolorowanie(object):
    def __init__(self, file_input):
        self.graph = load_graph(file_input)
        self.spr = Sprawdzenie(self.graph)

    def sprawdzenie(self):
        # type: () -> bool
        return self.spr.sprawdz()

    def _przypisane_kolory(self, wezel):
        dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
        # dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        dobra_lista = []
        for i in dziwna_lista:
            try:
                dobra_lista.append(int(i))
            except ValueError:
                continue
        return dobra_lista

