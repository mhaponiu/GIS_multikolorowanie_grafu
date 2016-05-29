# coding=utf-8
from graph_tool.all import random_graph, Graph, load_graph, graph_draw, \
    all_shortest_paths, shortest_distance, global_clustering, local_clustering, \
    vertex_average

import numpy

from Errors import CiagloscError, CiagloscErrorWezla, IloczynNiePusty, GISBaseException, IloczynNiePustyWezlow, \
    PropertyError


class Sprawdzenie(object):
    def __init__(self, graph):
        # type: (Graph)
        self.graph = graph

    def sprawdz(self):
        # type: () -> bool
        try:
            for wezel in self.graph.vertices():
                self._sprawdz_sasiadow(wezel)
        except GISBaseException as e:
            raise e
        return True

    def _ciaglosc_przedzialu(self, lista):
        posortowana = sorted(lista)
        if posortowana == range(min(lista), max(lista)+1):
            return True
        else:
            raise CiagloscError(posortowana)

    def _przypisane_kolory(self, wezel):
        try:
            dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
            #dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])
        dobra_lista = []
        for i in dziwna_lista:
            try:
                dobra_lista.append(int(i))
            except ValueError:
                continue
        return dobra_lista

    def _sprawdz_sasiadow(self, wezel):
        try:
            moje_kolory = self._przypisane_kolory(wezel)
            self._ciaglosc_przedzialu(moje_kolory)
            for sasiad in wezel.all_neighbours():
                self._sprawdz_wezel(sasiad, moje_kolory)
        except CiagloscError as e:
            raise CiagloscErrorWezla(wezel, e.przedzial)
        except IloczynNiePusty as e:
            raise IloczynNiePustyWezlow(e.zbior, sasiad, wezel)
        except GISBaseException as e:
            raise e
        return True

    def _sprawdz_wezel(self, sasiad, kolory):
        zbior_kolorow_sasiada = set(self._przypisane_kolory(sasiad))
        iloczyn = zbior_kolorow_sasiada & set(kolory)
        zbior_pusty = set()
        if(iloczyn == zbior_pusty):
            return True
        else:
            raise IloczynNiePusty(iloczyn)


class StatInfo(object):
    def __init__(self, graph):
        self.graph = graph

    def srednia_kolorow(self):
        pass

    def mediana_kolorow(self):
        pass

    def suma_dziur_grafu(self):
        pass

    def min_kolor(self):
        pass

    def max_kolor(self):
        pass

    def liczba_krawedzi(self):
        pass

    def _max_liczba_krawedzi(self):
        pass

    def liczba_wierzcholkow(self):
        pass

    def sredni_stopien_wierzcholka(self):
        pass

    def sredni_wspolczynnik_klasteryzacji(self):
        '''The local clustering coefficient [watts-collective-1998] ci is defined as
        ci=|{ejk}| / (ki(ki−1))   :vj,vk∈Ni,ejk∈E
        where ki is the out-degree of vertex i, and
        Ni={vj:eij∈E}
        is the set of out-neighbours of vertex i.
        For undirected graphs the value of ci is normalized as  c′i=2ci.
        The implemented algorithm runs in O(|V|⟨k⟩2) time, where ⟨k⟩ is the average out-degree
        https://en.wikipedia.org/wiki/Clustering_coefficient'''
        lc = local_clustering(self.graph, undirected=True)
        return vertex_average(self.graph, lc)[0]


    def srednia_dlugosc_sciezki(self):
        # shortest_distance korzysta z algorytmu Johnson'a O(V E log V).
        srednie = []
        for len_array in shortest_distance(self.graph):
            srednie.append(len_array)
        return numpy.average(srednie)







class Kolorowanie(object):
    def __init__(self, file_input):
        self.graph = load_graph(file_input)
        self.spr = Sprawdzenie(self.graph)

    def sprawdzenie(self):
        # type: () -> bool
        return self.spr.sprawdz()

    def _przypisane_kolory(self, wezel):
        try:
            dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
            # dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])
        dobra_lista = []
        for i in dziwna_lista:
            try:
                dobra_lista.append(int(i))
            except ValueError:
                continue
        return dobra_lista

    def _liczba_kolorow(self, wezel):
        try:
            return self.graph.vertex_properties['liczba_kolorow'][wezel]
        except PropertyError as e:
            raise e
