def Dijkstra(G, start):
    # 输入是从 0 开始，所以起始点减 1
    start = start - 1
    inf = float('inf')
    node_num = len(G)
    # visited 代表哪些顶点加入过
    visited = [0] * node_num
    # 初始顶点到其余顶点的距离
    dis = {node: G[start][node] for node in range(node_num)}
    # parents 代表最终求出最短路径后，每个顶点的上一个顶点是谁，初始化为 -1，代表无上一个顶点
    parents = {node: -1 for node in range(node_num)}
    # 起始点加入进 visited 数组
    visited[start] = 1
    # 最开始的上一个顶点为初始顶点
    last_point = start

    for i in range(node_num - 1):
        # 求出 dis 中未加入 visited 数组的最短距离和顶点
        min_dis = inf
        for j in range(node_num):
            if visited[j] == 0 and dis[j] < min_dis:
                min_dis = dis[j]
                # 把该顶点做为下次遍历的上一个顶点
                last_point = j
        # 最短顶点假加入 visited 数组
        visited[last_point] = 1
        # 对首次循环做特殊处理，不然在首次循环时会没法求出该点的上一个顶点
        if i == 0:
            parents[last_point] = start + 1
        for k in range(node_num):
            if G[last_point][k] < inf and dis[k] > dis[last_point] + G[last_point][k]:
                # 如果有更短的路径，更新 dis 和 记录 parents
                dis[k] = dis[last_point] + G[last_point][k]
                parents[k] = last_point + 1

    # 因为从 0 开始，最后把顶点都加 1
    return {key + 1: values for key, values in dis.items()}, {key + 1: values for key, values in parents.items()}


if __name__ == '__main__':
    inf = float('inf')
    name = ['A', 'B', 'C', 'D', 'E']
    G = [
        [0, 7, inf, inf, 1],
        [7, 0, 1, inf, 8],
        [inf, 1, 0, 2, inf],
        [inf, inf, 2, 0, 2],
        [1, 8, inf, 2, 0]
    ]
    start_node = str(input("start_node:")).upper()
    dis, parents = Dijkstra(G, (name.index(start_node) + 1))
    print("dis: ", dis)
    print("parents:", parents, '\n')
    for i in range(len(G)):
        shortest_path = ''
        print(start_node + '-->' + name[i] + ':' + str(dis[i + 1]))
        if name[i] == start_node:
            print(start_node + '\n')
            continue
        shortest_path = f"-->{name[i]}" + shortest_path
        i = i + 1
        while True:
            shortest_path = f"-->{name[parents[i] - 1]}" + shortest_path
            i = parents[i]
            if parents[i] == -1:
                shortest_path = shortest_path.lstrip('-->')
                break
        print(shortest_path + '\n')
