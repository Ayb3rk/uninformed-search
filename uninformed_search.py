def BFS (start, finish, list, minNum):
    path = []
    for i in list: #list is sorted naturally
        path.append(i) #we append each node to path
        if(len(path) == minNum): #if path is long enough, we break
            break
    path.append(finish) #we append finish to path
    path.insert(0, start) #we insert start to path
    if(len(path)-2 < minNum): #if path is not long enough, we return None
        return None
    return path #if path is long enough, we return path
    

def DFS (start, finish, customerCoordinates, adjacencyList, minNum) :
    stack = [] #stack
    visitedCustomers = [] #visited customers
    followList = customerCoordinates #list of customers to follow
    for i in followList:
        if(i not in visitedCustomers): #if customer is not visited
            stack.append(i) #we append it to stack
            visitedCustomers.append(i) #we append it to visited customers
        if(len(stack) == minNum): #if stack is long enough, we break
            break
        followList = adjacencyList[customerCoordinates.index(i)] #else we change followList to adjacency list of customer

    stack = stack[::-1] #we reverse stack
    stack.append(finish) #we append finish to stack
    stack.insert(0, start) #we insert start to stack
    if(len(stack)-2 < minNum):
        return None #if stack is not long enough, we return None
    return stack #if stack is long enough, we return stack

def get_cost(src, dest): 
    return abs(src[0]-dest[0]) + abs(src[1]-dest[1])

def UCS ( startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum ) :
    if len(customerCoordinates)-2 < minNum:
        return None
    frontier = [] #priority queue
    frontier.append([0, startCoordiante, [startCoordiante]]) #cost, node, path followed
    costsAndPaths = [] #cost, path (finished paths)
    while frontier:
        node = frontier.pop(0)
        if node[1] not in node[2][:-1]: #if node is not in path (since it includes itself, we check if it is in path except the last one)
            if node[1] == finishCoordinate and len(node[2])-2 < minNum:
                continue #if node is finish and path is not long enough, we continue, do not append it to costsAndPaths
            if len(node[2]) - 2 >= minNum:
                costsAndPaths.append([node[0], node[2]]) #if path is long enough, we append it to costsAndPaths
                continue
            for i in customerAdjacencyList[customerCoordinates.index(node[1])]: #for each node in adjacency list of node
                if i not in node[2]: #if node is not in path
                    frontier.append([node[0]+get_cost(node[1], i), i, node[2] + [i]]) #we append it to frontier with cost, node, path
            frontier.sort(key=lambda x: x[0]) #sort frontier by cost
    if costsAndPaths: #after we finish, if costsAndPaths is not empty
        costsAndPaths.sort(key=lambda x: x[0]) #sort costsAndPaths by cost
        return costsAndPaths[0][1] #return the first path
    return None #if costsAndPaths is empty, return None


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
        customerCoordinates.remove(startCoordiante)
        customerCoordinates.remove(finishCoordinate)
        result = BFS(startCoordiante, finishCoordinate, customerCoordinates, minNum)
    if(method_name == "DFS"):
        customerCoordinates.remove(startCoordiante)
        customerCoordinates.remove(finishCoordinate)
        result = DFS(startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum)
    if(method_name == "UCS"):
        result = UCS(startCoordiante, finishCoordinate, customerCoordinates, customerAdjacencyList, minNum)
    return result

print(UnInformedSearch("BFS", "example.txt"))
