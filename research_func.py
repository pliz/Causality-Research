#BFS implementation of subgraph and supergraph
#Gu to G1 algorithm
from itertools import permutations, combinations
import copy

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
        #print "new edge: ",edge
        tool.addanedge(g,edge)
        testgu =  tool.undersample(g,rate)
        if testgu == gu:
            #print "addition of the edge ", edge, " produces the same gu"
            addg = copy.deepcopy(g)
            s.append(addg)
            tool.delanedge(g,edge)
        else:
            #print "addition of the edge ", edge, " doesn't produce the same gu"
            tool.delanedge(g,edge)
            edgesleft.remove(edge)

    #initialization for edgetuples with 2+edges
    edgetuples = []
    edgetuplesleft = []
    for comb in combinations(edgesleft,2):
        edgetuples.append(comb)
        edgetuplesleft.append(comb)
    #when an edgetuple consists of 2+ edges
    for i in range(2,tool.numofvertices(g)+1):
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
            oldedgetuples = edgetuplesleft
            edgetuples = []
            edgetuplesleft = []
            for comb in combinations(oldedgetuples,i+1):
                edgetuples.append(comb)
                edgetuplesleft.append(comb)
    s1 = set()  #want to return a set of supergraphs
    for graph in s:
        s1.add(tool.g2num(graph))
    #s contains dictionary graph notation
    #s1 contains string graph notation
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
        #print "new edge: ",edge
        tool.delanedge(g,edge)
        testgu =  tool.undersample(g,rate)
        if testgu == gu:
            #print "deletion of the edge ", edge, " produces the same gu"
            addg = copy.deepcopy(g)
            s.append(addg)
            tool.addanedge(g,edge)
        else:
            #print "deletion of the edge ", edge, " doesn't produce the same gu"
            tool.addanedge(g,edge)
            edgesleft.remove(edge)

    #initialization for edgetuples with 2+edges
    edgetuples = []
    edgetuplesleft = []
    for comb in combinations(edgesleft,2):
        edgetuples.append(comb)
        edgetuplesleft.append(comb)
    #when an edgetuple consists of 2+ edges
    for i in range(2,tool.numofvertices(g)+1):
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
            oldedgetuples = edgetuplesleft
            edgetuples = []
            edgetuplesleft = []
            for comb in combinations(oldedgetuples,i+1):
                edgetuples.append(comb)
                edgetuplesleft.append(comb)
    s1 = set()  #want to return a set of subgraphs
    for graph in s:
        s1.add(tool.g2num(graph))
    #s contains dictionary graph notation
    #s1 contains string graph notation
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

#finds all the super and subgraphs of a graph g given a rate
def findAllGraphs(g, gu, rate):
    (a,a1) = subgraphs_in_eq(g,gu,rate)
    (b,b1) = supergraphs_in_eq(g,gu,rate)
    c = a+b
    c1 = a1 | b1
    return (c,c1)


#gu to g1 algorithm
#NOT YET WORKABLE
def gutog1(gu):
    if tool.undersample(g,rate) != gu:
        raise ValueError('g is not in equivalence class of gu')

    G_test = copy.deepcopy(gu)
    for edge in edgelist(gu):
        delanedge(G_test,edge)
    #G_test is gu with all edges removed
    G1_found = False
    test_u = 1
    while G1_found == False:
        #initialization for edgetuples with only 1 edge
        initialedges = tool.edgelist(tool.superclique(gu))
        ###this far###
        edgesleft = copy.deepcopy(initialedges)   
        #when an edgetuple consists of only 1 edge, it needs to be handled individually
        for edge in initialedges:
            #print "new edge: ",edge
            tool.addanedge(G_test,edge)
            testgu =  tool.undersample(g,rate)
            if testgu == gu:
                #print "addition of the edge ", edge, " produces the same gu"
                addg = copy.deepcopy(g)
                s.append(addg)
                tool.delanedge(g,edge)
            else:
                #print "addition of the edge ", edge, " doesn't produce the same gu"
                tool.delanedge(g,edge)
                edgesleft.remove(edge)

        #initialization for edgetuples with 2+edges
        edgetuples = []
        edgetuplesleft = []
        for comb in combinations(edgesleft,2):
            edgetuples.append(comb)
            edgetuplesleft.append(comb)
        #when an edgetuple consists of 2+ edges
        for i in range(2,tool.numofvertices(g)+1):
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
                oldedgetuples = edgetuplesleft
                edgetuples = []
                edgetuplesleft = []
                for comb in combinations(oldedgetuples,i+1):
                    edgetuples.append(comb)
                    edgetuplesleft.append(comb)
        s1 = set()  #want to return a set of supergraphs
        for graph in s:
            s1.add(tool.g2num(graph))
        #s contains dictionary graph notation
        #s1 contains string graph notation
        return (s,s1)

def main():

    #TESTING SUPERGRAPH

    #from page 3 of danks and plis paper
    #g = {
    #'1': {'1': set([(0, 1)]), '2': set([(0, 1)])},
    #'2': {'3': set([(0, 1)])},
    #'3': {'4': set([(0, 1)])},
    #'4': {'1': set([(0, 1)])}
    #}
    #g2 = {
    #'1': {'1': set([(0, 1)]), '3': set([(0, 1)]), '2': set([(0, 1), (2, 0)])},
    #'3': {'1': set([(0, 1)])}, 
    #'2': {'1': set([(2, 0)]), '4': set([(0, 1)])}, 
    #'4': {'1': set([(0, 1)]), '2': set([(0, 1)])}
    #}
    #supergraphs_in_eq(g, g2, 1) #no supergraphs!

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
    #g2 = undersample(g, 1)
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
    g = {
    '1': {'2': set([(0, 1)])},
    '2': {'3': set([(0, 1)]), '4': set([(0, 1)])},
    '3': {'4': set([(0, 1)])},
    '4': {'2': set([(0, 1)]), '4': set([(0, 1)]), '5': set([(0, 1)])},
    '5': {'1': set([(0, 1)])}
    }
    g3 = tool.undersample(g,2)
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
    g3 = tool.undersample(g,2)
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

    supergraphs_in_eq(g, g3, 2)
    subgraphs_in_eq(g, g3, 2) #h1-h3 are all found! yay!
    findminG1(g,g3,2)   #returns h1
    findEquivClass(g, g3, 2)

if __name__ == "__main__":
    main()
