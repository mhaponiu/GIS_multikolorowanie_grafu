# coding=utf-8
from graph_tool.all import Graph, load_graph, shortest_distance, local_clustering, vertex_average

import numpy, argparse, sys, logging

from Errors import CiagloscError, CiagloscErrorWezla, IloczynNiePusty, \
    GISBaseException, IloczynNiePustyWezlow, PropertyError, LiczebnoscKolorowError


class Sprawdzenie(object):
    def __init__(self, graph):
        # type: (Graph)
        self.graph = graph

    def sprawdz(self):
        # type: () -> bool
        for wezel in self.graph.vertices():
            self._liczebnosc_przypisanych_kolorow(wezel)
            self._sprawdz_sasiadow(wezel)
        return True

    def _liczebnosc_przypisanych_kolorow(self, wezel):
        try:
            powinno_byc = self._liczba_kolorow(wezel)
            jest_przypisanych = len(self._przypisane_kolory(wezel))
        except GISBaseException as e:
            raise e
        if powinno_byc == jest_przypisanych:
            return True
        else:
            raise LiczebnoscKolorowError(wezel, powinno_byc, jest_przypisanych)

    def _liczba_kolorow(self, wezel):
        try:
            return int(self.graph.vertex_properties['liczba_kolorow'][wezel])
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])

    def _ciaglosc_przedzialu(self, lista):
        posortowana = sorted(lista)
        if posortowana == range(min(lista), max(lista) + 1):
            return True
        else:
            raise CiagloscError(posortowana)

    def _przypisane_kolory(self, wezel):
        try:
            dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
            # dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])
        try:
            splited = dziwna_lista.split(', ')
        except AttributeError:
            return dziwna_lista  # dobra juz jest
        return [int(kolor_string) for kolor_string in splited]

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
        if (iloczyn == zbior_pusty):
            return True
        else:
            raise IloczynNiePusty(iloczyn)


class StatInfo(object):
    def __init__(self, graph):
        self.graph = graph

    def _przypisane_kolory(self, wezel):
        try:
            dziwna_lista = self.graph.vertex_properties['przypisane_kolory'][wezel]
            # dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
        except KeyError as e:
            raise PropertyError(wierzcholek=wezel, wlasciwosc=e.message[1])
        try:
            splited = dziwna_lista.split(', ')
        except AttributeError:
            return dziwna_lista  # dobra juz jest
        return [int(kolor_string) for kolor_string in splited]

    def srednia_liczba_kolorow(self):
        lista = []
        for v in self.graph.vertices():
            try:
                liczba = self.graph.vertex_properties['liczba_kolorow'][v]
                lista.append(int(liczba))
            # dziwna lista bo zwraca ['1', ',', ' ', '2', ',', ' ', '3'] zamiast [1,2,3]
            except KeyError as e:
                raise PropertyError(wierzcholek=v, wlasciwosc=e.message[1])
        return numpy.average(lista)

    def max_kolor(self):
        maximum = 0
        for v in self.graph.vertices():
            lista_max = self._przypisane_kolory(v)
            lista_max.append(maximum)
            maximum = max(lista_max)
        return maximum

    def liczba_krawedzi(self):
        suma = 0
        for v in self.graph.vertices():
            suma = suma + len(list(v.all_edges()))
        return suma / 2

    def liczba_wierzcholkow(self):
        return len(list(self.graph.vertices()))

    def sredni_stopien_wierzcholka(self):
        lista_stopni = []
        for v in self.graph.vertices():
            lista_stopni.append(len(list(v.all_edges())))
        return numpy.average(lista_stopni)

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

    def statystyki(self):
        # stat = OrderedDict()
        stat = {}
        stat['sredni_wspolczynnik_klasteryzacji'] = self.sredni_wspolczynnik_klasteryzacji()
        stat['srednia_dlugosc_sciezki'] = self.srednia_dlugosc_sciezki()
        stat['liczba_wierzcholkow'] = self.liczba_wierzcholkow()
        stat['liczba_krawedzi'] = self.liczba_krawedzi()
        try:
            stat['max_kolor'] = self.max_kolor()
        except PropertyError:
            pass
        try:
            stat['srednia_liczba_kolorow'] = self.srednia_liczba_kolorow()
        except PropertyError:
            pass
        stat['sredni_stopien_wierzcholka'] = self.sredni_stopien_wierzcholka()
        return stat


class Kolorowanie(object):
    def __init__(self, file_input):
        self.graph = load_graph(file_input)
        self.spr = Sprawdzenie(self.graph)
        self.stat = StatInfo(self.graph)

    def sprawdzenie(self):
        # type: () -> bool
        return self.spr.sprawdz()

    def statystyki(self):
        return self.stat.statystyki()

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
        log_100 = len(lista_wezlow)
        log_x = log_100
        while lista_wezlow != []:
            wezel = lista_wezlow[0]
            # print 'koloruje ', lista_wezlow[wezel]
            kolory = self._koloruj_wierzcholek(wezel)
            self.graph.vertex_properties['przypisane_kolory'][wezel] = kolory
            lista_wezlow.remove(lista_wezlow[0])
            self._seria_sortowan(lista_wezlow)
            log_x = log_x - 1
            logging.info(" postęp: " + str(int(100 - log_x * 100 / log_100)) + "%")

    def _seria_sortowan(self, lista_wezlow):
        self._sortuj_liczba_kolorow(lista_wezlow)
        self._sortuj_stopien(lista_wezlow)
        self._sortuj_suma_przypisanych_kolorow_sasiadow(lista_wezlow)

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

    def _sortuj_liczba_kolorow(self, lista_wezlow, od_najwiekszego=True):
        lista_wezlow.sort(reverse=od_najwiekszego, key=lambda v: self.graph.vertex_properties['liczba_kolorow'][v])

    def _sortuj_stopien(self, lista_wezlow, od_najwiekszego=True):
        lista_wezlow.sort(reverse=od_najwiekszego, key=lambda v: len(list(v.all_edges())))

    def _sortuj_suma_przypisanych_kolorow_sasiadow(self, lista_wezlow, od_najwiekszego=True):
        lista_wezlow.sort(reverse=od_najwiekszego, key=self._suma_kolorow_sasiadow)

    def _suma_kolorow_sasiadow(self, wezel):
        suma = 0
        for w in wezel.all_neighbours():
            suma = suma + len(self._przypisane_kolory(w))
        # print 'wezel',str(wezel), ' ',suma
        return suma

    def _koloruj_wierzcholek(self, wezel):
        liczba_kolorow = self._liczba_kolorow(wezel)
        lista_list_kolorow_sasiadow = self._listy_przypisanych_kolorow_sasiadow(wezel)
        zbior_kolorow_sasiadow = self._zbior(lista_list_kolorow_sasiadow)
        try:
            maximum = max(zbior_kolorow_sasiadow)
            kolory = range(maximum + 1, maximum + 1 + liczba_kolorow)
            for dziura in self._generuj_dziure(zbior_kolorow_sasiadow):
                if len(dziura) >= liczba_kolorow:
                    kolory = dziura[:liczba_kolorow]
                    break
            return kolory
        except ValueError as e:
            return range(1, liczba_kolorow + 1)

    def _generuj_dziure(self, zbior_kolorow_sasiadow):
        try:
            maximum = max(zbior_kolorow_sasiadow)
        except ValueError:
            return
        dziura = []
        for i in xrange(1, maximum + 1):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('Input_file')
    parser.add_argument('-o', '--output', help="nazwa pliku wynikowego, (type: %(type)s)"
                        , type=str, default='')
    parser.add_argument('-c', '--check', action='store_true',
                        help='wykonuje sprawdzenie poprawnosci pokolorowania grafu')
    parser.add_argument('-s', '--stat', action='store_true',
                        help='podaje dane statystyczne grafu')
    parser.add_argument('--INFO', action='store_true',
                        help='wyswietla dodatkowe informacje w trakcie wykonywania zadania')
    zparsowane = parser.parse_args()

    k = Kolorowanie(file_input=zparsowane.Input_file)

    if zparsowane.INFO:
        logging.basicConfig(level=logging.INFO)

    if zparsowane.output:
        k.koloruj()
        k.zapisz(zparsowane.output)

    if zparsowane.check:
        k.sprawdzenie()
        print "\nGraf został sprawdzony:\n\twynik pozytywny"

    if zparsowane.stat:
        print "\nStatystyki:"
        stat = k.statystyki()
        for (key, value) in zip(stat.keys(), stat.values()):
            print ' '.join(['\t', key, ':', str(value)])
