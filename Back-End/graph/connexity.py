def is_graph_connected(adj_matrix):
    """
    Vérifie la connexité d'un graphe représenté par une matrice d'adjacence.
    Retourne True si le graphe est connexe, False sinon.
    """
    n = len(adj_matrix)
    if n == 0:
        return True
    visited = set()

    def dfs(u):
        visited.add(u)
        for v, w in enumerate(adj_matrix[u]):
            if w != 0 and v not in visited:
                dfs(v)

    dfs(0)
    return len(visited) == n
