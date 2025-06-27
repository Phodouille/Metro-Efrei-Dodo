import os
import networkx as nx
import matplotlib.pyplot as plt
from graph_parser import load_graph_from_pickle

def kruskal(graph):
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            parent[root_y] = root_x
            return True
        return False

    for node in graph:
        parent[node] = node

    edges = []
    seen = set()
    for u in graph:
        for v, _, w in graph[u]:
            if u != v:
                edge_key = tuple(sorted([u, v])) + (w,)
                if edge_key not in seen:
                    seen.add(edge_key)
                    edges.append((u, v, w))

    edges.sort(key=lambda x: x[2])

    mst = []
    for u, v, w in edges:
        if union(u, v):
            mst.append((u, v, w))

    return mst

def visualize_mst(mst, station_names):
    G = nx.Graph()
    for u, v, w in mst:
        name_u = station_names.get(u, u)
        name_v = station_names.get(v, v)
        G.add_edge(name_u, name_v, weight=w)

    pos = nx.spring_layout(G, k=0.25, iterations=100)
    plt.figure(figsize=(30, 30))
    nx.draw(G, pos, with_labels=True, node_size=30, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Arbre couvrant minimal du réseau métro parisien (Kruskal)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pickle_path = os.path.join(base_dir, "..", "data", "metro_graph.pkl")

    graph, station_names, _ = load_graph_from_pickle(pickle_path)
    mst = kruskal(graph)

    print("Arbre couvrant minimal (ACPM - Kruskal) :")
    for u, v, w in mst:
        print(f"{station_names[u]} ↔ {station_names[v]} : {int(w)} s")

    print(f"\nNombre total d’arêtes dans l’arbre : {len(mst)}")
    visualize_mst(mst, station_names)
