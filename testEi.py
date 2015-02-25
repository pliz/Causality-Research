from itertools import combinations

import sys,os
TOOLSPATH='~/Users/cynthia/Desktop/Causality/Causality-Research/mytools.py'
sys.path.append(os.path.expanduser(TOOLSPATH))

import mytools as tool

#for gu to g1 algorithm
def createNextEi1(oldEi,i):
    newEi = []
    oldEiset = set()
    for edgetuple in oldEi:
        oldEiset.add(edgetuple)
    set1 = set()
    for edgetuple in oldEiset:
        print edgetuple
        for k in range(0,i):
            set1.add(edgetuple[k])  #set1 consists of all the vertices involved in edges in oldEi
    set2 = set()
    combs = combinations(set1,i+1)
    for comb in combs:
        set2.add(comb)
    for object in set2:
        newEi.append(object)
    print newEi
    return newEi

    
#for super and subgraph
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

def main():
    #oldEi = combinations(['e1','e2','e3','e4'],2)
    #oldEi = [('e1','e2'),('e1','e3'),('e1','e4'),('e2','e3'),('e2','e4')]
    print list(createNextEi2(oldEi,2)) #should contain [(e1,e2,e3),]

if __name__ == "__main__":
    main()