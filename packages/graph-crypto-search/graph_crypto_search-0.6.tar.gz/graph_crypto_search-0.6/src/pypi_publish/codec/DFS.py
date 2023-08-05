graph = {0: [1, 2], 1: [3,0], 2: [3,1,0], 3: [1, 2]}
visited = set()


def dfs(visited, graph, root):
    if root not in visited:
        print(root, end=" ")
        visited.add(root)
        for i in graph[root]:
            dfs(visited, graph, i)

dfs(visited, graph, 0)