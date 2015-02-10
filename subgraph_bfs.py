#BFS implementation of subgraph
from itertools import permutations, combinations
import copy

#returns all the subgraphs of g that are in the same equivalence class
#as g with respect to gu and the rate
#BFS
def subgraphs_in_eq(g, gu, rate):

    if undersample(g,rate) != gu:
        raise ValueError('g is not in equivalence class of gu')

    #set of supergraphs in same equiv class as g
    s = []

    #initialization for edgetuples with only 1 edge
    initialedges = edgelist(g)
    edgesleft = copy.deepcopy(initialedges)   
    #when an edgetuple consists of only 1 edge, it needs to be handled individually
    for edge in initialedges:
        #print "new edge: ",edge
        delanedge(g,edge)
        testgu =  undersample(g,rate)
        if testgu == gu:
            #print "deletion of the edge ", edge, " produces the same gu"
            addg = copy.deepcopy(g)
            s.append(addg)
            addanedge(g,edge)
        else:
            #print "deletion of the edge ", edge, " doesn't produce the same gu"
            addanedge(g,edge)
            edgesleft.remove(edge)

    #initialization for edgetuples with 2+edges
    edgetuples = []
    edgetuplesleft = []
    for comb in combinations(edgesleft,2):
        edgetuples.append(comb)
        edgetuplesleft.append(comb)
    #when an edgetuple consists of 2+ edges
    for i in range(2,numofvertices(g)+1):
        for edgetuple in edgetuples:
            for edge in edgetuple:
                delanedge(g,edge)
            testgu = undersample(g,rate)
            if testgu == gu:
                addg = copy.deepcopy(g)
                s.append(addg)
            else:
                edgetuplesleft.remove(edgetuple)     
            for edge in edgetuple:
                addanedge(g,edge)
        if not edgetuplesleft:  
            break
        else:
            oldedgetuples = edgetuplesleft
            edgetuples = []
            edgetuplesleft = []
            for comb in combinations(oldedgetuples,i+1):
                edgetuples.append(comb)
                edgetuplesleft.append(comb)
    #for graph in s:
    #    print g2num(graph)
    return s

def findminG1(g,gu,rate):
    s = subgraphs_in_eq(g,gu,rate)
    if not s:
        return g
    else:
        edges = edgelist(g)
        minnumedge=len(edges)
        for graph in s:
            edges = edgelist(graph)
            numedge = len(edges)
            if minnumedge > numedge:
                minnumedge = numedge
                smallestgraph = graph
        print g2num(smallestgraph)
        return smallestgraph


#returns all the edges of graph g in the form [('s','e'),('s','e'),....]
def edgelist(g): 
    l = []
    for n in g:
        l.extend([(n,e) for e in g[n] if (0,1) in g[n][e]])
    return l

#helper function for undersample
def directed_inc(G,D):
    G_un = {}
    for v in D:
        G_un[v] = {}
        for w in [el for el in D[v] if (0,1) in D[v][el]]:
            for e in G[w]:
                G_un[v][e] = set([(0,1)])
    return G_un

#helper function for undersample
def bidirected_inc(G,D):
    for w in G:
        l = [e for e in D[w] if (2,0) in D[w][e]]
        for p in l:
            if p in G[w]: 
                G[w][p].add((2,0))
            else: 
                G[w][p] = set([(2,0)])
        l = [e for e in D[w] if (0,1) in D[w][e]]
        for pair in permutations(l,2):
            if pair[1] in G[pair[0]]:
                G[pair[0]][pair[1]].add((2,0))
            else:
                G[pair[0]][pair[1]] = set([(2,0)])
    return G

#helper function for undersample
def increment_u(G_star, G_u):
    # directed edges
    G_un = directed_inc(G_star,G_u)
    # bidirected edges
    G_un = bidirected_inc(G_un,G_u)
    return G_un

#returns the undersampled graph of G 
#if G^U is desired u is U-1
def undersample(G, u):
    Gu = G
    for i in range(u):
        Gu = increment_u(G, Gu)
    return Gu

#returns the superclique of g
def superclique(n):
    g = {}
    for i in range(n):
        g[str(i+1)] = {str(j+1):set([(0,1),(2,0)])
                       for j in range(n) if j!=i}
        g[str(i+1)][str(i+1)] = set([(0,1)])
    return g   

#returns the complement of graph g
def complement(g):
    n = len(g)
    sq = superclique(n)
    for v in g:
        for w in g[v]:
            sq[v][w].difference_update(g[v][w])
            if not sq[v][w]: sq[v].pop(w)                
    return sq

#helper function for addanedge
def maskanedge(g,e): 
    return [e[1] in g[e[0]]]

#Slightly different from your addanedge
#adds an edge e to graph g
#e[0] is the starting vertex
#e[1] is the ending vertex
def addanedge(g,e):
    mask = maskanedge(g,e)
    g[e[0]][e[1]] =  set([(0,1)])
    return mask

#Slightly different from your delanedge
#delete edge e in graph g
#e[0] is the starting vertex
#e[1] is the ending vertex
def delanedge(g,e):
    g[e[0]].pop(e[1], None)

#new function I added
#returns the number of vertices of graph g
def numofvertices(g):
    return len(g)

def g2num(G): return int(graph2str(G),2)

def graph2str(G):
    n = len(G)
    d = {((0,1),):'1', ((2,0),):'0',((2,0),(0,1),):'0',((0,1),(2,0),):'0'}
    A = ['0']*(n*n)
    for v in G:
        for w in G[v]:
            A[n*(int(v)-1)+int(w)-1] = d[tuple(G[v][w])]
    return ''.join(A)

def main():

    #from email "a task for you"
    #g = {
    #'1': {'2': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)]), '6': set([(0, 1)]), '7': set([(0, 1)]), '8': set([(0, 1)])},
    #'6': {'6': set([(0, 1)]), '7': set([(0, 1)])},
    #'7': {'8': set([(0, 1)])},
    #'8': {'1': set([(0, 1)]),'3': set([(0, 1)]),'4': set([(0, 1)]),'7': set([(0, 1)]),'8': set([(0, 1)])}
    #}
    #h is a subgraph in the equivalence class of g with the extra edge (5,7) 
    #h = {
    #'1': {'2': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)]), '6': set([(0, 1)]), '8': set([(0, 1)])},
    #'6': {'6': set([(0, 1)]), '7': set([(0, 1)])},
    #'7': {'8': set([(0, 1)])},
    #'8': {'1': set([(0, 1)]),'3': set([(0, 1)]),'4': set([(0, 1)]),'7': set([(0, 1)]),'8': set([(0, 1)])}
    #}
    #g2 = undersample(g, 1)
    #subgraphs_in_eq(g, g2, 1) #contains h! yay!



    #from email
    g = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }
    g3 = undersample(g,2)
    #h1-h3 are all subrgraphs of g that lead to the same g3
    #note h1 is the minimal G1
    h1 = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'4': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }
    h2 = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'2': set([(0, 1)]), '4': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }
    h3 = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'4': set([(0, 1)]), '5': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }

    #subgraphs_in_eq(g, g3, 2) #h1-h4 are all found! yay!
    findminG1(g,g3,2)   #returns h1

if __name__ == "__main__":
    main()
