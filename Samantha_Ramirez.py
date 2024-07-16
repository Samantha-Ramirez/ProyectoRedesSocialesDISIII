#import sys
class Community:
    def __init__(self, _id):
        self._id = _id
        self._users = list()

    def getUsers(self):
        return self._users
    
    def addUser(self, userId):
        self.getUsers().append(int(userId))

    def printSolution(self):
        print("Comunidad "+str(self._id)+":")
        self.getUsers().sort()
        users = self.getUsers()

        for i in users:
            print(str(i))

class TestCase:
    def __init__(self, _id, _M, _N):
        self._graph = dict()
        self._id = _id
        self._M = _M if _M >= 1 else 1
        self._N = _N if _N >= 1 else 1
        self._communities = dict()

    def getGraph(self): 
        return self._graph

    def getCommunities(self): 
        return self._communities

    def addCommunity(self, com):
        self.getCommunities().update({com._id:com})

    def createNode(self, P):
        graph = self.getGraph()
        if P>=0 and P<=(self._M-1):
            graph.update({P:[]})
    
    def createEdge(self, P, Q):
        graph = self.getGraph()
        if (P>=0 and Q>=0) and (P<=(self._M-1) and Q<=(self._M-1)):
            if P in graph.keys():
                graph[P].append(Q)
    
    def addChildren(self, current, community, visited):
        graph = self.getGraph()

        # add current 
        visited[current] = True
        community.addUser(current)

        for i in graph.get(current):
            # add user to community
            if not visited[i]:
                visited = self.addChildren(i, community, visited)

        return visited

    def getNextNotVisited(self, visited):
        for i in range(0, len(visited)):
            if not visited[i]:
                return i
        return -1

    def createCommunities(self):
        graph = self.getGraph()
        items = list(graph.keys())
        visited = list()
        
        for i in items:
            visited.append(False)

        current = self.getNextNotVisited(visited)
        i = 1
        while current != -1:
            # create community 
            community = Community(i)
            # add children not visited 
            visited = self.addChildren(current, community, visited)
            current = self.getNextNotVisited(visited)
            i = i+1
            #add community to Test
            self.addCommunity(community)
        
        return self.getCommunities()
    
    def sortCommunities(self, comms):
        def getLessUser(com):
            com[1].getUsers().sort()
            return com[1].getUsers()[0]
        
        return sorted(comms.items(), key=getLessUser)
    
    def printSolution(self):
        print("Caso " + str(self._id) + ":")
        # Comunidades se escribirán en orden ascendente, 
        # se tomará el usuario con menor numero y se ordenarán
        # según ese criterio
        comms = self.getCommunities()
        sortedCommunities = self.sortCommunities(comms)
        for key, i in sortedCommunities:
            i.printSolution()
        print("\n")

class SocialNetwork:
    def __init__(self):
        self._numTestCases = 0
        self._testCases = dict()
    
    def getTestCases(self):
        return self._testCases
    
    def getInput(self):
        text = input()
        self._numTestCases = int(text[0])

        for i in range(1, self._numTestCases+1):
           
            text = input().split(" ")
            # cantidad de usuarios registrados en la red social
            # cantidad de solicitudes de amistad aceptadas en red social           
            Test = TestCase(i, int(text[0]), int(text[1]))

            # create all users in graph
            for i in range(0, Test._M):
                Test.createNode(i)

            # create friendships 
            for i in range(0, Test._N):
                text = input().split(" ")
                userP = int(text[0])
                userQ = int(text[1])
                Test.createEdge(userP, userQ)
                Test.createEdge(userQ, userP)
            
            # add to social network 
            self.addTestCase(Test)

    def addTestCase(self, Test):
        self._testCases.update({Test._id:Test})
    
    def getCommunities(self):
        for key, i in self.getTestCases().items():
            i.createCommunities()
        self.printSolution()

    def printSolution(self):
        for key, i in self.getTestCases().items():
            i.printSolution()
    
RedSocial = SocialNetwork()
RedSocial.getInput()
RedSocial.getCommunities()