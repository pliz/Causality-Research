#BFS implementation of subgraph and supergraph
#Gu to G1 algorithm
from itertools import combinations
from functools import wraps
import copy
import time
import sys,os

TOOLSPATH='../gunfolds/tools/'
sys.path.append(os.path.expanduser(TOOLSPATH))

import bfutils as bfu
import mytools as tool

def memo(func):
    cache = {}                        # Stored subproblem solutions
    @wraps(func)                      # Make wrap look like func
    def wrap(*args):                  # The memoized wrapper
        s = tool.gsig(args[0])        # Signature: just the g
        #s = tool.signature(args[0],args[2])# Signature: g and edges
        if s not in cache:            # Not already computed?
            cache[s] = func(*args)    # Compute & cache the solution
        return cache[s]               # Return the cached solution
    return wrap

def prune_conflicts(H, g, elist):
    """checks if adding an edge from the list to graph g causes a
    conflict with respect to H and if it does removes the edge
    from the list

    Arguments:
    - `H`: the undersampled graph
    - `g`: a graph under construction
    - `elist`: list of edges to check
    """
    masks  = []
    for e in elist:
        tool.addanedge(g,e)
        if tool.checkconflict(H,g):
            masks.append(False)
        else:
            masks.append(True)
        tool.delanedge(g,e)
    return [elist[i] for i in range(len(elist)) if masks[i]]

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
            nedges = prune_conflicts(H, g, edges)
            n = len(nedges)

            if n == 0: return None

            for i in range(n):
                tool.addanedge(g,nedges[i])
                if tool.checkequality(H,g): return tool.gsig(g)
                s.add(addedges(g,H,nedges[:i]+nedges[i+1:]))
                tool.delanedge(g,nedges[i])

    edges = tool.edgelist(tool.complement(g))
    addedges(g,H,edges)
    return s-set([None])

def main():
    g = bfu.ringmore(4,2);
    H = bfu.undersample(g,2);
    ss = eqclass(H)
    print ss

if __name__ == "__main__":
    main()
