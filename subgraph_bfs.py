#BFS implementation of subgraph
from itertools import permutations, combinations
import copy

import sys,os
TOOLSPATH='~/Users/cynthia/Desktop/Causality/Causality-Research/mytools.py'
sys.path.append(os.path.expanduser(TOOLSPATH))

import mytools as tool

#returns all the subgraphs of g that are in the same equivalence class
#as g with respect to gu and the rate
#BFS
def subgraphs_in_eq(g, gu, rate):

    if tool.undersample(g,rate) != gu:
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
