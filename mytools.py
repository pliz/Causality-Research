#collection of helper functions
from itertools import permutations,combinations

#WORKS FOR SUBGRAPHS AND SUPERGRAPHS
#newEi consists of elements of the form
# (e1,e2,...ei+1) where
#every possible combination of size i 
#chosen from e1,e2...ei+1 is in oldEi
def createNextEi(oldEi,i):
    newEi = []
    oldEiset = set()
    for tuple in oldEi:
        oldEiset.add(tuple)
    set1 = set()
    for tuple in oldEi:
        for k in range(0,i):
            set1.add(tuple[k])
    combs = combinations(set1,i+1)
    for comb in combs:
        smallercombsset = set()
        smallercombs = combinations(comb,i)
        for smallercomb in smallercombs:
            smallercombsset.add(smallercomb)
        if smallercombsset.issubset(oldEiset):
            newEi.append(comb)
    return newEi

def createNextEi2(oldEi,i):
    
        
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
#if G^U is desired the input u=U-1
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

#Slightly different from sergey's addanedge
#adds an edge e to graph g
#e[0] is the starting vertex
#e[1] is the ending vertex
def addanedge(g,e):
    mask = maskanedge(g,e)
    g[e[0]][e[1]] =  set([(0,1)])
    return mask

#Slightly different from sergey's delanedge
#delete edge e in graph g
#e[0] is the starting vertex
#e[1] is the ending vertex
def delanedge(g,e):
    g[e[0]].pop(e[1], None)

#returns the number of vertices of graph g
def numofvertices(g):
    return len(g)

#concise way of notating a graph G
def g2num(G): return int(graph2str(G),2)

#helper function for g2num
def graph2str(G):
    n = len(G)
    d = {((0,1),):'1', ((2,0),):'0',((2,0),(0,1),):'0',((0,1),(2,0),):'0'}
    A = ['0']*(n*n)
    for v in G:
        for w in G[v]:
            A[n*(int(v)-1)+int(w)-1] = d[tuple(G[v][w])]
    return ''.join(A)
