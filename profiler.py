
import json, os
from scipy.odr.odrpack import odr_stop

from gis_tool import generuj
from kolorowanie import Kolorowanie
import logging, time

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def name(n, e, c):
    return '_'.join(['n', str(n), 'e', str(e), 'c', str(c)])

# n_od = 50
# n_do = 150
# n_krok = 50
# e_od = 5
# e_do = 15
# e_krok = 5
# c_od = 2
# c_do = 10
# c_krok = 4


# logging.basicConfig(level=logging.INFO)
#
# start = time.time()
#
# for n in range(n_od, n_do+1, n_krok):
#     for e in range(e_od, e_do+1, e_krok):
#         for c in range(c_od, c_do+1, c_krok):
#             g = generuj(n, e, c)
#             sciezka = 'profile_data/'+name(n,e,c)
#             g.save(sciezka+'.dot')
#             k = Kolorowanie(sciezka+'.dot')
#             t_start = time.time()
#             k.koloruj()
#             t_end = time.time()
#             t_delta = t_end - t_start
#             stat = k.statystyki()
#             slownik = {'czas': t_delta}
#             slownik['statystyki'] = stat
#             with open(sciezka+'.stat', 'wt') as f:
#                 json.dump(slownik, f, indent=4)
#
#             print '\t\t', str(float(c) / c_do * 100) + '%'
#         print '\t', str(float(e) / e_do * 100) + '%'
#     print str(float(n) / n_do * 100) + '%'
#
#
# stop = time.time()

def profiluj():
    n_od = 5
    n_do = 1405
    n_krok = 200

    e_od = 10
    e_do = 50
    e_krok = 40
    e = 50

    c_od = 4
    c_do = 4
    c_krok = 1

    e = 10
    c = 4

    logging.basicConfig(level=logging.INFO)

    start = time.time()

    for n in range(n_od, n_do + 1, n_krok):
        g = generuj(n, e, c)
        sciezka = 'profile_data/' + name(n, e, c)
        g.save(sciezka + '.dot')
        k = Kolorowanie(sciezka + '.dot')
        t_start = time.time()
        k.koloruj()
        t_end = time.time()
        t_delta = t_end - t_start
        stat = k.statystyki()
        slownik = {'czas': t_delta}
        slownik['statystyki'] = stat
        with open(sciezka + '.stat', 'wt') as f:
            json.dump(slownik, f, indent=4)
        print '\t' + str(float(n) / n_do * 100) + '%'

    e = 50
    c = 4

    for n in range(n_od, n_do + 1, n_krok):
        g = generuj(n, e, c)
        sciezka = 'profile_data/' + name(n, e, c)
        g.save(sciezka + '.dot')
        k = Kolorowanie(sciezka + '.dot')
        t_start = time.time()
        k.koloruj()
        t_end = time.time()
        t_delta = t_end - t_start
        stat = k.statystyki()
        slownik = {'czas': t_delta}
        slownik['statystyki'] = stat
        with open(sciezka + '.stat', 'wt') as f:
            json.dump(slownik, f, indent=4)
        print '\t' + str(float(n) / n_do * 100) + '%'

    e = 50
    c = 15

    for n in range(n_od, n_do + 1, n_krok):
        g = generuj(n, e, c)
        sciezka = 'profile_data/' + name(n, e, c)
        g.save(sciezka + '.dot')
        k = Kolorowanie(sciezka + '.dot')
        t_start = time.time()
        k.koloruj()
        t_end = time.time()
        t_delta = t_end - t_start
        stat = k.statystyki()
        slownik = {'czas': t_delta}
        slownik['statystyki'] = stat
        with open(sciezka + '.stat', 'wt') as f:
            json.dump(slownik, f, indent=4)
        print '\t' + str(float(n) / n_do * 100) + '%'

    stop = time.time()

    print '\n\tKONIEC -> laczny czas wykonania: ' + str(stop - start) + ' s'

def rysuj(e, c, kolor_wykresu):
    data_dir = 'profile_data'
    e_n = "e_" + str(e)
    c_n = "c_" + str(c)
    files =  os.listdir(data_dir)
    files_e10 = [file for file in files if e_n in file and '.stat' in file and c_n in file]
    files_e10.sort(key=lambda a: int(a.split('_')[1]))
    liczba_wierzcholkow = []
    czas = []
    for file in files_e10:
        with open('/'.join([data_dir, file])) as f:
            slownik = json.load(f)
            liczba_wierzcholkow.append(slownik['statystyki']['liczba_wierzcholkow'])
            czas.append(slownik['czas'])
    print liczba_wierzcholkow
    print czas

    plt.ylabel('czas [s]')
    plt.xlabel('liczba wezlow')
    # plt.title("sredni stopien wierzcholka: "+str(e)+'\nkolorow max ' + str(c))
    plt.plot(liczba_wierzcholkow, czas, kolor_wykresu)
    # plt.plot(czas, liczba_wierzcholkow, kolor_wykresu)

    # red_patch = mpatches.Patch(color='green', label='The red data')
    # plt.legend(handles=[red_patch])

    # plt.show()
    # plt.savefig('_'.join([e_n, c_n]))


def produkuj_rysunek(output):
    rysuj(e=10, c=4, kolor_wykresu='r.-')
    red_patch = mpatches.Patch(color='red', label='e srednie: 10\nmax kolor 4')
    # plt.legend(handles=[red_patch])

    rysuj(e=50, c=4, kolor_wykresu='g.-')
    green_patch = mpatches.Patch(color='green', label='e srednie: 50\nmax kolor: 4')

    rysuj(e=50, c=15, kolor_wykresu='y.-')
    yellow_patch = mpatches.Patch(color='yellow', label='e srednie: 50\nmax kolor: 15')

    plt.legend(handles=[red_patch, green_patch, yellow_patch], loc=2)

    plt.savefig("zestawienie_nowe")



if __name__ == '__main__':
    profiluj()
    produkuj_rysunek("zestawienie_nowe")
    # czas wykonania okolo 3h
