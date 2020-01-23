infinity = 1000000
invalid_node = -1

class Node:
    previous = invalid_node #declares a new notes previous node to -1 as default
    distfromsource = infinity #declated a new nodes distance from source to 1000000 as default
    visited = False #declares new node as unvisited as default

class Dijkstra:

    def __init__(self):
        '''initialise class'''
        self.startnode = 0#initialise all variables, lists and bools to default values
        self.endnode = 0
        self.network = []
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = self.startnode

    def populate_network(self, filename):#reads values from network.txt and adds them to network list
        '''populate network data structure'''
        self.network_populated = False  #set populate netowrk to false before populated
        #load in file contents line by line
        try:
            file = open(filename, "r")  #tries to open readfile
        except IOError:
            print("populate_network: Network file does not exist!") #error if cant open file
            return  #break
        for line in file:#for each line
            self.network.append(list(map(int, line.strip().split(','))))
                #append to network list, converts each number to int after removing the comma
        self.network_populated = True #when all lines appended populate network is true
        file.close()#close read file

    def populate_node_table(self):#function creates a list of nodes from network table and assigns default values read from text file
        self.nodetable_populated = False
        for line in self.network: #loop each line in network table
            self.nodetable.append(Node())#append a node for each line 
        self.nodetable[self.startnode].distfromsource = 0 #start node is source so set distance for that node to 0
        self.currentnode = self.startnode #sets current node to starting node
        self.nodetable_populated = True #nodetable is now populated 


    def parse_route(self,filename):#function determines the start and end node of the route read from text file
        self.route_populated = False
        try:
            routefile = open(filename,'r')#try to open read file
        except IOError:
            print("parse_route: Route file does not exist!")#error if cant open read file
            return  #break
        for line in routefile:#for each line in file
            self.route = line.strip().split('>')
        self.startnode = ord(self.route[0]) - 65 #sets start node by assigning ascii value for char 0 and -65 to bind letter to corresponding number
                                                #e.g ord a = 65 -65 =0
                                                #ord b = 66 -65 = 1
        self.endnode = ord(self.route[1]) - 65#sets end node by assigning ascii value for char 1 and -65 to bind letter to corresponding number
        self.route_populated = True #route is now populated
        routefile.close() # close readfile
        
    def return_near_neighbour(self, query):#function outputs letter and index values of nodes connected to current node and returns index of connected nodes
        neigbhourNodes = [] #list to store the connected nodes
        for index, node in enumerate(self.network[query]):
            if node != 0: #if not looking at current node
                if not self.nodetable[index].visited: #and index != self.endnode:#if the node unvisited
                    neigbhourNodes.append(index)#add neigbhour to list
            #neigbhourNodes.append(self.endnode)
        return neigbhourNodes#return list of neighbours


    def calculate_tentative(self):#calculate distances to source of neighbout nodes nodes and if distance is smaller replace it
        for index, node in enumerate(self.return_near_neighbour(self.currentnode)):#loop through current unvisited neighbours
            if self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][node] < self.nodetable[node].distfromsource:#if the current nodes distance from souce plus the link the the neighbour node is less then the current weight of neighbour node
                self.nodetable[node].distfromsource =  self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][node]#overite distance from source to new value via current node
                self.nodetable[node].previous = self.currentnode#this neighbour nodes previous to curent node
           

                
    
    def determine_next_node(self): 
        minDist = infinity
        minNode = invalid_node  

        for index, node in enumerate(self.nodetable):#loops nodetable
            if self.nodetable[index].visited == False and self.nodetable[index]:
                if minDist > self.nodetable[index].distfromsource and index != self.endnode: 
                    if self.network[self.currentnode][index] !=0:
                        minDist = self.nodetable[index].distfromsource
                        minNode = index
        if self.currentnode!= self.endnode: #makes sure to visit all the other nodes before end node
            if not self.nodetable[minNode].visited:#if node is unvisited and not infinity
                return minNode#return index as the next current node 
            return self.endnode

    def calculate_shortest_path(self):#function to call other functions to calculate shortest path
        while self.currentnode != self.endnode:#keeps looping untill end node is hit
            self.calculate_tentative()#calculate the distances of all neighbours
            self.nodetable[self.currentnode].visited = True#current node is now visited
            self.currentnode = self.determine_next_node()#set new current node to be return value from determine next node function
        self.return_shortest_path()

    
    def return_shortest_path(self):#function loops through the previous node beginning from end node and add to list
        node = self.endnode#variable to store the node to be appended to the list
        route = []#list to store the route
        route.append(chr(self.endnode+65))#append the last node as letter
        while (node != invalid_node):#while this nodes previous node isnt invalid node
            if self.nodetable[node].previous != -1:#if this nodes previous node isnt start node
                route.append(chr(self.nodetable[node].previous+65))#append that nodes previous as a letter to list
                node = self.nodetable[node].previous#set the next node to be looked at as this nodes previous
            else:#if the next node is the start node
                node = invalid_node#set node to previous which will be  to break loop

        route.reverse()#reverse the order of list as it originally starts from end node
        print("ROUTE IS: ",route)#output message to display the route
        print("TOTAL DISTANCE:", self.nodetable[self.endnode].distfromsource)




if __name__ == '__main__':
    Algorithm = Dijkstra()
    Algorithm.populate_network("network.txt")
    Algorithm.parse_route("route.txt")
    Algorithm.populate_node_table()
    print("Network Table:")
    for line in Algorithm.network:
        print(line)
    print(f"Startnode = {Algorithm.startnode} or {chr(Algorithm.startnode+65)}, Endnode = {Algorithm.endnode} or {chr(Algorithm.endnode+65)}")
    Algorithm.calculate_shortest_path()

