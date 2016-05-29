import unittest

from Errors import CiagloscError, IloczynNiePusty, GISBaseException, IloczynNiePustyWezlow, CiagloscErrorWezla
from kolorowanie import Kolorowanie, Sprawdzenie

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
        cls.wzorzec_po = 'dane_testowe/wzorzec_po.dot'
        cls.k = Kolorowanie(cls.wzorzec_po)
        cls.spr = Sprawdzenie(graph=cls.k.graph)

        cls.wzorzec_zly_iloczyn_po = 'dane_testowe/wzorzec_zly_iloczyn_po.dot'
        cls.k_zly_iloczyn = Kolorowanie(file_input=cls.wzorzec_zly_iloczyn_po)
        cls.spr_zly_iloczyn = Sprawdzenie(graph=cls.k_zly_iloczyn.graph)

        cls.wzorzec_zly_nieciagly_przdzial_po = 'dane_testowe/wzorzec_zly_nieciagly_przedzial_po.dot'
        cls.k_zly_nieciagly_przedzial = Kolorowanie(file_input=cls.wzorzec_zly_nieciagly_przdzial_po)
        cls.spr_zly_nieciagly_przedzial = Sprawdzenie(graph=cls.k_zly_nieciagly_przedzial.graph)

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
        v1 = list(self.k.graph.vertices())[1]
        self.assertEqual(set(self.spr._przypisane_kolory(v1)), set([1,2,3]))

    def test_sprawdz_wezel1(self):
        v1 = list(self.k.graph.vertices())[1] #kolory 1,2,3
        self.assertTrue(self.spr._sprawdz_wezel(v1, set([])))

    def test_sprawdz_wezel2(self):
        v1 = list(self.k.graph.vertices())[1] #kolory 1,2,3
        self.assertRaises(IloczynNiePusty,
                          self.spr._sprawdz_wezel,
                          v1, set([1]))

    def test_sprawdz_wezel3(self):
        v1 = list(self.k.graph.vertices())[1] #kolory 1,2,3
        self.assertRaises(IloczynNiePusty,
                          self.spr._sprawdz_wezel,
                          v1, set([3,4,5]))

    def test_sprawdz_wezel4(self):
        v1 = list(self.k.graph.vertices())[1] #kolory 1,2,3
        self.assertTrue(self.spr._sprawdz_wezel(v1, set([4, 5])))


    def test_sprawdz_sasiadow(self):
        v1 = list(self.k.graph.vertices())[1]  # kolory 1,2,3
        self.spr._sprawdz_sasiadow(v1)

    def test_sprawdz_sasiadow2(self):
        v1 = list(self.k_zly_iloczyn.graph.vertices())[1]  # kolory 1,2,3,4
        self.assertRaises(IloczynNiePusty,
                          self.spr_zly_iloczyn._sprawdz_sasiadow, v1)

    def test_sprawdz_sasiadow3(self):
        v2 = list(self.k_zly_iloczyn.graph.vertices())[2]  # kolory 4,5
        self.assertRaises(IloczynNiePusty,
                          self.spr_zly_iloczyn._sprawdz_sasiadow, v2)

    def test_sprawdz_sasiadow4(self):
        v0 = list(self.k_zly_iloczyn.graph.vertices())[0]  # kolory 6
        self.assertTrue(self.spr_zly_iloczyn._sprawdz_sasiadow(v0))

    def test_sprawdz_dobry(self):
        self.assertTrue(self.spr.sprawdz())

    def test_sprawdz_zly_iloczyn(self):
        self.assertRaises(IloczynNiePustyWezlow, self.spr_zly_iloczyn.sprawdz)
        # self.spr_zly_iloczyn.sprawdz()

    def test_sprawdz_zly_nieciagly_przedzial(self):
        self.assertRaises(CiagloscErrorWezla, self.spr_zly_nieciagly_przedzial.sprawdz)
        # self.spr_zly_nieciagly_przedzial.sprawdz()

