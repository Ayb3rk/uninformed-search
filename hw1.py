from importlib.resources import path
import queue


def BFS (start, finish, list, minNum):
    path = []
    for i in list:
        path.append(i)
        if(len(path) == minNum):
            break
    path.append(finish)
    path.insert(0, start)
    if(len(path)-2 < minNum):
        return None
    return path
    

def DFS (start, finish, customerCoordinates, adjacencyList, minNum) :
    path = []
    visitedCustomers = []
    followList = customerCoordinates
    for i in followList:
        if(i not in visitedCustomers):
            path.append(i)
            visitedCustomers.append(i)
        if(len(path) == minNum):
            break
        followList = adjacencyList[customerCoordinates.index(i)]
    path = path[::-1]
    path.append(finish)
    path.insert(0, start)
    if(len(path)-2 < minNum):
        return None
    return path

def get_cost(src, dest): 
    return abs(src[0]-dest[0]) + abs(src[1]-dest[1])
        


def UCS ( startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum ) :
    path = []
    pathsAndCosts = []
    priorityQueue = []
    visitedCustomers = []
    priorityQueue.append([0, startCoordiante])
    distance = {}
    for i in customerCoordinates:
        distance[i] = float("inf")
    distance[startCoordiante] = 0
    while len(priorityQueue) != 0:
        priorityQueue.sort()
        current = priorityQueue.pop(0)
        if current[1] not in visitedCustomers:
            visitedCustomers.append(current[1])
            path.append(current[1])
            if(current[1] == finishCoordinate):
                path = []
                continue
            if(len(path)-1 == minNum):
                finishDistance = get_cost(current[1], finishCoordinate)
                path.append(finishCoordinate)
                pathsAndCosts.append([current[0] + finishDistance, path])
                path = []
                path.append(startCoordiante)
            for i in customerAdjacencyList[customerCoordinates.index(current[1])]:
                if distance[i] > current[0] + get_cost(current[1], i):
                    distance[i] = current[0] + get_cost(current[1], i)
                    if(priorityQueue.count([distance[i], i]) == 0):
                        priorityQueue.append([distance[i], i])
                    else:
                        if priorityQueue[priorityQueue.index([distance[i], i])][0] > distance[i]:
                            priorityQueue[priorityQueue.index([distance[i], i])][0] = distance[i]

    pathsAndCosts.sort()
    return pathsAndCosts[0][1]









def CreateGraphList(env):
    graph = []
    x = 0
    y = 0
    for i in env:
        graph.append([])
        for j in i:
            graph[x].append(j)
            y += 1
        x += 1
    return graph



def UnInformedSearch ( method_name , problem_file_name ) :
    result = []
    env = eval(open(problem_file_name).read())["env"]
    minNum = eval(open(problem_file_name).read())["min"]
    graphList = CreateGraphList(env)
    customerCoordinates = []
    customerAdjacencyList = []
    startCoordiante = ()
    finishCoordinate = ()

    for i in range(len(graphList)):
        for j in range(len(graphList[i])):
            if graphList[i][j] == 'C':
                customerCoordinates.append((i,j))
            if graphList[i][j] == 'S':
                startCoordiante = (i,j)
                customerCoordinates.append((i,j))
            if graphList[i][j] == 'F':
                customerCoordinates.append((i,j))
                finishCoordinate = (i,j)

    for i in customerCoordinates:
        customerAdjacencyList.append([])
        for j in customerCoordinates:
            if i != j:
                customerAdjacencyList[customerCoordinates.index(i)].append(j)
    
    if(method_name == "BFS"):
        result = BFS(startCoordiante, finishCoordinate, customerCoordinates, minNum)
    if(method_name == "DFS"):
        result = DFS(startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum)
    if(method_name == "UCS"):
        result = UCS(startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum)
    return result

print(UnInformedSearch("UCS", "example.txt"))

