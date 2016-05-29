import unittest
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

    def test_ciaglosc_przedzialu_1(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([1, 2, 3]), True)

    def test_ciaglosc_przedzialu_2(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([1, 3]), False)

    def test_ciaglosc_przedzialu_3(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([3, 3]), False)

    def test_ciaglosc_przedzialu_4(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([4, 3]), True)

    def test_ciaglosc_przedzialu_5(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([4]), True)

    def test_ciaglosc_przedzialu_6(self):
        self.assertEqual(self.spr._ciaglosc_przedzialu([3, 1]), False)

    def test_przypisane_kolory(self):
        v1 = list(self.k.graph.vertices())[1]
        self.assertEqual(set(self.spr._przypisane_kolory(v1)), set([1,2,3]))



