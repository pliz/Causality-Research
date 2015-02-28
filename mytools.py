#collection of helper functions
from itertools import permutations,combinations
from functools import wraps
import random




#helper function for checkconflict
#if sublist is contained within superlist, return true
def contained(sublist, superlist):
    temp = superlist[:]
    try:
        for v in sublist:
            temp.remove(v)
        return True
    except ValueError:
        return False

#it is assumed that G_test already has an edge added
#H and G_test should have the same number of vertices
#returns true if there is a conflict
#returns false if there is not a conflict
def checkconflict(H,G_test):
    conflict = True
    Hedges = edgelist(H)
    allundersamples = all_undersamples(G_test)
    for graph in allundersamples:
        gedges = edgelist(graph)
        if contained(gedges,Hedges):
            conflict = False
            break
    return conflict

#it is assumed that G_test already has an edge added
#H and G_test should have the same number of vertices
#returns true if there is equality
#returns false if there is not equality
def checkequality(H,G_test):
    equality = False
    allundersamples = all_undersamples(G_test)
    for graph in allundersamples:
        if graph == H:
            equality = True
    return equality


#helper function for checkconflict
def all_undersamples(G_star,steps=5):
    glist = [G_star]
    while True:
        g = increment_u(G_star, glist[-1])
        if ecj.isSclique(g): return glist # superclique convergence
        # this will (may be) capture DAGs and oscillations
        if g in glist: return glist
        glist.append(g)
    return glist

#helper function for backtrack_more
def memo(func):
    cache = {}                        # Stored subproblem solutions
    @wraps(func)                      # Make wrap look like func
    def wrap(*args):                  # The memoized wrapper
        s = signature(args[0],args[2])# Signature: g and edges
        if s not in cache:            # Not already computed?
            cache[s] = func(*args)    # Compute & cache the solution
        return cache[s]               # Return the cached solution
    return wrap

#helper function for backtrack_more
def esig(l,n):
    '''
    turns edge list into a hash string
    '''
    z = len(str(n))
    n = map(lambda x: ''.join(map(lambda y: y.zfill(z),x)), l)
    n.sort()
    n = ''.join(n[::-1])
    return int('1'+n)

#helper function for backtrack_more
def gsig(g):
    '''
    turns input graph g into a hash string using edges
    '''
    return g2num(g)

#helper function for backtrack_more
def signature(g, edges): return (gsig(g),esig(edges,len(g)))

#helper function for backtrack_more
def isSclique(G):
    n = len(G)
    for v in G:
        if sum([(0,1) in G[v][w] for w in G[v]]) < n: return False
        if sum([(2,0) in G[v][w] for w in G[v]]) < n-1: return False
    return True

#helper function for backtrack_more
def ok2addaVpath(e,p,g,g2):
    mask = addaVpath(g,e,p)
    if not isedgesubset(undersample(g,2), g2):
        cleanVedges(g,e,p,mask)
        return False
    #l = [e[0]] + list(p) + [e[1]]
    #for i in range(len(l)-2):
        #if not edge_increment_ok(l[i],l[i+1],l[i+2],g,g2):
        #    cleanVedges(g,e,p,mask)
        #    return False
        #mask.extend(add2edges(g,(l[i],l[i+2]),l[i+1]))
    cleanVedges(g,e,p,mask)
    return True

#helper function for backtrack_more
def maskaVpath(g,e,p):
    mask = []
    mask.extend([p[0] in g[e[0]], e[1] in g[p[-1]]])
    for i in range(1,len(p)):
        mask.append(p[i] in g[p[i-1]])
    return mask

#helper function for backtrack_more
def addaVpath(g,v,b):
    mask = maskaVpath(g,v,b)

    s = set([(0,1)])
    l = [v[0]] + list(b) + [v[1]]
    for i in range(len(l)-1):
        g[l[i]][l[i+1]] = s
    return mask

#helper function for backtrack_more
def cleanVedges(g, e,p, mask):

    if mask:
        if not mask[0]: g[e[0]].pop(p[0], None)
        if not mask[1]: g[p[-1]].pop(e[1], None)

        i = 0
        for m in mask[2:]:
            if not m: g[p[i]].pop(p[i+1], None)
            i += 1

#helper function for backtrack_more
def delaVpath(g, v, b, mask):
    cleanVedges(g, v, b, mask)

#helper function for backtrack_more
def cloneempty(g): return {n:{} for n in g} # return a graph with no edges

#helper function for backtrack_more
def isedgesubset(g2star,g2):
    '''
    check if g2star edges are a subset of those of g2
    '''
    for n in g2star:
        for h in g2star[n]:
            if h in g2[n]:
                #if not (0,1) in g2[n][h]:
                if not g2star[n][h].issubset(g2[n][h]):
                    return False
            else:
                    return False
    return True

def backtrack_more(g2, rate=1, capsize=None):
    '''
    computes all g1 that are in the equivalence class for g2
    '''
    if isSclique(g2):
        print 'Superclique - any SCC with GCD = 1 fits'
        return set([-1])

    single_cache = {}
    if rate == 1:
        ln = [n for n in g2]
    else:
        ln = [x for x in permutations(g2.keys(),rate)] + [(n,n) for n in g2]

    @memo # memoize the search
    def nodesearch(g, g2, edges, s):
        if edges:
            if undersample(g,rate) == g2:
                s.add(g2num(g))
                if capsize and len(s)>capsize:
                    raise ValueError('Too many elements')
                return g
            e = edges[0]
            for n in ln:

                if (n,e) in single_cache: continue
                if not ok2addaVpath(e,n,g,g2): continue

                mask = addaVpath(g,e,n)
                r = nodesearch(g,g2,edges[1:],s)
                delaVpath(g,e,n,mask)

        elif undersample(g,rate)==g2:
            s.add(g2num(g))
            if capsize and len(s)>capsize:
                raise ValueError('Too many elements in eqclass')
            return g

    # find all directed g1's not conflicting with g2
    n = len(g2)
    edges = edgelist(g2)
    random.shuffle(edges)
    g = cloneempty(g2)

    for e in edges:
        for n in ln:

            mask = addaVpath(g,e,n)
            if not isedgesubset(undersample(g,rate), g2):
                single_cache[(n,e)] = False
            delaVpath(g,e,n,mask)

    s = set()
    try:
        nodesearch(g,g2,edges,s)
    except ValueError:
        s.add(0)
    return s



#newEi consists of elements of the form
# (e1,e2,...ei+1) where
#every possible combination of size i 
#chosen from e1,e2...ei+1 is in oldEi

#this version is for gu to g1 algorithm
def createNextEi1(oldEi,i):
    newEi = []
    oldEiset = set()
    for edgetuple in oldEi:
        oldEiset.add(edgetuple)
    set1 = set()
    for edgetuple in oldEiset:
        for k in range(0,i):
            set1.add(edgetuple[k])  #set1 consists of all the vertices involved in edges in oldEi
    set2 = set()
    combs = combinations(set1,i+1)
    for comb in combs:
        set2.add(comb)
    for object in set2:
        newEi.append(object)
    return newEi

#for super and subgraph algorithm
def createNextEi2(oldEi,i):
    newEi = []
    oldEiset = set()
    for edgetuple in oldEi:
        oldEiset.add(edgetuple)
    set1 = set()
    for edgetuple in oldEiset:
        for k in range(0,i):
            set1.add(edgetuple[k])      
    set2 = set()
    combs = combinations(set1,i+1)
    for comb in combs:
        set2.add(comb)
    oldEisetOfsets = set(frozenset(edgetuple) for edgetuple in oldEiset)
    for comb in set2:
        smallercombsset = set()
        smallercombs = combinations(comb,i)
        set3 = set()
        for smallercomb in smallercombs:
            set3.add(smallercomb)
        set3Ofsets = set(frozenset(edgetuple) for edgetuple in set3)
        if set3Ofsets.issubset(oldEisetOfsets): 
            newEi.append(comb)
    print newEi
    return newEi

        
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
#g itself is changed
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
