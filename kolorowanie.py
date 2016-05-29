from graph_tool.all import random_graph, Graph, load_graph, graph_draw
from Errors import CiagloscError, CiagloscErrorWezla, IloczynNiePusty, GISBaseException, IloczynNiePustyWezlow


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
        try:
            moje_kolory = self._przypisane_kolory(wezel)
            self._ciaglosc_przedzialu(moje_kolory)
            for sasiad in wezel.all_neighbours():
                self._sprawdz_wezel(sasiad, moje_kolory)
        except CiagloscError as e:
            raise CiagloscErrorWezla(wezel, e.przedzial)
        except IloczynNiePusty as e:
            raise IloczynNiePustyWezlow(e.zbior, sasiad, wezel)

        # except CiagloscError or IloczynNiePusty as e:
        #     raise e
        return True

    def _sprawdz_wezel(self, sasiad, kolory):
        zbior_kolorow_sasiada = set(self._przypisane_kolory(sasiad))
        iloczyn = zbior_kolorow_sasiada & set(kolory)
        zbior_pusty = set()
        if(iloczyn == zbior_pusty):
            return True
        else:
            raise IloczynNiePusty(iloczyn)


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
