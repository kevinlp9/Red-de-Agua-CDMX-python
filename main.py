#librerias necesaria para visualizar y exportar grafos
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_excel('agua.xlsx', index_col=None)
### los datos se importaron correctamente
df.head()

###agua toma los datos de agua.xlsx y le agrega variables
AGUA = nx.from_pandas_edgelist(df,source='Origen',target='Destino',edge_attr='Longitud de tuberia',create_using=nx.DiGraph())

###muestra los nodos 
AGUA.nodes()

###muestra las aristas
AGUA.edges()

###cantidad de nodos
AGUA.order()

suministros = []
consumidores = []
###muestra los lugares con mas de dos tuberias
for x in AGUA.nodes():
    if AGUA.in_degree(x)>1:
        print(x)
        consumidores.append(x);
    
    if AGUA.in_degree(x)==0:
        suministros.append(x);


# Calcular el camino más corto utilizando Dijkstra
djk_path = nx.dijkstra_path(AGUA, source='San Bartolo', target='San Juan de Letrán', weight=True)

# Crear una nueva instancia de un grafo dirigido
grafo_exportar = nx.DiGraph()

# Agregar los nodos y aristas del camino más corto al nuevo grafo
for i in range(len(djk_path)-1):
    source = djk_path[i]
    target = djk_path[i+1]
    weight=True
    grafo_exportar.add_edge(source, target, weight=weight)

# Exportar el grafo y el camino más corto a un archivo gephi
nx.write_graphml(grafo_exportar, "grafo_rutacorta.gexf")

# Exportar el grafo completo a gephi
nx.write_gexf(AGUA, "grafo_completo.gexf", version="1.2draft")
indice=0
for nodo in consumidores:
    
    djk_paths = nx.multi_source_dijkstra(AGUA,suministros,target=nodo,weight=True)
    grafo_n = nx.DiGraph()

    for j in range(len(djk_paths[1])-1):
        source = djk_paths[1][j]
        target = djk_paths[1][j+1]
        weight=True
        grafo_n.add_edge(source, target, weight=weight)
    
    nx.write_graphml(grafo_n, "grafo_rutacorta_"+str(indice)+".gexf")
    indice=indice+1