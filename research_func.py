#BFS implementation of subgraph and supergraph
#Gu to G1 algorithm
from itertools import combinations
from functools import wraps
import copy
import time

import sys,os
TOOLSPATH='~/Users/cynthia/Desktop/Causality/Causality-Research/mytools.py'
sys.path.append(os.path.expanduser(TOOLSPATH))

import mytools as tool

#returns all the supergraphs of g that are in the same equivalence class
#as g with respect to gu and the rate
#BFS
def supergraphs_in_eq(g, gu, rate):

    if tool.undersample(g,rate) != gu:
        raise ValueError('g is not in equivalence class of gu')

    #list of supergraphs in same equiv class as g
    s = []

    #initialization for edgetuples with only 1 edge
    initialedges = tool.edgelist(tool.complement(g))
    edgesleft = copy.deepcopy(initialedges)
    #when an edgetuple consists of only 1 edge, it needs to be handled individually
    for edge in initialedges:
        tool.addanedge(g,edge)
        testgu =  tool.undersample(g,rate)
        if testgu == gu:
            addg = copy.deepcopy(g)
            s.append(addg)
            tool.delanedge(g,edge)
        else:
            tool.delanedge(g,edge)
            edgesleft.remove(edge)

    #initialization for edgetuples with 2+edges
    edgetuples = []
    edgetuplesleft = []
    for comb in combinations(edgesleft,2):
        edgetuples.append(comb)
        edgetuplesleft.append(comb)
    #when an edgetuple consists of 2+ edges
    for i in range(2,(tool.numofvertices(g))**2+1):
        for edgetuple in edgetuples:
            for edge in edgetuple:
                tool.addanedge(g,edge)
            testgu = tool.undersample(g,rate)
            if testgu == gu:
                addg = copy.deepcopy(g)
                s.append(addg)
                tool.delanedge(g,edge)
            else:
                edgetuplesleft.remove(edgetuple)
            for edge in edgetuple:
                tool.delanedge(g,edge)
        if not edgetuplesleft:
            break
        else:
            edgetuples = tool.createNextEi2(edgetuples,i)
            edgetuplesleft = copy.deepcopy(edgetuples)

    s1 = set()  #want to return a set of supergraphs
    for graph in s:
        s1.add(tool.g2num(graph))
    #s contains dictionary graph notation
    #s1 contains string graph notation
    print (s,s1)
    return (s,s1)


#returns all the subgraphs of g that are in the same equivalence class
#as g with respect to gu and the rate
#BFS
def subgraphs_in_eq(g, gu, rate):

    if tool.undersample(g,rate) != gu:
        raise ValueError('g is not in equivalence class of gu')

    #list of subgraphs in same equiv class as g
    s = []

    #initialization for edgetuples with only 1 edge
    initialedges = tool.edgelist(g)
    edgesleft = copy.deepcopy(initialedges)
    #when an edgetuple consists of only 1 edge, it needs to be handled individually
    for edge in initialedges:
        tool.delanedge(g,edge)
        testgu =  tool.undersample(g,rate)
        if testgu == gu:
            addg = copy.deepcopy(g)
            s.append(addg)
            tool.addanedge(g,edge)
        else:
            tool.addanedge(g,edge)
            edgesleft.remove(edge)

    #initialization for edgetuples with 2+edges
    edgetuples = []
    edgetuplesleft = []
    for comb in combinations(edgesleft,2):
        edgetuples.append(comb)
        edgetuplesleft.append(comb)
    #when an edgetuple consists of 2+ edges
    for i in range(2,(tool.numofvertices(g))**2+1):
        for edgetuple in edgetuples:
            for edge in edgetuple:
                tool.delanedge(g,edge)
            testgu = tool.undersample(g,rate)
            if testgu == gu:
                addg = copy.deepcopy(g)
                s.append(addg)
            else:
                edgetuplesleft.remove(edgetuple)
            for edge in edgetuple:
                tool.addanedge(g,edge)
        if not edgetuplesleft:
            break
        else:
            edgetuples = tool.createNextEi2(edgetuples,i)
            edgetuplesleft = copy.deepcopy(edgetuples)
    s1 = set()  #want to return a set of subgraphs
    for graph in s:
        s1.add(tool.g2num(graph))
    #s contains dictionary graph notation
    #s1 contains string graph notation
    print (s,s1)
    return (s,s1)

#find the smallest graph in the same equivalence class as g
def findminG1(g,gu,rate):
    (s,s1) = subgraphs_in_eq(g,gu,rate)
    if not s:
        return (g,tool.g2num(g))
    else:
        edges = tool.edgelist(g)
        minnumedge=len(edges)
        for graph in s:
            edges = tool.edgelist(graph)
            numedge = len(edges)
            if minnumedge > numedge:
                minnumedge = numedge
                smallestgraph = graph
        return (smallestgraph,tool.g2num(smallestgraph))





#my exploding version of gu to g1 algorithm
def explodinggutog1(h,max_u):
    G_test = copy.deepcopy(h)
    for edge in tool.edgelist(h):
        tool.delanedge(G_test,edge)
    #G_test is h with all edges removed
    G1_found = False
    u = 1
    while G1_found == False:
        #initialization for edgetuples with only 1 edge
        initialedges = tool.edgelist(tool.superclique(tool.numofvertices(h)))
        edgesleft = copy.deepcopy(initialedges)
        #when an edgetuple consists of only 1 edge, it needs to be handled individually
        for edge in initialedges:
            print "adding edge ", edge
            tool.addanedge(G_test,edge)
            testgu =  tool.undersample(G_test,u)
            if testgu == h:
                print "suceeds for u = ",u
                print "\n"
                G1 = copy.deepcopy(G_test)
                u1 = u
                G1_found = True
                tool.delanedge(G_test,edge)
            else:
                print "fails for u = ",u
                print "\n"
                tool.delanedge(G_test,edge)
        if G1_found == True:
            #print (G1,u1)
            return (G1, u1)
            break
        #initialization for edgetuples with 2+edges
        edgetuples = []
        edgetuplesleft = []
        for comb in combinations(edgesleft,2):
            edgetuples.append(comb)
            edgetuplesleft.append(comb)
        #when an edgetuple consists of 2+ edges
        #i represents the number of edges we wish to add at a time
        for i in range(2,(tool.numofvertices(h))**2+1):
            for edgetuple in edgetuples:
                print "adding edges ",edgetuple
                for edge in edgetuple:
                    tool.addanedge(G_test,edge)
                testgu = tool.undersample(G_test,u)
                if testgu == h:
                    print "succeeds for u = ",u
                    print "\n"
                    G1 = copy.deepcopy(G_test)
                    u1 = u
                    return (G1,u1)
                    G1_found = True
                    tool.delanedge(G_test,edge)
                else:
                    print "fails for u = ",u
                    print "\n"
                    for edge in edgetuple:
                        tool.delanedge(G_test,edge)
                if len(tool.edgelist(testgu))== tool.numofvertices(h)**2:
                    print "testgu has hit superclique"
                    #should I force it to move to the next u?
                    #testing to find out
            if not edgetuplesleft:
                break
            else:
                edgetuples = tool.createNextEi1(edgetuples,i)
                edgetuplesleft = copy.deepcopy(edgetuples)
        u = u + 1
        if u == max_u:
            print "no G found given max_u"
            break




#strawman brute force gu to g1 algorithm
#for comparison
def strawmangutog1(h,max_u):
    g1_list = []
    for u in range(1,max_u):
        g1_list.append(tool.backtrack_more(h, u))
    print g1_list
    return g1_list






#helper function for hopefulgutog1
#returns G1s
def search(G,H,EL,S,newEls,edgesinG):
    newEl = []
    if EL:  #execute this statement if EL is not empty
        for edge in EL:
            tool.addanedge(G,edge)
            if not tool.checkconflict(H,G):
                #if there doesn't exist a conflict
                #ie adding the edge makes one of the undersamples a subset of H
                newEl.append(edge)
            tool.delanedge(G,edge)
        #we have now constructed newEl
        newEl1 = copy.deepcopy(newEl)

        #print "G: ",tool.edgelist(G)
        #print "current new El: ",newEl

        if newEl: #execute if newEl is not empty
            newEls.append(newEl)
        if tool.edgelist(G):
            if not newEl:
                tool.delanedge(G,edgesinG[-1])
                edgesinG.remove(edgesinG[-1])
                newEls[-1].remove(newEls[-1][-1])
            while not newEls[-1]:
                if newEls == [[]]:
                    return None
                tool.delanedge(G,edgesinG[-1])
                edgesinG.remove(edgesinG[-1])
                newEls.remove(newEls[-1])
                newEls[-1].remove(newEls[-1][-1])

        for edge in newEl1:
            tool.addanedge(G,edge)
            edgesinG.append(edge)
            if tool.checkequality(H,G):
                #if there is equality
                #ie adding the edge makes one of the undersamples = H
                #print "G1 found: ",G
                S.add(tool.gsig(G))
                return S


            Gedges = tool.edgelist(G)
            #anotherEl consists of all the edges that Gedges does not have
            anotherEl = tool.edgelist(tool.superclique(tool.numofvertices(H)))
            for gedge in Gedges:
                if gedge in anotherEl:
                    anotherEl.remove(gedge)

            search(G,H,anotherEl,S,newEls,edgesinG)

    else:  #execute this statement if EL is empty(no more edges can be added because we have hit the superclique)
        return None



#hopeful gu to g1 algorithm
#adding edge by edge depth first search
def hopefulgutog1(H):
    G = tool.cloneempty(H)
    EL = tool.edgelist(tool.superclique(tool.numofvertices(H)))
    S = set()
    def search(G,H,EL,S,newEls,edgesinG):
        newEl = []
        if EL:  #execute this statement if EL is not empty
            for edge in EL:
                tool.addanedge(G,edge)
                if not tool.checkconflict(H,G):
                    newEl.append(edge)
                tool.delanedge(G,edge)
            newEl1 = copy.deepcopy(newEl)

            if newEl: #execute if newEl is not empty
                newEls.append(newEl)
            if tool.edgelist(G):
                if not newEl:
                    tool.delanedge(G,edgesinG[-1])
                    edgesinG.remove(edgesinG[-1])
                    newEls[-1].remove(newEls[-1][-1])
                while not newEls[-1]:
                    if newEls == [[]]:
                        return None
                    tool.delanedge(G,edgesinG[-1])
                    edgesinG.remove(edgesinG[-1])
                    newEls.remove(newEls[-1])
                    newEls[-1].remove(newEls[-1][-1])

            for edge in newEl1:
                tool.addanedge(G,edge)
                edgesinG.append(edge)

                if tool.checkequality(H,G): S.add(tool.gsig(G))

                anotherEl = tool.edgelist(tool.complement(G))

                search(G,H,anotherEl,S,newEls,edgesinG)

            else:
                return None

    search(G,H,EL,S,[],[])
    return S


def memo(func):
    cache = {}                        # Stored subproblem solutions
    @wraps(func)                      # Make wrap look like func
    def wrap(*args):                  # The memoized wrapper
        s = tool.signature(args[0],args[2])# Signature: g and edges
        if s not in cache:            # Not already computed?
            cache[s] = func(*args)    # Compute & cache the solution
        return cache[s]               # Return the cached solution
    return wrap


def eqclass(H):
    '''
    Find all graphs in the same equivalence class with respect to
    graph H and any undesampling rate.
    '''
    g = {n:{} for n in H}
    s = set()
    @memo
    def addedges(g,H,edges):
        if edges:
            masks  = []
            for e in edges:
                tool.addanedge(g,e)
                if tool.checkconflict(H,g):
                    masks.append(False)
                else:
                    masks.append(True)
                tool.delanedge(g,e)

            nedges = [edges[i] for i in range(len(edges)) if masks[i]]
            n = len(nedges)
            if n:
                for i in range(n):
                    tool.addanedge(g,nedges[i])
                    if tool.checkequality(H,g):
                        s.add(tool.gsig(g))
                    addedges(g,H,nedges[:i]+nedges[i+1:])
                    tool.delanedge(g,nedges[i])

    edges = tool.edgelist(tool.complement(g))
    addedges(g,H,edges)
    return s




def main():

    #TESTING SUPERGRAPH

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
    #g2 = tool.undersample(g, 1)
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
    #supergraphs_in_eq(g, g2, 1) #contains h! yay!

    #from email
    #g = {
    #'1': {'2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #g3 = tool.undersample(g,2)
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
    #supergraphs_in_eq(g, g3, 2) #h1-h4 are all found! yay!









    #TESTING SUBGRAPH

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
    #g2 = tool.undersample(g, 1)
    #subgraphs_in_eq(g, g2, 1) #contains h! yay!

    #from email
    #g = {
    #'1': {'2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    #'3': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #g3 = tool.undersample(g,2)
    #h1-h3 are all subrgraphs of g that lead to the same g3
    #note h1 is the minimal G1
    #h1 = {
    #'1': {'2': set([(0, 1)])},
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
    #'3': {'4': set([(0, 1)]), '5': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    #'5': {'1': set([(0, 1)])}
    #}
    #subgraphs_in_eq(g, g3, 2) #h1-h3 are all found! yay!
    #findminG1(g,g3,2)   #returns h1
    #findAllGraphs(g, g3, 2)











    #TESTING strawman GU to G1 ALG
    #random
    #H = {
    #'1': {'1': set([(0, 1)]), '3': set([(0, 1), (2, 0)]), '2': set([(0, 1), (2, 0)]), '4': set([(0, 1)])},
    #'3': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1)]), '2': set([(0, 1), (2, 0)])},
    #'2': {'1': set([(0, 1), (2, 0)]), '3': set([(2, 0)]), '2': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)]), '4': set([(0, 1)])}
    #}
    #max_u=5
    #strawmangutog1(H,max_u)













    #TESTING exploding GU TO G1 ALG

    #random
    #H = {
    #'1': {'1': set([(0, 1)]), '3': set([(0, 1), (2, 0)]), '2': set([(0, 1), (2, 0)]), '4': set([(0, 1)])},
    #'3': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1)]), '2': set([(0, 1), (2, 0)])},
    #'2': {'1': set([(0, 1), (2, 0)]), '3': set([(2, 0)]), '2': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)]), '4': set([(0, 1)])}
    #}
    #max_u=5
    #(G,u) = explodinggutog1(H,max_u) #find a G such that H = G^2
    #print "graph is: ",G," and u is: ",u
    #print "in hash notation, G is ",tool.g2num(G)
    #does this G satisfy G^2=H?
    #test = tool.undersample(G,1)
    #if H == test:
    #    print "yes"

    #H= {
    #'1': {'3': set([(2, 0)]), '2': set([(0, 1), (2, 0)]), '5': set([(0, 1), (2, 0)]), '4': set([(0, 1), (2, 0)])},
    #'3': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1)]), '2': set([(0, 1), (2, 0)]), '5': set([(0, 1), (2, 0)]), '4': set([(0, 1), (2, 0)])},
    #'2': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1), (2, 0)]), '2': set([(0, 1)]), '5': set([(0, 1), (2, 0)]), '4': set([(0, 1), (2, 0)])},
    #'5': {'1': set([(2, 0)]), '3': set([(0, 1), (2, 0)]), '2': set([(2, 0)]), '4': set([(0, 1), (2, 0)])},
    #'4': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1), (2, 0)]), '2': set([(0, 1), (2, 0)]), '5': set([(0, 1), (2, 0)]), '4': set([(0, 1)])}
    #}
    #max_u=2
    #(G,u) = explodinggutog1(H,max_u) #find a G such that H = G^2
    #print "graph is: ",G," and u is: ",u
    #here is the G that is returned
    #G = {
    #'1': {'4': set([(0, 1)])},
    #'3': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)]), '5': set([(0, 1)]), '4': set([(0, 1)])},
    #'2': {'3': set([(0, 1)])},
    #'5': {'1': set([(0, 1)]), '2': set([(0, 1)])},
    #'4': {'2': set([(0, 1)]), '5': set([(0, 1)]), '4': set([(0, 1)])}
    #}
    #does this G satisfy G^2=H?
    #test = tool.undersample(G,1)
    #if H == test:
    #    print "yes"











    #TESTING HOPEFUL GU to G1 Algorithm

    H = {
    '1': {'1': set([(0, 1)]), '3': set([(0, 1), (2, 0)]), '2': set([(0, 1), (2, 0)]), '4': set([(0, 1)])},
    '3': {'1': set([(0, 1), (2, 0)]), '3': set([(0, 1)]), '2': set([(0, 1), (2, 0)])},
    '2': {'1': set([(0, 1), (2, 0)]), '3': set([(2, 0)]), '2': set([(0, 1)])},
    '4': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)]), '4': set([(0, 1)])}
    }

    t0 = time.time()
    print hopefulgutog1(H)
    t1 = time.time()
    total = t1-t0
    print "time in seconds: ", total

    #two G's are found
    #G = {
    #'1': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)])},
    #'3': {'1': set([(0, 1)]), '3': set([(0, 1)])},
    #'2': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '2': set([(0, 1)])}
    #}
    #G = {
    #'1': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1)])},
    #'3': {'1': set([(0, 1)])},
    #'2': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)]), '2': set([(0, 1)])}
    #}

    #does this G satisfy G^2=H?
    #test = tool.undersample(G,1)
    #if H == test:
    #    print "yes"

    #H= {
    #'1': {'2': set([(1, 0)])},
    #'2': {'1': set([(1, 0)]), '2': set([(1, 0)])},
    #'3': {'1': set([(1, 0)]), '2': set([(1, 0)])}
    #}
    #hopefulgutog1(H) #can't find any


if __name__ == "__main__":
    main()
