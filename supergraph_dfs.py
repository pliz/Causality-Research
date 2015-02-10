#DFS implementation of Supergraph
import itertools

def directed_inc(G,D):
    G_un = {}
    # directed edges
    for v in D:
        G_un[v] = {}
        for w in [el for el in D[v] if (0,1) in D[v][el]]:
            for e in G[w]:
                G_un[v][e] = set([(0,1)])
    return G_un

def bidirected_inc(G,D):
    # bidirected edges
    for w in G:
        # transfer old bidirected edges
        l = [e for e in D[w] if (2,0) in D[w][e]]
        for p in l:
            if p in G[w]: 
                G[w][p].add((2,0))
            else: 
                G[w][p] = set([(2,0)])
        # new bidirected edges
        l = [e for e in D[w] if (0,1) in D[w][e]]
        for pair in itertools.permutations(l,2):
            if pair[1] in G[pair[0]]:
                G[pair[0]][pair[1]].add((2,0))
            else:
                G[pair[0]][pair[1]] = set([(2,0)])
    return G

def increment_u(G_star, G_u):
    # directed edges
    G_un = directed_inc(G_star,G_u)
    # bidirected edges
    G_un = bidirected_inc(G_un,G_u)
    return G_un

def undersample(G, u):
    Gu = G
    for i in range(u):
        Gu = increment_u(G, Gu)
    return Gu

def ok2addanedge1(s, e, g, g2,rate=1):
    """
    s - start,
    e - end
    """
    # directed edges
    for u in g:
        if s in g[u] and not (e in g2[u] and (0,1) in g2[u][e]):
            return False
    for u in g[e]: # s -> Ch(e)
        if not (u in g2[s] and (0,1) in g2[s][u]):return False
    # bidirected edges
    for u in g[s]: # e <-> Ch(s)
        if u!=e and not (u in g2[e] and (2,0) in g2[e][u]):return False
    return True

def ok2addanedge2(s, e, g, g2, rate=1):
    mask = addanedge(g,(s,e))
    value = undersample(g,rate) == g2
    delanedge(g,(s,e),mask)
    return value

def ok2addanedge(s, e, g, g2, rate=1):
    f = [ok2addanedge1, ok2addanedge2]
    return f[min([1,rate-1])](s,e,g,g2,rate=rate)

def addanedge(g,e):
    '''
    add edge e[0] -> e[1] to g
    '''
    mask = maskanedge(g,e)
    g[e[0]][e[1]] =  set([(0,1)])
    return mask

def delanedge(g,e,mask):
    '''
    delete edge e[0] -> e[1] from g if it was not there before
    '''
    if not mask[0]: g[e[0]].pop(e[1], None)

def edgelist(g): 
    l = []
    for n in g:
        l.extend([(n,e) for e in g[n] if (0,1) in g[n][e]])
    return l

def g2num(G): return int(graph2str(G),2)

def complement(g):
    n = len(g)
    sq = superclique(n)
    for v in g:
        for w in g[v]:
            sq[v][w].difference_update(g[v][w])
            if not sq[v][w]: sq[v].pop(w)                
    return sq

def superclique(n):
    g = {}
    for i in range(n):
        g[str(i+1)] = {str(j+1):set([(0,1),(2,0)])
                       for j in range(n) if j!=i}
        g[str(i+1)][str(i+1)] = set([(0,1)])
    return g 

def maskanedge(g,e): return [e[1] in g[e[0]]]

def graph2str(G):
    n = len(G)
    d = {((0,1),):'1', ((2,0),):'0',((2,0),(0,1),):'0',((0,1),(2,0),):'0'}
    A = ['0']*(n*n)
    for v in G:
        for w in G[v]:
            A[n*(int(v)-1)+int(w)-1] = d[tuple(G[v][w])]
    return ''.join(A)

def supergraphs_in_eq(g, g2, rate):
    if undersample(g,rate) != g2:
        raise ValueError('g is not in equivalence class of g2')

    s = set()

    def addnodes(g,g2,edges):
        if edges:
            masks  = []
            for e in edges:
                if ok2addanedge(e[0],e[1],g,g2,rate=rate):
                    masks.append(True)
                else:
                    masks.append(False)
            nedges = [edges[i] for i in range(len(edges)) if masks[i]]
            n = len(nedges)
            if n:
                for i in range(n):
                    mask = addanedge(g,nedges[i])
                    s.add(g2num(g))
                    addnodes(g,g2,nedges[:i]+nedges[i+1:])
                    delanedge(g,nedges[i],mask)

    edges = edgelist(complement(g))
    addnodes(g,g2,edges)
    for graph in s:
        print graph
    return s

def main():

    #from page 3 of danks and plis paper
    #g = {
    #'1': {'1': set([(0, 1)]), '2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)])}
    #}
    #gu = undersample(g,1)
    #supergraphs_in_eq(g, gu, 1) #no supergraphs!

    #from email "a task for you"
    #g = {
    #'1': {'2': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)]), '6': set([(0, 1)]), '8': set([(0, 1)])},
    #'6': {'6': set([(0, 1)]), '7': set([(0, 1)])},
    #'7': {'8': set([(0, 1)])},
    #'8': {'1': set([(0, 1)]),'3': set([(0, 1)]),'4': set([(0, 1)]),'7': set([(0, 1)]),'8': set([(0, 1)])}
    #}
    #gu = undersample(g, 1)
    #h is a supergraph in the equivalence class of g with the extra edge (5,7) 
    #h = {
    #'1': {'2': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)]), '7': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)]), '6': set([(0, 1)]), '7': set([(0, 1)]), '8': set([(0, 1)])},
    #'6': {'6': set([(0, 1)]), '7': set([(0, 1)])},
    #'7': {'8': set([(0, 1)])},
    #'8': {'1': set([(0, 1)]),'3': set([(0, 1)]),'4': set([(0, 1)]),'7': set([(0, 1)]),'8': set([(0, 1)])}
    #}
    #supergraphs_in_eq(g, gu, 1) #contains h! yay!

    #from email
    g = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'4': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }
    g3 = undersample(g,2)
    #h1-h4 are ALL the supergraphs of g that lead to the same g3
    #h1 = {
    #'1': {'2': set([(0, 1)]), '3': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #h2 = {
    #'1': {'2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'2': set([(0, 1)]), '4': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #h3 = {
    #'1': {'2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #h4 = {
    #'1': {'2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'4': set([(0, 1)]), '5': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    supergraphs_in_eq(g, g3, 2) #h1-h4 are all found! yay!


if __name__ == "__main__":
    main()