from graph_tool.all import *

g=Graph(directed=False)

v0 = g.add_vertex()
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()
v5 = g.add_vertex()

# addVertexPopeties('liczba_kolorow', 'int')

g.vertex_properties['liczba_kolorow'] = g.new_vertex_property('int')

g.vertex_properties['liczba_kolorow'][v0] = 1
g.vertex_properties['liczba_kolorow'][v1] = 3
g.vertex_properties['liczba_kolorow'][v2] = 2
g.vertex_properties['liczba_kolorow'][v3] = 2
g.vertex_properties['liczba_kolorow'][v4] = 1
g.vertex_properties['liczba_kolorow'][v5] = 1

g.add_edge(v0, v1)
g.add_edge(v1, v2)
g.add_edge(v1, v3)
g.add_edge(v2, v0)
g.add_edge(v1, v5)
g.add_edge(v4, v0)
g.add_edge(v4, v1)


g.save('przed.dot', 'dot')
g.save('przed.graphml', 'graphml')
# g.save('przed.gml', 'gml')

g2=Graph(g)

g.vertex_properties['wyswietlany_tekst'] = g.new_vertex_property('string')

for v in g.vertices():
    g.vertex_properties['wyswietlany_tekst'][v]= v.__str__() + ': ' + str(g.vertex_properties['liczba_kolorow'][v])

graph_draw(g, vertex_text=g.vertex_properties['wyswietlany_tekst']
           , bg_color = [255.,255.,255.,1]
           , output_size=(600,600)
           , output='przed.png')


g2.vertex_properties['przypisane_kolory'] = g.new_vertex_property('vector<int>')

g2.vertex_properties['przypisane_kolory'][v0] = [6]
g2.vertex_properties['przypisane_kolory'][v1] = [1,2,3]
g2.vertex_properties['przypisane_kolory'][v2] = [4,5]
g2.vertex_properties['przypisane_kolory'][v3] = [4,5]
g2.vertex_properties['przypisane_kolory'][v4] = [4]
g2.vertex_properties['przypisane_kolory'][v5] = [4]

g2.save('po.dot', 'dot')
g2.save('po.graphml', 'graphml')

gx = load_graph('po.dot','dot')
gx.save('after_load.dot', 'dot')
gx = load_graph('po.graphml', 'graphml')
gx.save('after_load.graphml', 'graphml')

# g2 = load_graph('po.graphtml')

# RYSOWANIE WYNIKOWEGO GRAFU
g2.vertex_properties['wyswietlany_tekst'] = g.new_vertex_property('string')

for v in g2.vertices():
    g2.vertex_properties['wyswietlany_tekst'][v]= v.__str__() + ': ' + \
                                                 str(g2.vertex_properties['liczba_kolorow'][v]) + \
                                                 str(list(g2.vertex_properties['przypisane_kolory'][v]))
graph_draw(g2, vertex_text=g2.vertex_properties['wyswietlany_tekst']
           , bg_color=[255., 255., 255., 1]
           , output_size=(600, 600)
           , output="po.png"
           )