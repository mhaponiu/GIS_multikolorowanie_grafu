
class GISBaseException(Exception):
    pass

class CiagloscError(GISBaseException):
    def __init__(self, przedzial):
        self.przedzial = przedzial

    def __str__(self):
        return "Przedzial " + str(self.przedzial) + " nie jest ciagly"

class CiagloscErrorWezla(CiagloscError):
    def __init__(self, wezel, przedzial):
        super(CiagloscError, self).__init__(przedzial)
        self.przedzial = przedzial
        self.wezel = wezel

    def __str__(self):
        return "Wezel " + str(self.wezel) + " ma nieciagly przedzial " + str(self.przedzial)

class IloczynNiePusty(GISBaseException):
    def __init__(self, zbior):
        self.zbior = zbior

    def __str__(self):
        return "Iloczyn zbiorow nie jest pusty: " + str(self.zbior)

class IloczynNiePustyWezlow(IloczynNiePusty):
    def __init__(self, zbior, wezel1, wezel2):
        super(IloczynNiePusty, self).__init__(zbior)
        self.wezel1 = wezel1
        self.wezel2 = wezel2
        self.zbior = zbior

    def __str__(self):
        return ' '.join(['Wezly', str(self.wezel1), 'i', str(self.wezel2),
                         'maja czesc wspolna:', str(self.zbior)])

class PropertyError(GISBaseException):
    def __init__(self, wierzcholek, wlasciwosc):
        self.wierzcholek = wierzcholek
        self.wlasciwosc = wlasciwosc

    def __str__(self):
        return "Brak w wezle " + str(self.wierzcholek) + " wlasciwosci: '" + self.wlasciwosc + "'"

class LiczebnoscKolorowError(GISBaseException):
    def __init__(self, wezel, powinno_byc, jest):
        self.powinno_byc = powinno_byc
        self.jest = jest
        self.wezel = wezel

    def __str__(self):
        return "W wezle " + str(self.wezel) + " przypisano " + str(self.jest) + '  kolory, a powinno byc ' + str(self.powinno_byc)
