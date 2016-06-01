import unittest
from graph_tool import Graph
from graph_tool.clustering import local_clustering
from graph_tool.stats import vertex_average

import numpy

from Errors import CiagloscError, IloczynNiePusty, GISBaseException, IloczynNiePustyWezlow, CiagloscErrorWezla, \
    PropertyError, LiczebnoscKolorowError
from kolorowanie import Kolorowanie, Sprawdzenie, StatInfo


class Wzorzec_przed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.wzorzec_przed = 'dane_testowe/wzorzec_przed.dot'
        cls.k = Kolorowanie(file_input=cls.wzorzec_przed)
        cls.g = cls.k.graph

    def test_create(self):
        k = Kolorowanie(self.wzorzec_przed)

    def test_iter_vertex_index1(self):
        for v in zip(self.g.vertices(), range(5)):
            self.assertEqual(v[0], v[1])

    def test_iter_vertex_index2(self):
        for tuple in zip(self.g.vertices(), range(5)):
            self.assertEqual(self.g.vertex_index[tuple[0]], tuple[1])

    def test_iter_vertex_liczba_kolorow(self):
        liczby_kolorow = [1,3,2,2,1,1]
        for tuple in zip(self.g.vertices(), liczby_kolorow):
            self.assertEqual(int(self.g.vertex_properties['liczba_kolorow'][tuple[0]]),
                             tuple[1])


class Wzorzec_po(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wzorzec_po = 'dane_testowe/wzorzec_po.dot'
        cls.k = Kolorowanie(file_input=cls.wzorzec_po)
        cls.g = cls.k.graph

    def test_create(self):
        k = Kolorowanie(self.wzorzec_po)

    def test_przypisane_kolory(self):
        v1 = list(self.g.vertices())[1]
        self.assertEqual(set(self.k.spr._przypisane_kolory(v1)), set([1, 2, 3]))

class Sprawdzenie_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wzorzec_po = 'dane_testowe/wzorzec_po.dot'
        k = Kolorowanie(wzorzec_po)
        cls.spr = Sprawdzenie(graph=k.graph)

        wzorzec_zly_iloczyn_po = 'dane_testowe/wzorzec_zly_iloczyn_po.dot'
        k_zly_iloczyn = Kolorowanie(file_input=wzorzec_zly_iloczyn_po)
        cls.spr_zly_iloczyn = Sprawdzenie(graph=k_zly_iloczyn.graph)

        wzorzec_zly_nieciagly_przdzial_po = 'dane_testowe/wzorzec_zly_nieciagly_przedzial_po.dot'
        k_zly_nieciagly_przedzial = Kolorowanie(file_input=wzorzec_zly_nieciagly_przdzial_po)
        cls.spr_zly_nieciagly_przedzial = Sprawdzenie(graph=k_zly_nieciagly_przedzial.graph)

        wzorzec_zla_liczebnosc = 'dane_testowe/wzorzec_zla_liczebnosc.dot'
        k_zla_liczebnosc = Kolorowanie(file_input=wzorzec_zla_liczebnosc)
        cls.spr_zla_liczebnosc = Sprawdzenie(graph=k_zla_liczebnosc.graph)

        wzorzec_przed = 'dane_testowe/wzorzec_przed.dot'
        k_przed = Kolorowanie(wzorzec_przed)
        cls.spr_przed = Sprawdzenie(graph=k_przed.graph)

    def test_ciaglosc_przedzialu_1(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([1, 2, 3]), True)

    def test_ciaglosc_przedzialu_2(self):
        self.assertRaises(CiagloscError, self.spr._ciaglosc_przedzialu, [1, 3])

    def test_ciaglosc_przedzialu_3(self):
        self.assertRaises(CiagloscError, self.spr._ciaglosc_przedzialu, [3, 3])

    def test_ciaglosc_przedzialu_4(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([4, 3]), True)

    def test_ciaglosc_przedzialu_5(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([4]), True)

    def test_ciaglosc_przedzialu_6(self):
        self.assertRaises(CiagloscError, self.spr._ciaglosc_przedzialu, [3, 1])

    def test_przypisane_kolory(self):
        v1 = list(self.spr.graph.vertices())[1]
        self.assertEqual(set(self.spr._przypisane_kolory(v1)), set([1,2,3]))

    def test_sprawdz_wezel1(self):
        v1 = list(self.spr.graph.vertices())[1] #kolory 1,2,3
        self.assertTrue(self.spr._sprawdz_wezel(v1, set([])))

    def test_sprawdz_wezel2(self):
        v1 = list(self.spr.graph.vertices())[1] #kolory 1,2,3
        self.assertRaises(IloczynNiePusty,
                          self.spr._sprawdz_wezel,
                          v1, set([1]))

    def test_sprawdz_wezel3(self):
        v1 = list(self.spr.graph.vertices())[1] #kolory 1,2,3
        self.assertRaises(IloczynNiePusty,
                          self.spr._sprawdz_wezel,
                          v1, set([3,4,5]))

    def test_sprawdz_wezel4(self):
        v1 = list(self.spr.graph.vertices())[1] #kolory 1,2,3
        self.assertTrue(self.spr._sprawdz_wezel(v1, set([4, 5])))


    def test_sprawdz_sasiadow(self):
        v1 = list(self.spr.graph.vertices())[1]  # kolory 1,2,3
        self.spr._sprawdz_sasiadow(v1)

    def test_sprawdz_sasiadow2(self):
        v1 = list(self.spr_zly_iloczyn.graph.vertices())[1]  # kolory 1,2,3,4
        self.assertRaises(IloczynNiePusty,
                          self.spr_zly_iloczyn._sprawdz_sasiadow, v1)

    def test_sprawdz_sasiadow3(self):
        v2 = list(self.spr_zly_iloczyn.graph.vertices())[2]  # kolory 4,5
        self.assertRaises(IloczynNiePusty,
                          self.spr_zly_iloczyn._sprawdz_sasiadow, v2)

    def test_sprawdz_sasiadow4(self):
        v0 = list(self.spr_zly_iloczyn.graph.vertices())[0]  # kolory 6
        self.assertTrue(self.spr_zly_iloczyn._sprawdz_sasiadow(v0))

    def test_sprawdz_dobry(self):
        self.assertTrue(self.spr.sprawdz())

    def test_sprawdz_zly_iloczyn(self):
        self.assertRaises(IloczynNiePustyWezlow, self.spr_zly_iloczyn.sprawdz)
        # self.spr_zly_iloczyn.sprawdz()

    def test_sprawdz_zla_liczebnosc_przypisanych_kolorow(self):
        self.assertRaises(LiczebnoscKolorowError, self.spr_zla_liczebnosc.sprawdz)

    def test_sprawdz_zly_nieciagly_przedzial(self):
        self.assertRaises(CiagloscErrorWezla, self.spr_zly_nieciagly_przedzial.sprawdz)
        # self.spr_zly_nieciagly_przedzial.sprawdz()

    def test_brak_wlasciwosci_w_wezle(self):
        self.assertRaises(PropertyError, self.spr_przed.sprawdz)

class StatInfoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wzorzec_po = 'dane_testowe/wzorzec_po.dot'
        k = Kolorowanie(wzorzec_po)
        cls.g = k.graph
        cls.stat = StatInfo(graph=k.graph)

    def test_srednia_dlugosc_sciezki(self):
        oczekiwany_wynik = numpy.average([0, 1, 1, 2, 1, 2,
                                          1, 0, 1, 1, 1, 1,
                                          1, 1, 0, 2, 2, 2,
                                          2, 1, 2, 0, 2, 2,
                                          1, 1, 2, 2, 0, 2,
                                          2, 1, 2, 2, 2, 0])

        self.assertEqual(oczekiwany_wynik, self.stat.srednia_dlugosc_sciezki())

    def test_sredni_wspolczynnik_klasteryzacji(self):
        self.assertAlmostEqual(0.477777777778, self.stat.sredni_wspolczynnik_klasteryzacji(), delta=0.0000001)

    def test_sredni_wspolczynnik_klasteryzacji_na_sztywno_graf_pelny(self):
        # self.assertEqual(7. / 15, self.stat.sredni_wspolczynnik_klasteryzacji_moj())
        # print self.stat.sredni_wspolczynnik_klasteryzacji_moj()
        g=Graph(directed=False)
        v0 = g.add_vertex()
        v1 = g.add_vertex()
        v2 = g.add_vertex()
        v3 = g.add_vertex()
        g.add_edge(v0, v1)
        g.add_edge(v0, v2)
        g.add_edge(v0, v3)
        g.add_edge(v1, v2)
        g.add_edge(v1, v3)
        g.add_edge(v2, v3)
        lc = local_clustering(g, undirected=True)
        self.assertEqual(1.0, vertex_average(g, lc)[0])

    def test_statystyki_bez_kolorowania(self):
        statystyki = self.stat.statystyki()
        self.assertEqual(6, statystyki['liczba_wierzcholkow'])
        self.assertEqual(7, statystyki['liczba_krawedzi'])
        self.assertEqual(6, statystyki['max_kolor'])
        self.assertAlmostEqual(0.477777777778, statystyki['sredni_wspolczynnik_klasteryzacji'], delta=0.0000001)
        self.assertAlmostEqual(2.3333333333333335, statystyki['sredni_stopien_wierzcholka'], delta=0.0000001)
        self.assertAlmostEqual(1.2777777777777777, statystyki['srednia_dlugosc_sciezki'], delta=0.0000001)


class KolorowanieTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        wzorzec_po = 'dane_testowe/wzorzec_po.dot'
        cls.k_po = Kolorowanie(wzorzec_po)
        cls.v1_po = list(cls.k_po.graph.vertices())[1]
        cls.v0_po = list(cls.k_po.graph.vertices())[0]

        cls.wzorzec_przed = 'dane_testowe/wzorzec_przed.dot'
        cls.k_przed = Kolorowanie(cls.wzorzec_przed)
        cls.v1_przed = list(cls.k_przed.graph.vertices())[1]

        cls.wzorzec_zly_iloczyn = 'dane_testowe/wzorzec_zly_iloczyn_po.dot'
        cls.k_zly_iloczyn = Kolorowanie(cls.wzorzec_zly_iloczyn)
        cls.v1_zly_iloczyn = list(cls.k_zly_iloczyn.graph.vertices())[1]

        cls.wzorzec_zly_niecialgy_przedzial = 'dane_testowe/wzorzec_zly_nieciagly_przedzial_po.dot'
        cls.k_zly_przedzial = Kolorowanie(cls.wzorzec_zly_niecialgy_przedzial)
        cls.v1_zly_przedzial = list(cls.k_zly_przedzial.graph.vertices())[1]

        cls.wzorzec_bez_wlasciwosci = 'dane_testowe/wzorzec_bez_wlasciwosci.dot'
        cls.k_bez_wl = Kolorowanie(cls.wzorzec_bez_wlasciwosci)
        cls.v1_bez_wl = list(cls.k_bez_wl.graph.vertices())[1]

        cls.wzorzec_po_niepelny = 'dane_testowe/wzorzec_po_niepelny.dot'
        cls.k_niepelny= Kolorowanie(cls.wzorzec_po_niepelny)
        cls.v5_niepelny = list(cls.k_niepelny.graph.vertices())[5]
        cls.v0_niepelny = list(cls.k_niepelny.graph.vertices())[0]
        cls.v1_niepelny = list(cls.k_niepelny.graph.vertices())[1]

        cls.wzorzec_duze_przed = 'dane_testowe/duze_przed.dot'
        cls.k_duze_przed = Kolorowanie(cls.wzorzec_duze_przed)

        cls.wzorzec_duze_po = 'dane_testowe/duze_po.dot'
        cls.k_duze_po = Kolorowanie(cls.wzorzec_duze_po)

    def test_liczba_kolorow_pass(self):
        self.assertEqual(3, int(self.k_przed._liczba_kolorow(self.v1_przed)))

    def test_liczba_kolorow_fail(self):
        self.assertRaises(PropertyError, self.k_bez_wl._liczba_kolorow, self.v1_bez_wl)

    def test_przypisane_kolory_pass(self):
        self.assertEqual([1,2,3], self.k_po._przypisane_kolory(self.v1_po))

    def test_przypisane_kolory_fail(self):
        self.assertRaises(PropertyError, self.k_przed._przypisane_kolory, self.v1_przed)

    def test_przypisane_kolory_puste(self):
        self.assertEqual(0,len(self.k_niepelny._przypisane_kolory(self.v5_niepelny)))

    def test_sprawdzenie_pass(self):
        self.assertTrue(self.k_po.sprawdzenie())

    def test_sprawdzenie_fail_iloczyn(self):
        self.assertRaises(IloczynNiePustyWezlow, self.k_zly_iloczyn.sprawdzenie)

    def test_sprawdzenie_fail_przedzial(self):
        self.assertRaises(CiagloscErrorWezla, self.k_zly_przedzial.sprawdzenie)

    # @unittest.skip('')
    # def test_zapisz(self):
    #     self.k_po.zapisz('test_zapis')
    #
    # @unittest.skip('')
    # def test_zapisz_z_pusta_lista_przypisanych_kolorow(self):
    #     k = Kolorowanie(self.wzorzec_przed)
    #     k._dodaj_i_inicjuj_wlasciwosc_przypisane_kolory()
    #     k.zapisz('test_zapis2')

    def test_dodaj_wlasciwosc_przypisane_kolory(self):
        k = Kolorowanie(self.wzorzec_przed)
        k._dodaj_i_inicjuj_wlasciwosc_przypisane_kolory()
        v1 = list(k.graph.vertices())[1]
        self.assertEqual([], k.graph.vertex_properties['przypisane_kolory'][v1])

    def test_sortuj_liczba_kolorow(self):
        k = Kolorowanie(self.wzorzec_przed)
        lista_wierzch = list(k.graph.vertices())
        k._sortuj_liczba_kolorow(lista_wierzch)
        po = [int(str(v)) for v in lista_wierzch]
        self.assertEqual([1,2,3,0,4,5], po)

    def test_sortuj_stopien(self):
        k = Kolorowanie(self.wzorzec_przed)
        lista_wierzch = list(k.graph.vertices())
        k._sortuj_stopien(lista_wierzch)
        po = [int(str(v)) for v in lista_wierzch]
        self.assertEqual([1,0,2,4,3,5], po)

    def test_suma_kolorow_sasiadow(self):
        self.assertEqual(6, self.k_po._suma_kolorow_sasiadow(self.v0_po))
        self.assertEqual(7, self.k_po._suma_kolorow_sasiadow(self.v1_po))

    def test_suma_kolorow_sasiadow2(self):
        self.assertEqual(3, self.k_niepelny._suma_kolorow_sasiadow(self.v5_niepelny))
        self.assertEqual(2, self.k_niepelny._suma_kolorow_sasiadow(self.v1_niepelny))

    def test_sortuj_suma_przypisanych_kolorow_sasiadow(self):
        k = Kolorowanie(self.wzorzec_po_niepelny)
        lista_wezlow = list(k.graph.vertices())
        k._sortuj_suma_przypisanych_kolorow_sasiadow(lista_wezlow)
        po = [int(str(v)) for v in lista_wezlow]
        self.assertEqual([0,2,3,4,5,1], po)

    def test_listy_przypisanych_kolorow_sasiadow(self):
        self.assertEqual([[4,5],[4],[1,2,3]], self.k_po._listy_przypisanych_kolorow_sasiadow(self.v0_po))

    def test_zbior(self):
        self.assertEqual(set([1,2,3,4,5,7,8]), self.k_po._zbior([[4,5],[7,8],[1,2,3]]))

    def test_znajdz_dziure(self):
        zbior = set([3,4,7,8,10])
        self.assertEqual([[1, 2], [5, 6], [9]], list(self.k_po._generuj_dziure(zbior)))

    def test_znajdz_dziure2(self):
        zbior = set([1,2,3,4,7,8,10])
        self.assertEqual([[5, 6], [9]], list(self.k_po._generuj_dziure(zbior)))

    def test_znajdz_dziure3(self):
        zbior = set([1, 2, 3, 4, 7, 8, 9, 10])
        self.assertEqual([[5, 6]], list(self.k_po._generuj_dziure(zbior)))

    def test_znajdz_dziure4(self):
        zbior = set([1,2,3,4])
        self.assertEqual([],  list(self.k_po._generuj_dziure(zbior)))

    def test_znajdz_dziure5(self):
        zbior = set() #czyli wszyscy sasiedzi jeszcze pusci
        self.assertEqual([], list(self.k_po._generuj_dziure(zbior)))

    def test_koloruj_wierzcholek(self):
        self.assertEqual([1,2,3], self.k_po._koloruj_wierzcholek(self.v1_po))

    def test_koloruj_wierzcholek2(self):
        self.assertEqual([6], self.k_po._koloruj_wierzcholek(self.v0_po))

    def test_koloruj_wierzcholek3(self):
        k = Kolorowanie(self.wzorzec_przed)
        k._dodaj_i_inicjuj_wlasciwosc_przypisane_kolory()
        v0_przed = list(k.graph.vertices())[0]
        self.assertEqual([1], k._koloruj_wierzcholek(v0_przed))

    def test_koloruj_wierzcholek4(self):
        k = Kolorowanie(self.wzorzec_przed)
        k._dodaj_i_inicjuj_wlasciwosc_przypisane_kolory()
        v3_przed = list(k.graph.vertices())[3]
        self.assertEqual([1,2], k._koloruj_wierzcholek(v3_przed))

    def test_koloruj(self):
        k = Kolorowanie(self.wzorzec_przed)
        k.koloruj()
        self.assertEqual(True, k.sprawdzenie())

    def test_koloruj2(self):
        k = Kolorowanie(self.wzorzec_po_niepelny)
        k.koloruj()
        self.assertEqual(True, k.sprawdzenie())

    def test_koloruj3(self):
        k = Kolorowanie(self.wzorzec_zly_iloczyn)
        k.koloruj()
        # k.zapisz("dupa_po")
        self.assertEqual(True, k.sprawdzenie())

    def test_statystyki_z_pliku_po_kolorowaniu_duze(self):
        statystyki = self.k_duze_po.statystyki()
        self.assertEqual(30, statystyki['liczba_wierzcholkow'])
        self.assertEqual(61, statystyki['liczba_krawedzi'])
        self.assertEqual(16, statystyki['max_kolor'])
        self.assertAlmostEqual(0.0588888888889, statystyki['sredni_wspolczynnik_klasteryzacji'], delta=0.0000001)
        self.assertAlmostEqual(4.06666666667, statystyki['sredni_stopien_wierzcholka'], delta=0.0000001)
        self.assertAlmostEqual(2.41333333333, statystyki['srednia_dlugosc_sciezki'], delta=0.0000001)
        self.assertAlmostEqual(2.96666666667, statystyki['srednia_liczba_kolorow'], delta=0.0000001)

    def test_statystyki_odrazu_po_kolorowaniu_duze(self):
        k = Kolorowanie(self.wzorzec_duze_przed)
        k.koloruj()
        statystyki = k.statystyki()
        self.assertEqual(30, statystyki['liczba_wierzcholkow'])
        self.assertEqual(61, statystyki['liczba_krawedzi'])
        self.assertEqual(16, statystyki['max_kolor'])
        self.assertAlmostEqual(0.0588888888889, statystyki['sredni_wspolczynnik_klasteryzacji'], delta=0.0000001)
        self.assertAlmostEqual(4.06666666667, statystyki['sredni_stopien_wierzcholka'], delta=0.0000001)
        self.assertAlmostEqual(2.41333333333, statystyki['srednia_dlugosc_sciezki'], delta=0.0000001)
        self.assertAlmostEqual(2.96666666667, statystyki['srednia_liczba_kolorow'], delta=0.0000001)

    def test_sprawdzenie_z_pliku_po_kolorowaniu_duze(self):
        k = Kolorowanie(self.wzorzec_duze_po)
        self.assertTrue(k.sprawdzenie())

    def test_sprawdzenie_odrazu_po_kolorowaniu_duze(self):
        k = Kolorowanie(self.wzorzec_duze_przed)
        k.koloruj()
        self.assertTrue(k.sprawdzenie())




