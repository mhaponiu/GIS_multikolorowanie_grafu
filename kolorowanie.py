# coding=utf-8
from graph_tool.all import random_graph, Graph, load_graph, graph_draw, \
    all_shortest_paths, shortest_distance, global_clustering, local_clustering, \
    vertex_average

import numpy

from Errors import CiagloscError, CiagloscErrorWezla, IloczynNiePusty,\
    GISBaseException, IloczynNiePustyWezlow, PropertyError


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
        try:
            return self.spr.sprawdz()
        except GISBaseException as e:
            raise e

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
            return int(self.graph.vertex_properties['liczba_kolorow'][wezel])
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])

    def koloruj(self):
        self._dodaj_i_inicjuj_wlasciwosc_przypisane_kolory()
        lista_wezlow = list(self.graph.vertices())
        self._seria_sortowan(lista_wezlow)
        # TODO

    def _seria_sortowan(self, lista_wezlow):
        self._sortuj_liczba_kolorow(lista_wezlow)
        self._sortuj_stopien(lista_wezlow)

    def zapisz(self, output_file):
        posplitowane = output_file.split('.')
        if len(posplitowane) == 1:
            output_file = output_file + '.dot'
        else:
            output_file = ('_').join(posplitowane[:-1])
            if posplitowane[-1] == 'dot':
                output_file = output_file + '.dot'
            else:
                output_file = output_file + '.xml'
        self.graph.save(output_file)

    def _dodaj_i_inicjuj_wlasciwosc_przypisane_kolory(self):
        self.graph.vertex_properties['przypisane_kolory'] = self.graph.new_vertex_property('vector<int>')
        # for v in self.graph.vertices():
        #     self.graph.vertex_properties['przypisane_kolory'][v] = []

    def _sortuj_liczba_kolorow(self, lista_wierzcholkow, od_najwiekszego=True):
        lista_wierzcholkow.sort(reverse=od_najwiekszego, key=lambda v: self.graph.vertex_properties['liczba_kolorow'][v])

    def _sortuj_stopien(self, lista_wierzcholkow, od_najwiekszego=True):
        lista_wierzcholkow.sort(reverse=od_najwiekszego, key=lambda v: len(list(v.all_edges())))

    def _koloruj_wierzcholek(self, wezel):
        liczba_kolorow = self._liczba_kolorow(wezel)
        lista_list_kolorow_sasiadow = self._listy_przypisanych_kolorow_sasiadow(wezel)
        zbior_kolorow_sasiadow = self._zbior(lista_list_kolorow_sasiadow)
        try:
            maximum = max(zbior_kolorow_sasiadow)
            kolory = range(maximum+1, maximum+1+liczba_kolorow)
            for dziura in self._generuj_dziure(zbior_kolorow_sasiadow):
                if len(dziura) <= liczba_kolorow:
                    kolory = dziura
                    break
            return kolory
        except ValueError as e:
            return range(1, liczba_kolorow+1)


    def _generuj_dziure(self, zbior_kolorow_sasiadow):
        try:
            maximum = max(zbior_kolorow_sasiadow)
        except ValueError:
            return
        dziura = []
        for i in xrange(1, maximum+1):
            if i in zbior_kolorow_sasiadow:
                if dziura == []:
                    continue
                else:
                    yield dziura
                    dziura = []

            else:
                dziura.append(i)

    def _zbior(self, lista_list):
        zbior = set()
        for lista in lista_list:
            for i in lista:
                zbior.add(i)
        return zbior

    def _listy_przypisanych_kolorow_sasiadow(self, wezel):
        ret_lista = []
        for v in wezel.all_neighbours():
            ret_lista.append(self._przypisane_kolory(v))
        return ret_lista
