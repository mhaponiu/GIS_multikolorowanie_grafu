import json

from gis_tool import generuj
from kolorowanie import Kolorowanie
import logging, time

def name(n, e, c):
    return '_'.join(['n', str(n), 'e', str(e), 'c', str(c)])

n_od = 5
n_do = 5005
n_krok = 50

e_od = 2
e_do = 52
e_krok = 5

c_od = 2
c_do = 22
c_krok = 4


# n_od = 50
# n_do = 150
# n_krok = 50
# e_od = 5
# e_do = 15
# e_krok = 5
# c_od = 2
# c_do = 10
# c_krok = 4

start = time.time()

for n in range(n_od, n_do+1, n_krok):
    for e in range(e_od, e_do+1, e_krok):
        for c in range(c_od, c_do+1, c_krok):
            g = generuj(n, e, c)
            sciezka = 'profile_data/'+name(n,e,c)
            g.save(sciezka+'.dot')
            k = Kolorowanie(sciezka+'.dot')
            t_start = time.time()
            k.koloruj()
            t_end = time.time()
            t_delta = t_end - t_start
            stat = k.statystyki()
            slownik = {'czas': t_delta}
            slownik['statystyki'] = stat
            with open(sciezka+'.stat', 'wt') as f:
                json.dump(slownik, f, indent=4)

            print '\t\t', str(float(c) / c_do * 100) + '%'
        print '\t', str(float(e) / e_do * 100) + '%'
    print str(float(n) / n_do * 100) + '%'

stop = time.time()

print '\n\tKONIEC -> laczny czas wykonania: ' + str(stop - start) + ' s'