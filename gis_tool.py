import argparse
import sys
from graph_tool.all import random_graph, Graph, load_graph, graph_draw
from graph_tool.stats import remove_parallel_edges
from numpy.random import randint


def rysuj_wynik(input_file, output=None, size=(600, 600)):
    rozszerzenie = input_file.split('.')[1]
    g2 = load_graph(input_file)
    g2.vertex_properties['wyswietlany_tekst'] = g2.new_vertex_property('string')

    if rozszerzenie == 'dot':
        for v in g2.vertices():
            g2.vertex_properties['wyswietlany_tekst'][v] = v.__str__() + ': ' + \
                                                           g2.vertex_properties['liczba_kolorow'][v] + \
                                                           '[' + g2.vertex_properties['przypisane_kolory'][v] + ']'
    elif rozszerzenie == 'xml' or 'graphml':
        for v in g2.vertices():
            g2.vertex_properties['wyswietlany_tekst'][v] = v.__str__() + ': ' + \
                                                           str(g2.vertex_properties['liczba_kolorow'][v]) + \
                                                           str(list(g2.vertex_properties['przypisane_kolory'][v]))

    graph_draw(g2, vertex_text=g2.vertex_properties['wyswietlany_tekst']
               , bg_color=[255., 255., 255., 1]
               , output_size=size
               , output=output
               )


def rysuj_wejscie(input_file, output=None, size=(600, 600)):
    rozszerzenie = input_file.split('.')[1]
    g2 = load_graph(input_file)
    g2.vertex_properties['wyswietlany_tekst'] = g2.new_vertex_property('string')

    if rozszerzenie == 'dot':
        for v in g2.vertices():
            g2.vertex_properties['wyswietlany_tekst'][v] = v.__str__() + ': ' + \
                                                           g2.vertex_properties['liczba_kolorow'][v]
    elif rozszerzenie == 'xml' or 'graphml':
        for v in g2.vertices():
            g2.vertex_properties['wyswietlany_tekst'][v] = v.__str__() + ': ' + \
                                                           str(g2.vertex_properties['liczba_kolorow'][v])

    graph_draw(g2, vertex_text=g2.vertex_properties['wyswietlany_tekst']
               , bg_color=[255., 255., 255., 1]
               , output_size=size
               , output=output
               )


# rysuj_wynik(input='po.dot', output='loaddot.png', size=(600,600))
# rysuj_wynik(input='po.graphml', output='loadgraphml.png', size=(600,600))

# rysuj_wejscie(input='przed.graphml', output='wejscie_graphml.png', size=(600,600) )
# rysuj_wejscie(input='przed.dot', output='wejscie_dot.png', size=(600,600) )

def rysuj_graf_wejsciowy(g, output=None, size=(600, 600), bez_napisow=False):
    gx = Graph(g)
    gx.vertex_properties['wyswietlany_tekst'] = gx.new_vertex_property('string')

    for v in gx.vertices():
        gx.vertex_properties['wyswietlany_tekst'][v] = v.__str__() + ': ' + \
                                                       str(gx.vertex_properties['liczba_kolorow'][v])
    if bez_napisow:
        graph_draw(gx
                   # , vertex_text=gx.vertex_properties['wyswietlany_tekst']
                   , bg_color=[255., 255., 255., 1]
                   , output_size=size
                   , output=output
                   )
    else:
        graph_draw(gx
                   , vertex_text=gx.vertex_properties['wyswietlany_tekst']
                   , bg_color=[255., 255., 255., 1]
                   , output_size=size
                   , output=output
                   )


def generuj(n, rand_edges, num_colors):
    if rand_edges < 3: rand_edges = 3
    g = random_graph(n, (lambda: (randint(0, rand_edges), randint(1, rand_edges))), parallel_edges=False)
    g.set_directed(False)
    remove_parallel_edges(g)

    g.vertex_properties['liczba_kolorow'] = g.new_vertex_property('int')
    for v in g.vertices():
        g.vertex_properties['liczba_kolorow'][v] = randint(1, num_colors + 1)

    return g


# g = generuj(n=10, rand_edges=4, num_colors=3)
# rysuj_graf_wejsciowy(g, size=(1920,1080))

if __name__ == '__main__':
    #     https: // docs.python.org / 2 / library / argparse.html  # other-utilities
    akcje = ['generuj', 'rysuj_we', 'rysuj_wy']
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    subparsers = parser.add_subparsers(help='tryby pracy, [tryb] --help for more info')

    gen_parser = subparsers.add_parser('generuj', help='generuje graf wejsciowy')
    gen_parser.add_argument('Output_file', help="nazwa pliku wynikowego, (type: %(type)s)"
                            , type=str)
    gen_parser.add_argument('-N', help="liczba wezlow (default: %(default)s, type: %(type)s)"
                            , type=int, default=10, metavar='n')
    gen_parser.add_argument('-E', '--edges',
                            help="~max liczba wylosowanych krawedzi dla wezla (default: %(default)s, type: %(type)s)"
                            , type=int, default=4, metavar='e')
    gen_parser.add_argument('-C', '--colors',
                            help="max liczba wylosowanych kolorow dla wezla (default: %(default)s, type: %(type)s)"
                            , type=int, default=3, metavar='c')

    rysuj_we_parser = subparsers.add_parser('rysuj_we', help='rysuje graf wejsciowy')
    rysuj_we_parser.add_argument('Input', help="nazwa pliku wejsciowego do kolorowania (type: %(type)s)"
                                 , type=str)
    rysuj_we_parser.add_argument('-bn', '--bez_napisow', help='nie rysuje teksu wewnatrz wezla', action='store_true')

    rysuj_wy_parser = subparsers.add_parser('rysuj_wy', help='rysuje graf wynikowy')
    rysuj_wy_parser.add_argument('Input', help="nazwa pliku wynikowego pokolorowanego (type: %(type)s)"
                                 , type=str)

    # musze przeiterowac po parserach i pododawac bo inaczej nie mozna na koncu wiersza podac '-I', tylko trzeba na poczatku
    for subparser in subparsers.choices.items():
        # print subparser
        subparser[1].add_argument('-I', '--interactive'
                                  , help='wlacza interaktywny tryb przegladania grafu'
                                  , action='store_true')
        subparser[1].add_argument('-PNG'
                                  , nargs=2
                                  , metavar=('w', 'h')
                                  , help='drukuje plik png o nazwie argumentu pozycyjnego')

    argumenty = sys.argv
    zparsowane = parser.parse_args()
    # print zparsowane

    if 'generuj' in argumenty:
        g = generuj(zparsowane.N, zparsowane.edges, zparsowane.colors)
        # g.save(zparsowane.Output_file+'.graphml')
        save_name = zparsowane.Output_file
        domyslny_format = '.dot'  # ewentualnie '.graphml'
        posplitowane = save_name.split('.')
        if len(posplitowane) == 1:
            save_name = save_name + domyslny_format
        else:
            save_name = ('_').join(posplitowane[:-1])
            if posplitowane[-1] == 'dot':
                save_name = save_name + '.dot'
            else:
                save_name = save_name + '.xml'
        g.save(save_name)

        if zparsowane.PNG:
            rysuj_graf_wejsciowy(g, zparsowane.Output_file + '.png',
                                 size=(int(zparsowane.PNG[0]), int(zparsowane.PNG[1])))

        if zparsowane.interactive:
            rysuj_graf_wejsciowy(g)

    elif 'rysuj_we' in argumenty:
        g = load_graph(zparsowane.Input)
        file_name = zparsowane.Input.split('.')[0]

        if zparsowane.PNG:
            rysuj_graf_wejsciowy(g, file_name + '.png'
                                 , size=(int(zparsowane.PNG[0]), int(zparsowane.PNG[1]))
                                 , bez_napisow=zparsowane.bez_napisow)
        if zparsowane.interactive:
            rysuj_graf_wejsciowy(g, bez_napisow=zparsowane.bez_napisow)

    elif 'rysuj_wy' in argumenty:
        file_name = zparsowane.Input.split('.')[0]

        if zparsowane.PNG:
            rysuj_wynik(zparsowane.Input
                        , file_name + '.png'
                        , size=(int(zparsowane.PNG[0]), int(zparsowane.PNG[1])))
        if zparsowane.interactive:
            rysuj_wynik(zparsowane.Input)
